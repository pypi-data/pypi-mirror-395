import json
import logging
import select
import time
from contextlib import contextmanager

# 依赖检查：尽量抛出友好的错误
try:
    import psycopg2
    from psycopg2.pool import SimpleConnectionPool
    from psycopg2.extras import RealDictCursor
except ImportError:
    raise ImportError("PgMate requires 'psycopg2' or 'psycopg2-binary'. Please install it via pip.")

# 配置日志 (建议默认不要配置 basicConfig，留给用户配置，只定义 NullHandler 防止报错)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler()) 

class PgMate:
    """
    PgMate: PostgreSQL All-in-One Toolkit
    (Queue + Cron + KV Store + PubSub)
    """
    
    TABLE_JOBS = "_pgmate_jobs"
    TABLE_KV = "_pgmate_kv"
    
    CHANNEL_NOTIFY = "_pgmate_event_new_job"
    FUNC_NOTIFY_TRIGGER = "_pgmate_func_notify_trigger"
    FUNC_ADD_JOB = "_pgmate_func_add_job"
    FUNC_CLEANUP_KV = "_pgmate_func_cleanup_kv"

    def __init__(self, dsn, min_conn=1, max_conn=10):
        self.dsn = dsn
        self.pool = SimpleConnectionPool(min_conn, max_conn, dsn)
        self._init_schema()
        logger.info(f"[PgMate] Initialized. Tables ready: {self.TABLE_JOBS}, {self.TABLE_KV}")

    @contextmanager
    def get_cursor(self, commit=False):
        conn = self.pool.getconn()
        try:
            yield conn.cursor()
            if commit:
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            self.pool.putconn(conn)

    def _init_schema(self):
        ddl_sql = f"""
        CREATE EXTENSION IF NOT EXISTS pg_cron;

        CREATE TABLE IF NOT EXISTS {self.TABLE_JOBS} (
            id BIGSERIAL PRIMARY KEY,
            queue_name TEXT NOT NULL,
            payload JSONB NOT NULL DEFAULT '{{}}', 
            status TEXT NOT NULL DEFAULT 'pending',
            retry_count INT DEFAULT 0,
            max_retries INT DEFAULT 3,
            run_at TIMESTAMPTZ DEFAULT NOW(),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            last_error TEXT
        );

        CREATE TABLE IF NOT EXISTS {self.TABLE_KV} (
            key TEXT PRIMARY KEY,
            value JSONB NOT NULL,
            expires_at TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE INDEX IF NOT EXISTS idx_{self.TABLE_JOBS}_fetch 
            ON {self.TABLE_JOBS} (queue_name, status, run_at) 
            WHERE status = 'pending';
            
        CREATE INDEX IF NOT EXISTS idx_{self.TABLE_KV}_expires 
            ON {self.TABLE_KV} (expires_at);

        CREATE OR REPLACE FUNCTION {self.FUNC_NOTIFY_TRIGGER}() RETURNS TRIGGER AS $$
        BEGIN
            PERFORM pg_notify('{self.CHANNEL_NOTIFY}', NEW.queue_name);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS trg_{self.TABLE_JOBS}_insert ON {self.TABLE_JOBS};
        CREATE TRIGGER trg_{self.TABLE_JOBS}_insert
            AFTER INSERT ON {self.TABLE_JOBS}
            FOR EACH ROW
            EXECUTE FUNCTION {self.FUNC_NOTIFY_TRIGGER}();

        CREATE OR REPLACE FUNCTION {self.FUNC_ADD_JOB}(q_name TEXT, q_payload JSONB) 
        RETURNS VOID AS $$
        BEGIN
            INSERT INTO {self.TABLE_JOBS} (queue_name, payload) VALUES (q_name, q_payload);
        END;
        $$ LANGUAGE plpgsql;

        CREATE OR REPLACE FUNCTION {self.FUNC_CLEANUP_KV}() RETURNS VOID AS $$
        BEGIN
            DELETE FROM {self.TABLE_KV} WHERE expires_at < NOW();
        END;
        $$ LANGUAGE plpgsql;
        """
        with self.get_cursor(commit=True) as cur:
            cur.execute(ddl_sql)

    # --- Queue ---
    def enqueue(self, queue_name, payload, delay_seconds=0):
        sql = f"""
            INSERT INTO {self.TABLE_JOBS} (queue_name, payload, run_at)
            VALUES (%s, %s, NOW() + interval '%s seconds')
            RETURNING id;
        """
        with self.get_cursor(commit=True) as cur:
            cur.execute(sql, (queue_name, json.dumps(payload), delay_seconds))
            return cur.fetchone()[0]

    def _fetch_next_job(self, queue_name):
        sql = f"""
            UPDATE {self.TABLE_JOBS}
            SET status = 'processing', updated_at = NOW()
            WHERE id = (
                SELECT id FROM {self.TABLE_JOBS}
                WHERE queue_name = %s AND status = 'pending' AND run_at <= NOW()
                ORDER BY run_at ASC
                FOR UPDATE SKIP LOCKED LIMIT 1
            )
            RETURNING id, payload, retry_count, max_retries;
        """
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (queue_name,))
                job = cur.fetchone()
            conn.commit()
            return job
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)

    def _finish_job(self, job_id, status, error_msg=None, retry_data=None):
        conn = self.pool.getconn()
        try:
            with conn.cursor() as cur:
                if status == 'completed':
                    cur.execute(f"UPDATE {self.TABLE_JOBS} SET status = 'completed', updated_at = NOW() WHERE id = %s", (job_id,))
                else:
                    retry_count, max_retries = retry_data
                    new_status = 'pending' if retry_count < max_retries else 'failed'
                    next_run = "10 seconds" if new_status == 'pending' else "0 seconds"
                    sql = f"""
                        UPDATE {self.TABLE_JOBS} SET status = %s, last_error = %s, retry_count = retry_count + 1,
                        run_at = NOW() + interval '{next_run}', updated_at = NOW() WHERE id = %s
                    """
                    cur.execute(sql, (new_status, error_msg, job_id))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)

    def listen_and_consume(self, queue_name, handler_func):
        logger.info(f"[PgMate] Worker started. Listening on: {queue_name}")
        listen_conn = psycopg2.connect(self.dsn)
        listen_conn.autocommit = True
        try:
            cursor = listen_conn.cursor()
            cursor.execute(f"LISTEN {self.CHANNEL_NOTIFY};")
            while True:
                while True:
                    job = self._fetch_next_job(queue_name)
                    if not job: break
                    try:
                        handler_func(job['payload'])
                        self._finish_job(job['id'], 'completed')
                    except Exception as e:
                        logger.error(f"[PgMate] Job[{job['id']}] Failed: {e}")
                        self._finish_job(job['id'], 'failed', str(e), (job['retry_count'], job['max_retries']))
                
                if select.select([listen_conn], [], [], 10) != ([], [], []):
                    listen_conn.poll()
                    listen_conn.notifies.clear()
        except KeyboardInterrupt:
            logger.info("[PgMate] Worker stopped.")
        finally:
            listen_conn.close()
            self.pool.closeall()

    # --- Cron ---
    def schedule_cron(self, cron_expression, job_name, queue_name, payload):
        cron_command = f"SELECT {self.FUNC_ADD_JOB}('{queue_name}', '{json.dumps(payload)}'::jsonb)"
        with self.get_cursor(commit=True) as cur:
            cur.execute("SELECT cron.unschedule(%s)", (job_name,))
            cur.execute("SELECT cron.schedule(%s, %s, %s)", (job_name, cron_expression, cron_command))
            logger.info(f"[PgMate] Cron Scheduled: {job_name}")

    # --- KV Store ---
    def kv_set(self, key, value, ttl_seconds=None):
        sql = f"""
            INSERT INTO {self.TABLE_KV} (key, value, expires_at, updated_at)
            VALUES (%s, %s, CASE WHEN %s::int IS NULL THEN NULL ELSE NOW() + interval '%s seconds' END, NOW())
            ON CONFLICT (key) 
            DO UPDATE SET value = EXCLUDED.value, expires_at = EXCLUDED.expires_at, updated_at = NOW();
        """
        with self.get_cursor(commit=True) as cur:
            cur.execute(sql, (key, json.dumps(value), ttl_seconds, ttl_seconds))
            
    def kv_get(self, key, default=None):
        sql = f"SELECT value FROM {self.TABLE_KV} WHERE key = %s AND (expires_at IS NULL OR expires_at > NOW())"
        with self.get_cursor() as cur:
            cur.execute(sql, (key,))
            result = cur.fetchone()
            return result[0] if result else default
            
    def kv_delete(self, key):
        with self.get_cursor(commit=True) as cur:
            cur.execute(f"DELETE FROM {self.TABLE_KV} WHERE key = %s", (key,))

    def enable_kv_cleanup_job(self):
        sys_job_name = "_pgmate_sys_kv_cleanup"
        cmd = f"SELECT {self.FUNC_CLEANUP_KV}()"
        with self.get_cursor(commit=True) as cur:
            cur.execute("SELECT cron.unschedule(%s)", (sys_job_name,))
            cur.execute("SELECT cron.schedule(%s, '5 * * * *', %s)", (sys_job_name, cmd))
            logger.info("[PgMate] System: KV auto-cleanup cron enabled.")
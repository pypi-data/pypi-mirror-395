# PgMate

**PgMate** (formerly PgKit) is a lightweight PostgreSQL All-in-One Toolkit that provides:
- **Queue**: Simple job queue backed by PostgreSQL.
- **Cron**: Scheduled tasks using `pg_cron`.
- **KV Store**: Key-Value store with TTL support.
- **PubSub**: Real-time event notifications using `LISTEN/NOTIFY`.

## Requirements

- Python 3.8+
- PostgreSQL database
- `pg_cron` extension enabled in PostgreSQL (required for Cron and KV cleanup features)

## Installation

```bash
pip install pgmate
```

## Usage

### Initialization

```python
from pgmate import PgMate

# Initialize with PostgreSQL DSN
# Automatically creates necessary tables (_pgmate_jobs, _pgmate_kv) if they don't exist
mate = PgMate(dsn="postgres://user:password@localhost:5432/dbname")
```

### Job Queue

**Producer:**

```python
# Enqueue a job
job_id = mate.enqueue(
    queue_name="my_queue",
    payload={"task": "send_email", "email": "user@example.com"},
    delay_seconds=0
)
print(f"Job enqueued with ID: {job_id}")
```

**Consumer:**

```python
def process_job(payload):
    print(f"Processing: {payload}")
    # Raise exception to retry the job

# Start a worker that listens for new jobs
# This is a blocking call
mate.listen_and_consume("my_queue", process_job)
```

### Key-Value Store

```python
# Set a value with TTL (optional)
mate.kv_set("session:123", {"user_id": 42}, ttl_seconds=3600)

# Get a value
value = mate.kv_get("session:123")
print(value)  # {'user_id': 42}

# Delete a value
mate.kv_delete("session:123")

# Enable auto-cleanup for expired keys (requires pg_cron)
mate.enable_kv_cleanup_job()
```

### Cron Scheduler

Schedule recurring jobs using cron expressions.

```python
# Schedule a job to run every minute
mate.schedule_cron(
    cron_expression="* * * * *",
    job_name="daily_report",
    queue_name="reports",
    payload={"type": "daily"}
)
```

## Architecture

- **Tables**: `_pgmate_jobs`, `_pgmate_kv`
- **Notifications**: Uses `LISTEN/NOTIFY` on channel `_pgmate_event_new_job` for low-latency job processing.
- **Concurrency**: Safe for multiple workers (uses `FOR UPDATE SKIP LOCKED`).

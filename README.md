# Linq Data Take-Home Test

## Objective

Recover and back-calculate missed or incorrectly processed events without using a traditional database.  
This solution uses Apache Kafka to replay event logs and Python to apply stateless, idempotent logic.


## Assumptions

- The system is event-driven, using Kafka to emit and store events.
- Each event has an `id`, a `type` (e.g., `add`, `subtract`), and a `value`.
- Kafka is configured to retain past messages (log-based replay).
- No database is allowed or used.


## My Approach

- Replayed all events from a Kafka topic using `auto_offset_reset='earliest'`.
- Used a Python script to:
  - Deduplicate events by `event_id`
  - Apply arithmetic logic (`add`, `subtract`) in memory
  - Output the final recalculated result
- The logic is stateless, idempotent, and fully database-free.


## Why to Choose This Approach

- Kafka is ideal for event-driven recovery as it allows replaying messages efficiently without requiring a database.
- The solution is stateless and scalable, ensuring resilience without long-term storage.


## Trade-Offs & Limitations

- All logic runs in-memory; no database or disk storage used.
- Replayability relies on logs being available in Kafka for the necessary duration.
- Current implementation is single-threaded but can be parallelized using Kafka partitions.


## If I Had More Tools
With access to:
- A database: I could store checkpoints, audit logs, and snapshot states.
- Logs or S3: I could run batch recovery using AWS Glue or PySpark.
- Apache Flink: I could build a distributed, stateful streaming job with fault tolerance.


## How This Can Be Scaled

If this system needed to process millions of events per hour:
- Use Kafka consumer groups and partitions for parallel processing.
- Move to Apache Flink for production-scale processing.
- Integrate CI/CD, observability, and retries for enterprise readiness.
- Secure the pipeline using IAM, TLS, and compliance practices (HIPAA, GDPR).


## Alternative Approaches Considered
## S3 Log-Based Replay (AWS Glue / Python)
Another valid approach would be to store events as logs in S3 and reprocess them using AWS Glue or a Python script.

**How It Works:**
1. Store Raw Events in S3: Events are logged in JSON format in an S3 bucket (`s3://event-logs/`).
2. Reprocess Events: A Glue job (PySpark) or a Python script reads the logs, deduplicates using `event_id`, and applies transformations (`add`, `subtract`).
3. Output the Final Computed State: The results can be printed or stored back in S3 for further analysis.

**Why I Chose Kafka Over S3:**
- Kafka provides real-time streaming capabilities, while S3 is more suited for batch processing.
- Lower latency: Kafka allows immediate recovery, whereas S3-based processing introduces delays.
- Event retention & replayability: Kafka can retain and replay messages efficiently without requiring external storage.
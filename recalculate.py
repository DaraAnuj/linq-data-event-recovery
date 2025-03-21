from kafka import KafkaConsumer
import json

# Connect to Kafka broker and subscribe to the topic
consumer = KafkaConsumer(
    'events-topic',  # Replace with the Kafka topic name
    bootstrap_servers='localhost:9092',  # Replace with the Kafka broker
    group_id='event-replayer',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize processing state and deduplication tracker
state = {"total": 0}
processed_ids = set()

print("🔁 Starting Kafka replay...\n")

# Process events from Kafka
for msg in consumer:
    event = msg.value
    event_id = event.get("id")
    op = event.get("type")
    val = event.get("value")

    # Skip malformed or unknown events
    if not event_id or op not in ["add", "subtract"]:
        print(f" Skipping invalid event: {event}")
        continue

    # Deduplication based on event ID
    if event_id in processed_ids:
        continue

    processed_ids.add(event_id)

    # Apply operation to in-memory state
    if op == "add":
        state["total"] += val
    elif op == "subtract":
        state["total"] -= val

# Output the final result
print(f"\nFinal recalculated total: {state['total']}")

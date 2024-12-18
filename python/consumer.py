from confluent_kafka import Consumer
import sqlite3
import json

# Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'zoner_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['user_activity'])

# SQLite setup
conn = sqlite3.connect('/db/zoner.db')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_activity (
    user_id INTEGER,
    activity TEXT,
    timestamp REAL
)
""")
conn.commit()

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    event = json.loads(msg.value().decode('utf-8'))
    cursor.execute("""
        INSERT INTO user_activity (user_id, activity, timestamp)
        VALUES (?, ?, ?)
    """, (event['user_id'], event['activity'], event['timestamp']))
    conn.commit()
    print(f"Inserted event: {event}")

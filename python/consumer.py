# python/consumer.py

from confluent_kafka import Consumer
import snowflake.connector
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka consumer configuration
consumer = Consumer({
    'bootstrap.servers': os.getenv("KAFKA_BROKER"),
    'group.id': 'zoner_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['user_activity'])

# Snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('SNOWFLAKE_DATABASE')}")
cursor.execute(f"USE DATABASE {os.getenv('SNOWFLAKE_DATABASE')}")
cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {os.getenv('SNOWFLAKE_SCHEMA')}")
cursor.execute(f"USE SCHEMA {os.getenv('SNOWFLAKE_SCHEMA')}")

table_name = f"{os.getenv('SNOWFLAKE_DATABASE')}.{os.getenv('SNOWFLAKE_SCHEMA')}.user_activity"

# Ensure table exists
cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    user_id INT,
    activity STRING,
    timestamp TIMESTAMP
)
""")

while True:
    try:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        event = json.loads(msg.value().decode('utf-8'))
        cursor.execute(f"""
            INSERT INTO {table_name} (user_id, activity, timestamp)
            VALUES (%(user_id)s, %(activity)s, TO_TIMESTAMP(%(timestamp)s))
        """, event)
        conn.commit()
        print(f"Inserted event into Snowflake: {event}")
    except Exception as e:
        print(f"Error consuming message: {e}")

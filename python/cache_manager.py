# python/cache_manager.py

import redis
import snowflake.connector
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Redis connection
cache = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))

# Snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

def update_cache():
    try:
        cursor.execute(f"""
        SELECT activity, COUNT(*) FROM {os.getenv("SNOWFLAKE_TABLE")}
        GROUP BY activity
        """)
        activity_summary = cursor.fetchall()
        cache.set('activity_summary', json.dumps(activity_summary))
        print("Updated cache:", activity_summary)
    except Exception as e:
        print(f"Error updating cache: {e}")

while True:
    update_cache()
    time.sleep(5)

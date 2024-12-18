import sqlite3
import redis
import json

# Redis connection
cache = redis.Redis(host='redis', port=6379)

# SQLite setup
conn = sqlite3.connect('/db/zoner.db')
cursor = conn.cursor()

def update_cache():
    cursor.execute("""
    SELECT activity, COUNT(*) FROM user_activity
    GROUP BY activity
    """)
    activity_summary = cursor.fetchall()
    cache.set('activity_summary', json.dumps(activity_summary))
    print("Updated cache:", activity_summary)

while True:
    update_cache()
    time.sleep(5)  # Update cache every 5 seconds

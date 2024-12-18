# python/producer.py

from confluent_kafka import Producer
import json
import time
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Kafka configuration
BROKER = os.getenv("KAFKA_BROKER")
producer = Producer({'bootstrap.servers': BROKER})

user_activities = ['sleep', 'meal', 'light_exposure']

def create_event():
    return {
        'user_id': random.randint(1, 100),
        'activity': random.choice(user_activities),
        'timestamp': time.time()
    }

while True:
    try:
        event = create_event()
        producer.produce('user_activity', key=str(event['user_id']), value=json.dumps(event))
        print(f"Produced event: {event}")
        producer.flush()
    except Exception as e:
        print(f"Error producing message: {e}")
    time.sleep(1)

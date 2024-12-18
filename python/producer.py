from confluent_kafka import Producer
import json
import time
import random

producer = Producer({'bootstrap.servers': 'kafka:9092'})

user_activities = ['sleep', 'meal', 'light_exposure']

def create_event():
    return {
        'user_id': random.randint(1, 100),
        'activity': random.choice(user_activities),
        'timestamp': time.time()
    }

while True:
    event = create_event()
    producer.produce('user_activity', key=str(event['user_id']), value=json.dumps(event))
    print(f"Produced event: {event}")
    producer.flush()
    time.sleep(1)

import time, queue
from datetime import datetime, timezone
from faker import Faker
import random

fake = Faker()
message_queue = queue.Queue()

def generate_iot_data():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": f"device_{random.randint(1, 10)}",
        "data_type": "iot",
        "temperature": round(random.uniform(15, 45), 2),
        "humidity": round(random.uniform(30, 90), 2),
        "log_level": None,
        "message": None,
        "response_time_ms": None
    }

def generate_log_data():
    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    weights = [60, 20, 15, 5]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": f"server_{random.randint(1, 5)}",
        "data_type": "log",
        "temperature": None,
        "humidity": None,
        "log_level": random.choices(levels, weights)[0],
        "message": fake.sentence(),
        "response_time_ms": random.randint(10, 2000)
    }

def publish(stop_event):
    print("📡 Publisher started — streaming data...")
    while not stop_event.is_set():
        msg = generate_iot_data() if random.random() > 0.5 else generate_log_data()
        message_queue.put(msg)
        print(f"  → Published: {msg['data_type']} from {msg['device_id']}")
        time.sleep(1)
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from config import PROJECT_ID, CREDENTIALS_PATH
from bigquery_client import insert_rows
import json, time

credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

subscription_path = subscriber.subscription_path(PROJECT_ID, "sensor_data-sub")

ANOMALY_TEMP_THRESHOLD = 40
ANOMALY_RESPONSE_THRESHOLD = 1500

def process_message(msg):
    if msg["data_type"] == "iot":
        if msg["temperature"] and msg["temperature"] > ANOMALY_TEMP_THRESHOLD:
            print(f"  ⚠️ ANOMALY: High temp {msg['temperature']} on {msg['device_id']}")
    elif msg["data_type"] == "log":
        if msg["log_level"] in ["ERROR", "CRITICAL"]:
            print(f"  🔴 ALERT: {msg['log_level']} on {msg['device_id']}")
    return msg

def subscribe(stop_event):
    print("⚙️  Subscriber pulling from real GCP Pub/Sub...")
    batch = []
    while not stop_event.is_set():
        response = subscriber.pull(
            request={"subscription": subscription_path, "max_messages": 5},
            timeout=5
        )
        if not response.received_messages:
            if batch:
                insert_rows(batch)
                batch.clear()
            continue

        ack_ids = []
        for msg in response.received_messages:
            data = json.loads(msg.message.data.decode("utf-8"))
            processed = process_message(data)
            batch.append(processed)
            ack_ids.append(msg.ack_id)

        # Acknowledge messages so they don't get redelivered
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

        if len(batch) >= 5:
            insert_rows(batch)
            batch.clear()
from publisher import message_queue
from bigquery_client import insert_rows

ANOMALY_TEMP_THRESHOLD = 40
ANOMALY_RESPONSE_THRESHOLD = 1500

def process_message(msg):
    if msg["data_type"] == "iot":
        if msg["temperature"] and msg["temperature"] > ANOMALY_TEMP_THRESHOLD:
            print(f"  ⚠️ ANOMALY: High temp {msg['temperature']} on {msg['device_id']}")
    elif msg["data_type"] == "log":
        if msg["log_level"] in ["ERROR", "CRITICAL"]:
            print(f"  🔴 ALERT: {msg['log_level']} — {msg['message'][:50]}")
    return msg

def subscribe(stop_event):
    print("⚙️ Subscriber started...")
    batch = []
    while not stop_event.is_set():
        try:
            msg = message_queue.get(timeout=2)
            processed = process_message(msg)
            batch.append(processed)
            if len(batch) >= 5:
                insert_rows(batch)
                batch.clear()
        except:
            if batch:
                insert_rows(batch)
                batch.clear()
import threading, time
from publisher import publish
from subscriber import subscribe

stop_event = threading.Event()

pub_thread = threading.Thread(target=publish, args=(stop_event,))
sub_thread = threading.Thread(target=subscribe, args=(stop_event,))

pub_thread.start()
sub_thread.start()

print("🚀 Pipeline running... Press Ctrl+C to stop\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Stopping pipeline...")
    stop_event.set()
    pub_thread.join()
    sub_thread.join()
    print("✅ Done")
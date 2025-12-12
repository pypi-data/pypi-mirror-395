# pub_zenoh.py
import time
import json
import numpy as np
import zenoh


class RTGPub:
    def __init__(self, topic_name: str = "vr/rtg"):
        self.session = zenoh.open(zenoh.Config())
        self.pub = self.session.declare_publisher(topic_name)
        print(f"[RTGPub] Publishing on '{topic_name}'")
    
    def publish(self, t: float, values: list):
        payload = json.dumps([t, values]).encode("utf-8")
        self.pub.put(payload)
    
    def shutdown(self):
        self.pub.undeclare()
        self.session.close()

def main():
    rtg_pub = RTGPub()


    freq_hz = 1.2
    t0 = time.perf_counter()

    try:
        while True:
            t = time.perf_counter() - t0
            y = np.sin(2 * np.pi * freq_hz * t) + 0.2 * np.random.randn()

            rtg_pub.publish(t, [y, y, y])

            time.sleep(0.02)  # ~100 Hz publishing rate
    finally:
        rtg_pub.shutdown()


if __name__ == "__main__":
    main()

import zenoh
import time
from ubicoders_vrobots_msgs.M100_mission_generated import Vec3MsgT, MissionMsg, MissionMsgT,VRSceneObjectT
from ubicoders_vrobots_msgs.S007_srv_vrobotphysicalpropertymsg_generated import SrvVRobotPhysicalPropertyMsg, SrvVRobotPhysicalPropertyMsgT
import flatbuffers

class ServiceBase:
    def __init__(self, key: str = "vr/service", recv_timeout: float = 3.0):
        self.key = key
        self.recv_timeout = recv_timeout
        self.recv_signal = False

    def on_reply(self, reply):
        if reply.ok:
            sample = reply.ok
            try:
                print(f"OK {sample.key_expr} -> {sample.payload.to_string()}")
            except Exception:
                b = bytes(sample.payload)
                print(f"OK {sample.key_expr} -> {b!r} (len={len(b)})")
        else:
            print("ERR ->", reply.err.payload.to_string())

        self.recv_signal = True

    def pack(self, message, file_id:str):
        builder = flatbuffers.Builder(1024)
        os = message.Pack(builder)
        builder.Finish(os, bytes(file_id, "utf-8"))
        payload = builder.Output()  
        return payload

    def pack_and_send(self, message, file_id:str):
        with zenoh.open(zenoh.Config()) as session:
            querier = session.declare_querier(self.key, timeout=self.recv_timeout)
            payload = self.pack(message, file_id)
            print("Sending request...")
            querier.get(handler=self.on_reply, payload=zenoh.ZBytes(payload))

            # wait for the reply or timeout
            start_time = time.time()
            start_time_sec = time.time()
            while not self.recv_signal and (time.time() - start_time < self.recv_timeout):
                if time.time() - start_time_sec > 1.0:
                    print("Waiting for reply...")
                    start_time_sec = time.time()
                time.sleep(0.1)
            if not self.recv_signal:
                print("No reply received within timeout")

    
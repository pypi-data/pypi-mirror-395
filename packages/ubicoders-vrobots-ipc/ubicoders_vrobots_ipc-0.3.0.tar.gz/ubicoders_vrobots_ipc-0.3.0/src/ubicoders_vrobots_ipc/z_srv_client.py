# pip install eclipse-zenoh
import zenoh
import time
from ubicoders_vrobots_msgs.M100_mission_generated import Vec3MsgT, MissionMsg, MissionMsgT,VRSceneObjectT
from ubicoders_vrobots_msgs.S007_srv_vrobotphysicalpropertymsg_generated import SrvVRobotPhysicalPropertyMsg, SrvVRobotPhysicalPropertyMsgT
import flatbuffers

KEY = "vr/service"
RECVE_TIMEOUT = 3.0  # seconds
RECVE_SIGNAL = False

def on_reply(reply):
    if reply.ok:
        sample = reply.ok
        try:
            print(f"OK {sample.key_expr} -> {sample.payload.to_string()}")
        except Exception:
            b = bytes(sample.payload)
            print(f"OK {sample.key_expr} -> {b!r} (len={len(b)})")
    else:
        print("ERR ->", reply.err.payload.to_string())

    global RECVE_SIGNAL
    RECVE_SIGNAL = True

    

def main():
    # open session (defaults are fine; set ZENOH_* env vars if needed)
    with zenoh.open(zenoh.Config()) as session:
        querier = session.declare_querier(KEY, timeout=3.0)

        
        # send a couple of test payloads
        # msgT = SrvVRobotPhysicalPropertyMsgT()
        # msgT.timestamp = int(time.time() * 1e9)
        # msgT.request_id = 0
        # msgT.sysId = 0
        # msgT.setMass = True
        # msgT.mass = 3

        # builder = flatbuffers.Builder(512)
        # os = msgT.Pack(builder)
        # builder.Finish(os, bytes("S007", "utf-8"))
        # payload = builder.Output()

        pos = Vec3MsgT()
        pos.x, pos.y, pos.z = 60.6, 160, -3.0
        vrobot = VRSceneObjectT()
        vrobot.objectType = "heli"
        vrobot.position = pos


        mission = MissionMsgT()
        mission.mainScene = "city0_night"
        mission.vrobots =  [vrobot]   
        mission.newMission = True

        builder = flatbuffers.Builder(1024)
        os = mission.Pack(builder)
        builder.Finish(os, bytes("M100", "utf-8"))
        payload = builder.Output()  
        


        print("Sending:", payload)
        querier.get(handler=on_reply, payload=zenoh.ZBytes(payload))

        # wait for the reply or timeout
        start_time = time.time()
        while not RECVE_SIGNAL and (time.time() - start_time < RECVE_TIMEOUT):
            time.sleep(0.1)
        if not RECVE_SIGNAL:
            print("No reply received within timeout")

if __name__ == "__main__":
    main()

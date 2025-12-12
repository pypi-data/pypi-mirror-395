from ubicoders_vrobots_msgs import MissionMsgT, VRSceneObjectT, SrvSimParamsMsgT, SrvVRobotPhysicalPropertyMsgT,SrvResetAllMsgT
from .srv_base import ServiceBase
import time

def req_srv_mission(mission:MissionMsgT=None,):
    service_base = ServiceBase(key="vr/service", recv_timeout=3.0)
    service_base.pack_and_send(mission, file_id="M100")

def req_srv_physical_property(prop:SrvVRobotPhysicalPropertyMsgT=None,):
    service_base = ServiceBase(key="vr/service", recv_timeout=3.0)
    service_base.pack_and_send(prop, file_id="S007")

def req_srv_reset(sysId:int=0):
    service_base = ServiceBase(key="vr/service", recv_timeout=3.0)
    msgT = SrvResetAllMsgT()
    msgT.timestamp = time.time() * 1e3
    msgT.request_id = 0
    msgT.sysId = sysId
    msgT.resetAll = False
    service_base.pack_and_send(msgT, file_id="S000")

def req_srv_reset_all():
    service_base = ServiceBase(key="vr/service", recv_timeout=3.0)
    msgT = SrvResetAllMsgT()
    msgT.timestamp = time.time() * 1e3
    msgT.request_id = 0
    msgT.sysId = 0
    msgT.resetAll = True
    service_base.pack_and_send(msgT, file_id="S000")

def req_srv_simparams(simParams:SrvSimParamsMsgT=None,):
    service_base = ServiceBase(key="vr/service", recv_timeout=3.0)
    service_base.pack_and_send(simParams, file_id="S003")

if __name__ == "__main__":
    # pos = Vec3MsgT()
    # pos.x, pos.y, pos.z = 60.6, 160, -3.0


    # vrobot = VRSceneObjectT()
    # vrobot.objectType = "multirotor"
    # vrobot.position = pos


    # mission = MissionMsgT()
    # mission.vrobots =  [vrobot]   
    # mission.newMission = True

    # req_srv_mission(mission)

    # req_srv_reset_all()
    simparams = SrvSimParamsMsgT()
    simparams.timestamp = time.time() * 1e3
    simparams.setImgResolution = 360
    



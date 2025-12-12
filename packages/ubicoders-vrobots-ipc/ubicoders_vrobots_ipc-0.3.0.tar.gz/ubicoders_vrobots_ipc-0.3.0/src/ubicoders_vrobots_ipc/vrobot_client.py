import cv2

from ubicoders_vrobots_ipc.node_iox2_utils import ImageResolution
from .vrobot_node import VRobotNodeBase, vrobot_client_runner
from .rtg_pub import RTGPub

class VRobotNode(VRobotNodeBase):
    def __init__(self, sysId:int = 0):
        super().__init__(sysId)

    def setup(self):
        self.rtg = RTGPub(topic_name=f"vr/{self.sysId}/rtg")
        # self.state, self.imgStateLeft, self.imgStateRight, self.imgStateDown = self.initialize()
        cv2.namedWindow("CamLeft", cv2.WINDOW_NORMAL)    # make resizable window
        cv2.resizeWindow("CamLeft", 640, 360)
        cv2.namedWindow("CamRight", cv2.WINDOW_NORMAL)   # make resizable window
        cv2.resizeWindow("CamRight", 640, 360)
        cv2.namedWindow("CamDown", cv2.WINDOW_NORMAL)    # make resizable window
        cv2.resizeWindow("CamDown", 640, 360)

        self.register_img_subscriber("left", ImageResolution.P360)
        self.register_img_subscriber("right", ImageResolution.P360)
        self.register_img_subscriber("down", ImageResolution.P360)
        

    def update(self):
        if self.read_new_states():
            ts = self.state.timestamp # unix time in millis
            pos = self.state.linPos
            elapsed_sec = (ts - self.first_ts) / 1000.0
            print(f"State t={elapsed_sec} pos=({pos.x:.2f},{pos.y:.2f},{pos.z:.2f})")
            self.rtg.publish(elapsed_sec, [pos.x, pos.y, pos.z])

        if self.read_new_image("left"):
            img = self.imgStates["left"].image_data
            # print(f"Image ts={self.imgStateLeft.ts}")
            cv2.imshow("CamLeft", img)
            cv2.waitKey(1)

        if self.read_new_image("right"):
            img = self.imgStates["right"].image_data    
            cv2.imshow("CamRight", img)
            cv2.waitKey(1)

        if self.read_new_image("down"):
            img = self.imgStates["down"].image_data
            cv2.imshow("CamDown", img)
            cv2.waitKey(1)

        #self.update_cmd_multirotor([1600, 1600, 1600, 1600])  # neutral pwm to keep hovering
   


if __name__ == "__main__":
    try:
        vrobot_client_runner([VRobotNode(sysId=0)])
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down...")
    finally:
        cv2.destroyAllWindows()
        

import traceback
from typing import Callable, Dict, Tuple, Optional, Any
import zenoh

class ZenohNode:
    def __init__(self, sysId:int=0):
        self.sysId = sysId
        self.session = zenoh.open(zenoh.Config())
        self.pub_dict: Dict[str, zenoh.Publisher] = {}
        self.sub_dict: Dict[str, zenoh.Subscriber] = {}

    def create_publisher(self, topic:str):
        if topic in self.pub_dict:
            return self.pub_dict[topic]
        self.pub_dict[topic] = self.session.declare_publisher(topic)
        print(f"[ZenohNode] Created publisher for topic '{topic}'")
        return self.pub_dict[topic]
        
        
    def create_subscriber(self, topic:str, callback: Callable[[Any], None]):
        if topic in self.sub_dict:
            return self.sub_dict[topic]
        self.sub_dict[topic] = self.session.declare_subscriber(topic, callback)
        print(f"[ZenohNode] Created subscriber for topic '{topic}'")
        return self.sub_dict[topic]
        
    
    def publish(self, topic:str, data: bytes):
        if topic not in self.pub_dict:
            self.create_publisher(topic)
        self.pub_dict[topic].put(data)

    def shutdown(self):
        for sub in self.sub_dict.values():
            sub.undeclare()
        for pub in self.pub_dict.values():
            pub.undeclare()
        self.session.close()
import time
import traceback
from typing import Callable, Dict, Tuple, Optional, Any
import ctypes
import iceoryx2 as iox2
import threading
from .node_iox2_utils import *
from enum import Enum
iox2.set_log_level_from_env_or(iox2.LogLevel.Error)


class Iox2Node:
    def __init__(self, sysId:int=0, subs_poll_millis:int=10, node_name:str=None):
        self.sysId = sysId
        self.sub_dict = {}      # topic -> (subscriber, ImageResolution)
        self.sub_img_data = {}  # topic -> latest image data
        self.sub_threads = {}   # topic -> Thread
        self.stop_event = threading.Event()

        if node_name is None:
            node_name = f"vrobot_node_{sysId}"

        self.node = (
            iox2.NodeBuilder.new()
                .name(iox2.NodeName.new(node_name))
                .create(iox2.ServiceType.Ipc)
        )
        self.subs_poll_millis = subs_poll_millis

    def get_topic_name(self, topic: str, image_resolution: ImageResolution) -> str:
        return f"vr/{self.sysId}/cams/{topic}/{image_resolution.label}"

    def create_image_subscriber(
        self,
        cam_side: str,
        image_resolution: ImageResolution = ImageResolution.P720,
    ):
        if cam_side not in ["left", "right", "down"]:
            raise ValueError(f"Unsupported topic '{cam_side}'; must be 'left', 'right', or 'down'")

        topic_name = self.get_topic_name(cam_side, image_resolution)
        # print(f"payload type: {get_payload_type(image_resolution)}")
        service = (
            self.node.service_builder(iox2.ServiceName.new(topic_name))
                .publish_subscribe(get_payload_type(image_resolution))
                .user_header(GenericHeader)
                .open_or_create()
        )
        subscriber = service.subscriber_builder().create()

        # store before starting the thread to avoid races
        self.sub_dict[topic_name] = (subscriber, image_resolution)

        t = threading.Thread(target=self._listen_loop, args=(topic_name,), daemon=True)
        self.sub_threads[topic_name] = t
        t.start()
        print(f"[Iox2Node] Created subscriber for topic '{topic_name}'")

    def _listen_loop(self, topic_name: str):
        subscriber, image_resolution = self.sub_dict[topic_name]
        image_state_type = get_image_state_type(image_resolution)
        
        try:
            while not self.stop_event.is_set():
                if self.stop_event.is_set():
                    break

                sample = subscriber.receive()
                if sample is None:
                    continue

                header = sample.user_header().contents
                body = sample.payload().contents
                timestamp = header.timestamp / 10e5 # make it millis  
                image_data = body.image_data
                
                flip_mode = body.flip_mode        
                # print(f"topic '{topic_name}' received image ts={timestamp}, flip_mode={flip_mode}, image_data_size={len(image_data)} bytes")      
                self.sub_img_data[topic_name] = image_state_type(timestamp, image_data, flip_mode)
                time.sleep(self.subs_poll_millis / 1000.0)
        except Exception as e:
            self.stop_event.set()
            print(f"Listener for topic '{topic_name}' exiting.")

    def get_image_data(self, cam_side: str, image_resolution: ImageResolution) -> Optional[Any]:
        topic_name = self.get_topic_name(cam_side, image_resolution)
        if self.sub_img_data.get(topic_name) is None:
            return None
        else:
            return self.sub_img_data[topic_name]

    def shutdown(self, timeout: float = 2.0):
        """Signal threads to stop and wait briefly for them to exit."""
        self.stop_event.set()
        # Give each thread a chance to exit; avoid joining current thread.
        for topic, t in list(self.sub_threads.items()):
            if t is threading.current_thread():
                continue
            t.join(timeout=timeout)


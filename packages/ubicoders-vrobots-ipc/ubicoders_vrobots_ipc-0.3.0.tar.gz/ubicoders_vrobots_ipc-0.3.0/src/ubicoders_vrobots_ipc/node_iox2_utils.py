import ctypes
from enum import Enum
import traceback
import cv2
import numpy as np

class GenericHeader(ctypes.Structure):
    """The strongly typed payload type."""

    _fields_ = [
        ("frame_id", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint64),
    ]

    def __str__(self) -> str:
        """Returns human-readable string of the contents."""
        return (
            f"GenericHeader {{ frame_id: {self.frame_id}, timestamp: {self.timestamp} }}"
        )

    @staticmethod
    def type_name() -> str:
        """Returns the system-wide unique type name required for communication."""
        return "GenericHeader"

class ImageData360p(ctypes.Structure):
    """The strongly typed payload type matching C++ ImageData360p exactly."""

    _fields_ = [
        ("flip_mode", ctypes.c_uint8), # 0=none, 1=horizontal, 2=vertical, 3=both
        ("image_data", ctypes.c_uint8 * (640 * 360 * 4)),
    ]

    def __str__(self) -> str:
        """Returns human-readable string of the contents matching C++ operator<<."""
        result = f"ImageData360p {{ image_data_size: {self.image_data.size} bytes, image_data[0]: {self.image_data[0]} }}\n "
        return result

    @staticmethod
    def type_name() -> str:
        """Returns the system-wide unique type name required for communication."""
        return "ImageData360p"  # Matches C++ IOX2_TYPE_NAME

class ImageData720p(ctypes.Structure):
    """The strongly typed payload type matching C++ ImageData720p exactly."""

    _fields_ = [
        ("flip_mode", ctypes.c_uint8), # 0=none, 1=horizontal, 2=vertical, 3=both
        ("image_data", ctypes.c_uint8 * (1280 * 720 * 4)),
    ]

    def __str__(self) -> str:
        """Returns human-readable string of the contents matching C++ operator<<."""
        result = f"ImageData720p {{ image_data_size: {self.image_data.size} bytes, image_data[0]: {self.image_data[0]} }}\n "
        return result

    @staticmethod
    def type_name() -> str:
        """Returns the system-wide unique type name required for communication."""
        return "ImageData720p"  # Matches C++ IOX2_TYPE_NAME
    
class ImageData1080p(ctypes.Structure):
    """The strongly typed payload type matching C++ ImageData1080p exactly."""

    _fields_ = [
        ("flip_mode", ctypes.c_uint8), # 0=none, 1=horizontal, 2=vertical, 3=both
        ("image_data", ctypes.c_uint8 * (1920 * 1080 * 4)),
    ]

    def __str__(self) -> str:
        """Returns human-readable string of the contents matching C++ operator<<."""
        result = f"ImageData1080p {{ image_data_size: {self.image_data.size} bytes, image_data[0]: {self.image_data[0]} }}\n "
        return result

    @staticmethod
    def type_name() -> str:
        """Returns the system-wide unique type name required for communication."""
        return "ImageData1080p"  # Matches C++ IOX2_TYPE_NAME


class BaseImageState:
    def __init__(self, ts: ctypes.c_uint64 = 0, image_data=None, flip_mode: int = 0,
                 width: int = 0, height: int = 0, channels: int = 4):
        self.ts: ctypes.c_uint64 = ts
        self.flip_mode: int = flip_mode
        self.width: int = width
        self.height: int = height
        self.channels: int = channels
        self.image_data: np.ndarray = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)
        try:
            if image_data is None:
                return

            img_rgba = np.ctypeslib.as_array(image_data).reshape(
                (self.height, self.width, self.channels)
            )

            if flip_mode == 1:
                img_rgba = cv2.flip(img_rgba, 1)
            elif flip_mode == 2:
                img_rgba = cv2.flip(img_rgba, 0)
            elif flip_mode == 3:
                img_rgba = cv2.flip(img_rgba, -1)

            # store the converted image - copy
            self.image_data: np.ndarray = cv2.cvtColor(img_rgba, cv2.COLOR_RGBA2BGR)

        except Exception:
            # only print traceback when there IS an exception
            print(f"[{self.__class__.__name__}] Error ts={ts}")
            traceback.print_exc()
            self.image_data: np.ndarray = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)

# Subclasses for specific resolutions
class ImageState360p(BaseImageState):
    def __init__(self, ts: ctypes.c_uint64 = 0, image_data=None, flip_mode: int = 0):
        super().__init__(ts, image_data, flip_mode, width=640, height=360, channels=4)


class ImageState720p(BaseImageState):
    def __init__(self, ts: ctypes.c_uint64 = 0, image_data=None, flip_mode: int = 0):
        super().__init__(ts, image_data, flip_mode, width=1280, height=720, channels=4)


class ImageState1080p(BaseImageState):
    def __init__(self, ts: ctypes.c_uint64 = 0, image_data=None, flip_mode: int = 0):
        super().__init__(ts, image_data, flip_mode, width=1920, height=1080, channels=4)





class ImageResolution(Enum):
    P360 = (640, 360, 4)
    P720 = (1280, 720, 4)
    P1080 = (1920, 1080, 4)

    def __init__(self, width, height, channels):
        self.width = width
        self.height = height
        self.channels = channels

    @property
    def label(self) -> str:
        return f"{self.height}p"




def get_image_state_type(image_resolution: ImageResolution):
    if image_resolution == ImageResolution.P360:
        return ImageState360p
    elif image_resolution == ImageResolution.P720:
        return ImageState720p
    elif image_resolution == ImageResolution.P1080:
        return ImageState1080p
    else:
        raise ValueError(f"Unsupported image_resolution '{image_resolution}'; must be ImageResolution.6020, P720, or P1080")    

def get_payload_type(image_resolution: ImageResolution):
    if image_resolution == ImageResolution.P360:
        # NOTE: Your C++ type is 360p; keep this if C++ publishes 360p.
        return ImageData360p
    elif image_resolution == ImageResolution.P720:
        return ImageData720p
    elif image_resolution == ImageResolution.P1080:
        return ImageData1080p
    else:
        raise ValueError(f"Unsupported image_resolution '{image_resolution}'")        
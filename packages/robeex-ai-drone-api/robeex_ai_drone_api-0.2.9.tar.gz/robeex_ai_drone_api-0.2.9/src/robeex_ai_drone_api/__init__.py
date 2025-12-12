from .video_api import UDPVideoStream, FrameSize
from .nav_api import DroneNavAPI, DroneNavCommand, DroneNavMode, DroneNavState
from .rgb_led_api import DroneRGBLedApi, RGBMode, RGBLedIndex, MotorNumber
from .rc_api import RcApi, DroneTelemetry
from .ai_drone import RobeexAIDrone

try:
    import cv2
except ImportError as e:
    raise ImportError(
        "OpenCV is required. Install with:\n"
        "  pip install opencv-python"
    ) from e

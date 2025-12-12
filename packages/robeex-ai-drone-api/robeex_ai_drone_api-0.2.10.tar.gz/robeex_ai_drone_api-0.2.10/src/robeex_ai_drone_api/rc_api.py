import sys
import socket
import threading
import json
from robeex_ai_drone_api import DroneNavAPI, DroneRGBLedApi, DroneBottomFlashLedApi

class DroneTelemetry:
    def __init__(self, x: float, y: float, z: float, wz: float, battery: int, is_armed: bool, roll: float, pitch: float, distance: int):
        self.x = x  # Position X in meters
        self.y = y  # Position Y in meters
        self.z = z  # Altitude in meters
        self.wz = wz  # Yaw in radians
        self.battery = battery  # Battery percentage
        self.is_armed = is_armed  # Armed status
        self.roll = roll  # Roll angle in radians
        self.pitch = pitch  # Pitch angle in radians
        self.distance = distance  # Distance sensor measurement in cm

    def __str__(self):
        return f"[x={self.x}, y={self.y}, z={self.z}, wz={self.wz}, battery={self.battery}, is_armed={self.is_armed}, roll={self.roll}, pitch={self.pitch}, distance={self.distance}]"

class RcApi:
    """
    Remote Control API
    used for interaction with the drone
    """
    
    nav: DroneNavAPI
    rgb: DroneRGBLedApi
    bottom_flash_led: DroneBottomFlashLedApi

    def __init__(self, drone_ip, drone_port, debug = False):
        self.drone_ip = drone_ip
        self.drone_port = drone_port
        self.debug = debug
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1.0)  # Set a timeout for socket operations

        if sys.platform.startswith("win") and not hasattr(socket, "SO_REUSEPORT"):
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('', drone_port))

        self.nav = DroneNavAPI(self)  # Initialize the navigation API
        self.rgb = DroneRGBLedApi(self)  # Initialize the rgb API
        self.bottom_flash_led = DroneBottomFlashLedApi(self) # Initialize the bottom flash API

        self.telemetry_data: DroneTelemetry  # Explicitly use DroneTelemetry as the data type
        self._stop_event = threading.Event()
        self._telemetry_thread = threading.Thread(target=self._telemetry_rx_thread, daemon=True)
        self._is_running = False  # Flag to prevent multiple starts
        self._telemetry_event = threading.Event()  # Event to signal telemetry updates

    def start(self):
        """Start the telemetry receiving thread."""
        if self._is_running:  # Prevent multiple starts
            print("Telemetry thread is already running.")
            return
        self._is_running = True
        self._stop_event.clear()
        self._telemetry_thread.start()

    def stop(self):
        """Stop the telemetry receiving thread."""
        if not self._is_running:  # Prevent stopping if not running
            print("Telemetry thread is not running.")
            return
        self._is_running = False
        self._stop_event.set()
        self._telemetry_thread.join()

    def send_command(self, command: dict):
        """Send a command to the server."""
        try:
            s = json.dumps(command).encode()
            addr = (self.drone_ip, self.drone_port)
            # print(s, addr)
            self.sock.sendto(s, addr)
        except Exception as e:
            print(f"Error sending command: {e}")

    def _decode_telemetry(self, data: str) -> DroneTelemetry:
        """
        Decode telemetry data from RcAPI.

        :return: An instance of DroneTelemetry containing all telemetry data.
        """
        telemetry = json.loads(data)
        return DroneTelemetry(
            x=telemetry["x"],
            y=telemetry["y"],
            z=telemetry["z"],
            wz=telemetry["wz"],
            battery=telemetry["battery"],
            is_armed=bool(telemetry["a"]),
            roll=telemetry["r"],
            pitch=telemetry["p"],
            distance=telemetry["dis"]
        )

    def _telemetry_rx_thread(self):
        """Thread to receive telemetry data from the server."""
        while not self._stop_event.is_set():
            try:
                data, _ = self.sock.recvfrom(1024)  # Buffer size of 1024 bytes

                telemetry_data_str = data.decode()
                self.telemetry_data = self._decode_telemetry(telemetry_data_str)

                self._telemetry_event.set()  # Signal that telemetry data has been updated
                self._telemetry_event.clear()  # Reset the event for the next update
            except socket.timeout:
                continue  # Ignore timeout and keep polling
            except Exception as e:
                print(f"Error receiving telemetry: {e}")
                break

    def get_next_telemetry_update(self):
        """
        Wait for the telemetry thread to update telemetry data and return the value.

        :return: An instance of DroneTelemetry containing all telemetry data.
        """
        self._telemetry_event.wait()
        # loop = asyncio.get_event_loop()
        # await loop.run_in_executor(None, self._telemetry_event.wait)  # Wait for the event to be set
        return self.telemetry_data

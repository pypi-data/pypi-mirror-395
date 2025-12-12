import math
import robeex_ai_drone_api
from enum import IntFlag
from time import sleep
from .vec2 import Vec2

class DroneNavMode:
    DISABLE = "DISABLE"
    READY_TO_FLY = "READY_TO_FLY"
    TAKEOFF = "TAKEOFF"
    LAND = "LAND"
    MOVE = "MOVE"
    FAILSAFE = "FAILSAFE"

DRONE_NAV_MODE_TO_FLIGHT_MODE = {
    "DISABLE": 0,
    "READY_TO_FLY": 0,
    "TAKEOFF": 1,
    "LAND": 2,
    "MOVE": 5,
    "FAILSAFE": 128,
}

POSITION_SETPOINT_DEADZONE = 0.15
YAW_SETPOINT_DEADZONE_RAD = math.radians(15)
class IgnoreAxis(IntFlag):
    NONE = 0
    X = 1
    Y = 2
    Z = 4
    YAW = 8

class DroneNavState:
    def __init__(self, x=0, y=0, z=0, wz=0, mode=DroneNavMode.DISABLE):
        self.x = x  # Position X in meters
        self.y = y  # Position Y in meters
        self.z = z  # Altitude in meters
        self.wz = wz  # Yaw in radians
        self.mode = mode  # Current offboard mode


class DroneNavCommand:
    def __init__(self, is_rc: bool, roll=0, pitch=0, thrust=-500, yaw=0, arm=False, fmode=DroneNavMode.DISABLE):
        self.is_rc = is_rc
        self.roll = roll
        self.pitch = pitch
        self.thrust = thrust
        self.yaw = yaw
        self.arm = arm
        self.fmode = fmode

    def to_json(self):
        """
        Converts the NavCommand to a JSON-compatible dictionary.
        """
        return {
            "_": 0,
            "r": int(self.roll),
            "p": int(self.pitch),
            "t": int(self.thrust),
            "y": int(self.yaw),
            "a": 1 if self.arm else 0,
            "f": self.fmode,
            "rc": self.is_rc,
        }


class DroneNavAPI:
    """
    Handles drone movements
    """

    _UPPER_ALT_RANGE = 1.5

    def __init__(self, rc_api, debug = False):
        self.rc_api: robeex_ai_drone_api.RcApi = rc_api
        self.debug = debug
        self.offboard_state = DroneNavState()

    def __send_cmd(self, roll=0, pitch=0, thrust=-500, yaw=0, arm=False, fmode=DroneNavMode.DISABLE):
        """
        Sends a JSON command to the drone via RcAPI.

        :param roll: Roll value.
        :param pitch: Pitch value.
        :param thrust: Thrust value.
        :param yaw: Yaw value.
        :param arm: Arm status (True/False).
        :param fmode: Flight mode (OffboardMode).
        """
        command = DroneNavCommand(
            is_rc=False,
            roll=roll,
            pitch=pitch,
            thrust=thrust,
            yaw=yaw,
            arm=arm,
            fmode=fmode,
        )
        self.rc_api.send_command(command.to_json())

    def update_offboard_state(self, **kwargs):
        """
        Updates the offboard state and sends the corresponding command.

        :param kwargs: Key-value pairs to update the offboard state.
        """
        for key, value in kwargs.items():
            if hasattr(self.offboard_state, key):
                if self.debug:
                    print(key, '=', value)
                setattr(self.offboard_state, key, value)
            else:
                raise AttributeError(f"Invalid attribute: {key}")

        is_arm = self.offboard_state.mode != DroneNavMode.DISABLE and self.offboard_state.mode != DroneNavMode.FAILSAFE
        flight_mode = DRONE_NAV_MODE_TO_FLIGHT_MODE.get(self.offboard_state.mode, 0)

        self.__send_cmd(
            roll=self.offboard_state.x * 500,
            pitch=self.offboard_state.y * 500,
            thrust=(self.offboard_state.z / self._UPPER_ALT_RANGE) * 1000 - 500,
            yaw=(self.offboard_state.wz / math.pi) * 500,
            arm=is_arm,
            fmode=flight_mode,
        )

    def set_mode(self):
        """
        Sets the drone to the DISABLE mode.
        """
        self.update_offboard_state(mode=DroneNavMode.DISABLE)

    def arm(self):
        """
        Arms the drone and sets it to the READY_TO_FLY mode.
        """
        self.update_offboard_state(mode=DroneNavMode.READY_TO_FLY)

    def disarm(self):
        """
        Disarms the drone and disables offboard mode.
        """
        self.update_offboard_state(mode=DroneNavMode.DISABLE)

    def kill(self):
        """
        Sends the drone into FAILSAFE mode.
        """
        self.update_offboard_state(mode=DroneNavMode.FAILSAFE)

    def takeoff(self, altitude_meter: float, tolerance: float = 0.1, wait_until_done: bool = True):
        """
        Commands the drone to take off to a specified altitude.

        :param altitude_meter: The target altitude in meters.
        :param tolerance: The altitude tolerance in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.TAKEOFF, z=altitude_meter)
        if wait_until_done:
            self.wait_for_latest_setpoint(tolerance, ignore_axis=IgnoreAxis.X | IgnoreAxis.Y | IgnoreAxis.YAW)

    def land(self, wait_until_done: bool = True):
        """
        Commands the drone to land by setting the altitude to 0.

        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.LAND, z=0)
        if wait_until_done:
            self.wait_for_latest_setpoint(0.1, ignore_axis=IgnoreAxis.X | IgnoreAxis.Y | IgnoreAxis.YAW)

    def go_forward(self, meter: float, wait_until_done: bool = True):
        """
        Moves the drone forward by a specified distance.

        :param meter: The distance to move forward in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        body_frame_move_vec = Vec2(0, meter)
        world_frame_move_vec = body_frame_move_vec.rotate(-self.offboard_state.wz)

        self.update_offboard_state(mode=DroneNavMode.MOVE, x=self.offboard_state.x + world_frame_move_vec.x, y=self.offboard_state.y + world_frame_move_vec.y)
        if wait_until_done:
            self.wait_for_latest_setpoint()

    def go_backward(self, meter: float, wait_until_done: bool = True):
        """
        Moves the drone backward by a specified distance.

        :param meter: The distance to move backward in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.go_forward(-meter, wait_until_done)

    def go_right(self, meter: float, wait_until_done: bool = True):
        """
        Moves the drone to the right by a specified distance.

        :param meter: The distance to move right in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        body_frame_move_vec = Vec2(meter, 0)
        world_frame_move_vec = body_frame_move_vec.rotate(-self.offboard_state.wz)

        self.update_offboard_state(mode=DroneNavMode.MOVE, x=self.offboard_state.x + world_frame_move_vec.x, y=self.offboard_state.y + world_frame_move_vec.y)
        if wait_until_done:
            self.wait_for_latest_setpoint()

    def go_left(self, meter: float, wait_until_done: bool = True):
        """
        Moves the drone to the left by a specified distance.

        :param meter: The distance to move left in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.go_right(-meter, wait_until_done)

    def set_yaw(self, yaw_in_rad: float, wait_until_done: bool = True):
        """
        Sets the drone's yaw to a specific angle.

        :param yaw_in_rad: The target yaw angle in radians.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.MOVE, wz=yaw_in_rad)
        if wait_until_done:
            self.wait_for_latest_setpoint(
                POSITION_SETPOINT_DEADZONE, YAW_SETPOINT_DEADZONE_RAD
            )

    def turn_cw(self, rotation_in_rad: float, wait_until_done: bool = True):
        """
        Rotates the drone clockwise by a specified angle.

        :param rotation_in_rad: The angle to rotate in radians.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.MOVE, wz=self.offboard_state.wz + rotation_in_rad)
        if wait_until_done:
            self.wait_for_latest_setpoint(
                POSITION_SETPOINT_DEADZONE, YAW_SETPOINT_DEADZONE_RAD
            )

    def set_position_2d(self, x_m: float, y_m: float, wait_until_done: bool = True):
        """
        Sets the drone's position to specific coordinates.

        :param x_m: The target X coordinate in meters.
        :param y_m: The target Y coordinate in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.MOVE, x=x_m, y=y_m)
        if wait_until_done:
            self.wait_for_latest_setpoint(ignore_axis=IgnoreAxis.YAW)

    def set_position_3d(self, x_m: float, y_m: float, z_m: float, wait_until_done: bool = True):
        """
        Sets the drone's position to specific coordinates.

        :param x_m: The target X coordinate in meters.
        :param y_m: The target Y coordinate in meters.
        :param z_m: The target Z coordinate in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.MOVE, x=x_m, y=y_m, z=z_m)
        if wait_until_done:
            # self.wait_for_latest_setpoint()
            self.wait_for_latest_setpoint(ignore_axis=IgnoreAxis.YAW)

    def set_altitude(self, altitude_meter: float, wait_until_done: bool = True):
        """
        Sets the drone's altitude to a specific value.

        :param altitude_meter: The target altitude in meters.
        :param wait_until_done: Whether to wait until the setpoint is reached.
        """
        self.update_offboard_state(mode=DroneNavMode.MOVE, z=altitude_meter)
        if wait_until_done:
            self.wait_for_latest_setpoint()

    def wait_for_latest_setpoint(self, pos_tolerance: float = POSITION_SETPOINT_DEADZONE, yaw_tolerance: float = YAW_SETPOINT_DEADZONE_RAD, ignore_axis: IgnoreAxis = IgnoreAxis.NONE):
        """
        Waits for the drone to reach the setpoint within the specified tolerances.

        :param pos_tolerance: The position tolerance in meters.
        :param yaw_tolerance: The yaw tolerance in radians.
        :param ignore_axis: Axes to ignore during setpoint checks (bit mask).
        """
        while True:
            telemetry = self.rc_api.get_next_telemetry_update()

            pos_err = 0
            if not (ignore_axis & IgnoreAxis.X):
                pos_err += (telemetry.x - self.offboard_state.x) ** 2
            if not (ignore_axis & IgnoreAxis.Y):
                pos_err += (telemetry.y - self.offboard_state.y) ** 2
            if not (ignore_axis & IgnoreAxis.Z):
                pos_err += (telemetry.z - self.offboard_state.z) ** 2
            pos_err = math.sqrt(pos_err)

            yaw_err = 0 if (ignore_axis & IgnoreAxis.YAW) else abs(telemetry.wz - self.offboard_state.wz)

            if self.debug:
                print('wait', 'pos err:', pos_err, 'yaw err:', yaw_err)
                print(self.offboard_state.z, '==', telemetry.z)

            if pos_err < pos_tolerance and yaw_err < yaw_tolerance:
                break

            sleep(0.1)

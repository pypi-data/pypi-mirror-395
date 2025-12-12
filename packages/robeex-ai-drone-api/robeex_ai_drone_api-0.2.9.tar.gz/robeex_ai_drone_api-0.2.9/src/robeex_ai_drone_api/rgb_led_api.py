from enum import Enum, IntEnum
from typing import Union
import robeex_ai_drone_api


class RGBMode(Enum):
    """
    Drone RGB LEDs Mode
    - AUTO: Normal operation - showing drone current status
    - MANUAL: Color set by user using the API
    """

    AUTO = "AUTO"
    MANUAL = "MANUAL"


class MotorNumber(IntEnum):
    """
    Drone Motor Motor Number
    - 1: Top Right
    - 2: Top Left
    - 3: Bottom Left
    - 4: Bottom Left
    """
    MOTOR_1 = 1
    MOTOR_2 = 2
    MOTOR_3 = 3
    MOTOR_4 = 4

class RGBLedIndex(IntEnum):
    ALL = 0
    DISABLE = -1
    MOTOR_1 = 1
    MOTOR_2 = 2
    MOTOR_3 = 3
    MOTOR_4 = 4


class SetRGBLedCommand:
    def __init__(self, r: int, g: int, b: int, a: int, index: RGBLedIndex):
        """
        Represents a command to set the RGB LED state.

        :param r: Red intensity (0-255).
        :param g: Green intensity (0-255).
        :param b: Blue intensity (0-255).
        :param a: Brightness (0-255).
        :param index: LED index (-1 for disable, 0 for all, 1-4 for specific motors).
        """
        self.r = self._to_fix_digit(r)
        self.g = self._to_fix_digit(g)
        self.b = self._to_fix_digit(b)
        self.a = self._to_fix_digit(a)
        self.index = RGBLedIndex(self._to_fix_digit(index))

    def _to_fix_digit(self, x: Union[int, float]) -> int:
        """
        Converts a number to an integer with fixed digits.

        :param x: The number to convert.
        :return: The fixed integer.
        """
        return int(round(x))

    def to_json(self):
        """
        Converts the command to a JSON-compatible dictionary.
        """
        return {
            "_": 1,
            "r": self.r,
            "g": self.g,
            "b": self.b,
            "a": self.a,
            "i": self.index,
        }


class DroneRGBLedApi:
    """
    Handles interactions with Drone RGB LEDs
    """
    
    def __init__(self, rc_api):
        self.rc_api: robeex_ai_drone_api.RcApi = rc_api
        self.last_cmd = None
        self.brightness = 255  # Default brightness (0-255)

    def set_brightness(self, brightness: int):
        """
        Sets the brightness of the LEDs.

        :param brightness: Brightness percentage (0-100).
        """
        brightness = max(0, min(brightness, 100))
        self.brightness = int((brightness / 100) * 255)

        if not self.last_cmd:
            return

        # Update the color with the new brightness
        self.__set_color(
            self.last_cmd.r,
            self.last_cmd.g,
            self.last_cmd.b,
            self.last_cmd.index,
        )

    def __set_color(self, r: int, g: int, b: int, index: RGBLedIndex):
        """
        Sets the color of the LEDs.

        :param r: Red intensity (0-255).
        :param g: Green intensity (0-255).
        :param b: Blue intensity (0-255).
        :param index: LED index (-1 for disable, 0 for all, 1-4 for specific motors).
        """
        self.__send_cmd(r, g, b, self.brightness, index)

    def set_mode(self, mode: RGBMode):
        """
        Sets the mode of the LEDs (AUTO or MANUAL).

        :param mode: The mode to set (RGBMode.AUTO or RGBMode.MANUAL).
        """
        if not self.last_cmd:
            return

        current_mode = RGBMode.AUTO if self.last_cmd.index == RGBLedIndex.DISABLE else RGBMode.MANUAL

        if current_mode == mode:
            return

        if mode == RGBMode.AUTO:
            self.__send_cmd(0, 0, 0, 0, RGBLedIndex.DISABLE)
        else:
            self.__send_cmd(0, 0, 0, 0, RGBLedIndex.ALL)

    def set_full_color(self, r: int, g: int, b: int):
        """
        Sets the same color for all LEDs.

        :param r: Red intensity (0-255).
        :param g: Green intensity (0-255).
        :param b: Blue intensity (0-255).
        """
        self.__set_color(r, g, b, RGBLedIndex.ALL)

    def set_color_by_motor_number(self, r: int, g: int, b: int, index: MotorNumber):
        """
        Sets the color for a specific LED index.

        :param r: Red intensity (0-255).
        :param g: Green intensity (0-255).
        :param b: Blue intensity (0-255).
        :param index: LED index (-1 for disable, 0 for all, 1-4 for specific motors).
        """
        self.__set_color(r, g, b, RGBLedIndex(index))

    def __send_cmd(self, r: int, g: int, b: int, a: int, index: RGBLedIndex):
        """
        Sends a command to set the RGB LED state.

        :param r: Red intensity (0-255).
        :param g: Green intensity (0-255).
        :param b: Blue intensity (0-255).
        :param a: Brightness (0-255).
        :param index: LED index (-1 for disable, 0 for all, 1-4 for specific motors).
        """
        cmd = SetRGBLedCommand(r, g, b, a, index)
        self.last_cmd = cmd
        self.rc_api.send_command(cmd.to_json())

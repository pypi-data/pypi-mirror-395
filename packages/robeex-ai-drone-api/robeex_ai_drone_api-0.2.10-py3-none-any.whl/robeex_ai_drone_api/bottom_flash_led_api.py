from typing import Union, Optional
import robeex_ai_drone_api

class SetBottomFlashLedCommand:
    def __init__(self, brightness: int):
        """
        Represents a command to set the RGB LED state.

        :param brightness: Brightness (0-255).
        """
        self.brightness = self._to_fix_digit(brightness)

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
            "_": 2,
            "b": self.brightness
        }


class DroneBottomFlashLedApi:
    """
    Handles interactions with Drone Bottom Flash LED
    """

    def __init__(self, rc_api):
        self.rc_api: robeex_ai_drone_api.RcApi = rc_api
        self.last_cmd: Optional[SetBottomFlashLedCommand] = None

    def set_brightness(self, brightness: int):
        """
        Sets the brightness of the LED.

        :param brightness: Brightness percentage (0-100).
        """
        brightness = max(0, min(brightness, 100))

        if not self.last_cmd is None and self.last_cmd.brightness == brightness:
            return

        # Update the color with the new brightness
        self.__send_cmd(
            brightness
        )

    def __send_cmd(self, b: int):
        """
        Sends a command to set the RGB LED state.

        :param b: brightness (0-255).
        """
        cmd = SetBottomFlashLedCommand(b)
        self.last_cmd = cmd
        self.rc_api.send_command(cmd.to_json())

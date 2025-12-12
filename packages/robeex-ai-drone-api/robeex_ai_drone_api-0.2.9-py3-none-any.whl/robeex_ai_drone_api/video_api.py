import sys
from typing import Literal, Optional, Tuple, Union
import cv2
import numpy as np
import socket
from time import time
from enum import Enum

# TODO: get back to check enum docs

class FrameSize(Enum):
    """
    Enum for supported frame sizes.
    """

    SIZE_XHD = 12
    SIZE_HD = 11
    SIZE_1024x768 = 10
    SIZE_800x600 = 9
    SIZE_640x480 = 8
    SIZE_480x320 = 7
    SIZE_400x296 = 6
    SIZE_320x240 = 5
    SIZE_240x240 = 4


class UDPVideoStream:
    def __init__(self, host: str, port: int, chunk_size: int = 1324, timeout: int = 2, debug = False):
        """
        Initializes the UDP video stream.

        :param host: The IP address of the UDP server.
        :param port: The port of the UDP server.
        :param chunk_size: The size of each UDP packet.
        :param timeout: The timeout for the socket in seconds.
        """
        self.host = host
        self.port = port
        self.chunk_size = chunk_size
        self.timeout = timeout
        self.sock = None
        self.is_streaming = False
        self.fps = None
        self.last_time = time()
        self.debug = debug

    def __del__(self):
        self.release()

    def open(self, frame_size: FrameSize = FrameSize.SIZE_640x480, jpeg_quality: int = 45) -> Literal[True]:
        """
        Opens the UDP socket and starts the stream.

        :param frame_size: The frame size as a FrameSize enum value.
        :param jpeg_quality: The JPEG compression quality (0 to 100).
        :return: True if the stream is open, Throws otherwise.
        """
        if not isinstance(frame_size, FrameSize):
            raise ValueError(f"Invalid frame size. Use a value from the FrameSize enum.")
        if not (5 <= jpeg_quality <= 63):
            raise ValueError("JPEG quality must be between 5 and 63 (inclusive).")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if sys.platform.startswith("win") and not hasattr(socket, "SO_REUSEPORT"):
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.settimeout(self.timeout)
        self.sock.bind(('', self.port))

        start_command = f"start {frame_size.value} {jpeg_quality}".encode()
        self.sock.sendto(start_command, (self.host, self.port))
        self.is_streaming = True

        return True

    def release(self):
        """
        Releases the UDP socket and stops the stream.
        """
        if self.sock:
            self.sock.sendto(b"stop", (self.host, self.port))
            self.sock.close()
            self.sock = None
        self.is_streaming = False

    def isOpened(self):
        """
        Checks if the stream is open.

        :return: True if the stream is open, False otherwise.
        """
        return self.is_streaming

    def read(self) -> Union[Tuple[Literal[False], Literal[None]], Tuple[Literal[True], Literal[cv2.Mat]]]:
        """
        Reads a frame from the UDP stream.

        :return: A tuple (success, frame), where success is a boolean indicating
                 if the frame was successfully read, and frame is the decoded image.
        """
        if not self.is_streaming:
            return False, None

        data = b''
        pk_sum = 0
        is_ok = True

        while True:
            try:
                chunk, addr = self.sock.recvfrom(self.chunk_size)
                if len(chunk) < self.chunk_size:
                    pk_sum += chunk[0]
                    data += chunk
                    cs, addr = self.sock.recvfrom(1)
                    cs = cs[0]
                    tcs = pk_sum & 0xFF
                    if cs != tcs:
                        # print(len(data), 'checksum=', cs, '!=', tcs)
                        is_ok = False
                    break
                else:
                    pk_sum += chunk[0]
                    data += chunk
            except Exception as e:
                print('Error:', e)
                return False, None

        if not is_ok or not self._data_is_valid_jpeg(data):
            if self.debug:
                print('[Warning]: Invalid frame data received')
            return False, None

        nparr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            if self.debug:
                print('[Warning]: Failed to decode frame')
            return False, None

        # Calculate FPS
        current_time = time()
        elapsed_time = current_time - self.last_time
        self.last_time = current_time
        self.fps = 1 / elapsed_time if elapsed_time > 0 else None

        return True, frame

    def get_fps(self) -> Optional[float]:
        """
        Returns the current FPS of the stream.

        :return: The FPS as a float, or None if not available.
        """
        return self.fps

    @staticmethod
    def _data_is_valid_jpeg(data):
        """
        Validates if the data is a valid JPEG.

        :param data: The data to validate.
        :return: True if the data is a valid JPEG, False otherwise.
        """
        return len(data) > 2 and data[:2] == b'\xff\xd8' and data[-2:] == b'\xff\xd9'

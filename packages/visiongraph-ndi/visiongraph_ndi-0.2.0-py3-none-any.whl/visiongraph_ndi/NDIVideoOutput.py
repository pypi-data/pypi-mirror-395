from argparse import ArgumentParser, Namespace
from fractions import Fraction
from typing import Optional

import cv2
import numpy as np
from cyndilib import VideoSendFrame, FourCC, Sender
from visiongraph.output.fbs.FrameBufferSharingServer import FrameBufferSharingServer


class NDIVideoOutput(FrameBufferSharingServer):
    """
    Manages NDI video output for frame buffering and sharing. This class enables sending
    video frames with specified properties like width, height, frame rate, and format
    using a shared buffer mechanism.
    """

    def __init__(self, name: str, width: int = 1, height: int = 1, frame_rate: float = 60):
        """
        Initializes the NDI video output instance with specified properties.

        Args:
            name (str): The name of the NDI video stream.
            width (int): The width of the video frame in pixels.
            height (int): The height of the video frame in pixels.
            frame_rate (float): The frame rate of the video output.
        """
        super().__init__(name)

        self.fourcc: FourCC = FourCC.BGRA
        self.width: int = width
        self.height: int = height
        self.frame_rate: float = frame_rate

        self.sender: Optional[Sender] = None
        self.video_send_frame: Optional[VideoSendFrame] = None

    def setup(self):
        """
        Initializes or resets the NDI sender and associated video frame.
        """
        self._reset_sender()

    def send(self, frame: np.ndarray, flip_texture: bool = False):
        """
        Sends a frame to the NDI output, optionally flipping the texture.

        Args:
            frame (np.ndarray): The frame to be sent, expected in BGRA or BGR format.
            flip_texture (bool): Whether to flip the frame vertically for compatibility.
        """
        if frame.shape[2] != 4:
            frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        else:
            frame_rgba = frame

        if flip_texture:
            # make a horizontal flip just to be compatible to other FrameBufferSharingServer
            frame_rgba = cv2.flip(frame_rgba, 0)

        # check is frame size has changed and reset sender if necessary
        h, w = frame_rgba.shape[:2]
        x_res, y_res = self.video_send_frame.get_resolution()

        if x_res != w or y_res != h:
            self.width = w
            self.height = h

            # reset sender
            self._reset_sender()

        # create data to be sent
        data = frame_rgba.reshape(w * h * 4)[:self.video_send_frame.get_data_size()]
        self.video_send_frame.write_data(data)
        self.sender.send_video_async()

    def _reset_sender(self):
        """
        Resets the NDI sender, ensuring proper setup of the video frame with
        the specified resolution, frame rate, and format.
        """
        if self.sender is not None:
            self.sender.close()
            self.sender = None

        if self.video_send_frame is not None:
            self.video_send_frame.destroy()
            self.video_send_frame = None

        # setup video frame
        self.video_send_frame = VideoSendFrame()
        self.video_send_frame.set_resolution(self.width, self.height)
        self.video_send_frame.set_frame_rate(Fraction(int(self.frame_rate), 1))
        self.video_send_frame.set_fourcc(self.fourcc)

        self.sender = Sender(ndi_name=self.name)
        self.sender.set_video_frame(self.video_send_frame)

        self.sender.open()

    def release(self):
        """
        Releases resources by destroying the video frame and closing the sender.
        """
        if self.video_send_frame is not None:
            self.video_send_frame.destroy()
            self.video_send_frame = None

        if self.sender is not None:
            self.sender.close()
            self.sender = None

    def configure(self, args: Namespace):
        """
        Configures the video output settings using provided command-line arguments.

        Args:
            args (Namespace): Parsed arguments for configuration.
        """
        pass

    @staticmethod
    def add_params(parser: ArgumentParser):
        """
        Adds relevant parameters to the argument parser for configuring NDI video output.

        Args:
            parser (ArgumentParser): The argument parser to be configured.
        """
        pass

    @staticmethod
    def create(name: str) -> "NDIVideoOutput":
        """
        Factory method to create an instance of NDIVideoOutput.

        Args:
            name (str): The name of the NDI video output instance.

        Returns:
            NDIVideoOutput: A new instance of NDIVideoOutput.
        """
        return NDIVideoOutput(name)

    def __enter__(self):
        """
        Context manager entry to set up the NDI video output.

        Returns:
            NDIVideoOutput: The initialized NDI video output instance.
        """
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit to release the NDI video output resources.

        Args:
            exc_type: Exception type if an exception occurred.
            exc_val: Exception value if an exception occurred.
            exc_tb: Traceback if an exception occurred.
        """
        self.release()

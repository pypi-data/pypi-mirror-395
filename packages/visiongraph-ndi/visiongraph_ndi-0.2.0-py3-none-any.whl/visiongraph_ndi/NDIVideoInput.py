import time
from argparse import ArgumentParser, Namespace
from typing import Optional, List

import numpy as np
from cyndilib import RecvBandwidth, Finder, Source, Receiver, VideoFrameSync, RecvColorFormat
from visiongraph.input.BaseInput import BaseInput


class NDIVideoInput(BaseInput):
    """
    A class to handle NDI video input streams, allowing video data capture from a specific stream
    and host with configurations for color format, bandwidth, and connection settings.
    """

    def __init__(self,
                 stream_name: Optional[str] = None,
                 host_name: Optional[str] = None):
        """
        Initializes the NDIVideoInput object with optional stream and host names.

        Args:
            stream_name (Optional[str]): Name of the stream to connect to.
            host_name (Optional[str]): Name of the host providing the stream.
        """
        super().__init__()

        self.stream_name = stream_name
        self.host_name = host_name

        self.color_format: RecvColorFormat = RecvColorFormat.BGRX_BGRA
        self.bandwidth: RecvBandwidth = RecvBandwidth.highest

        self.finder: Optional[Finder] = None
        self.source: Optional[Source] = None
        self.receiver: Optional[Receiver] = None
        self.video_frame_sync: Optional[VideoFrameSync] = None

    def setup(self):
        """
        Sets up the connection to the NDI video source by locating the stream and initializing
        the receiver with appropriate settings for frame sync and connection.

        Raises:
            Exception: If the source specified by stream_name and host_name cannot be found.
        """
        self.finder = Finder()
        self.finder.open()

        self.source = self.get_source_by_name(self.stream_name, self.host_name)
        if self.source is None:
            raise Exception(f"Could not find source {self.stream_name} @ {self.host_name}!")

        # setup receiver
        self.receiver = Receiver(
            color_format=self.color_format,
            bandwidth=self.bandwidth,
        )
        self.video_frame_sync = VideoFrameSync()
        frame_sync = self.receiver.frame_sync
        frame_sync.set_video_frame(self.video_frame_sync)

        self.receiver.connect_to(self.source)
        self._wait_for_connection()

    def read(self) -> (int, Optional[np.ndarray]):
        """
        Captures a video frame from the connected source.

        Returns:
            tuple[int, Optional[np.ndarray]]: A timestamp in milliseconds and the captured image
            data as a numpy array, or -1 and None if the capture failed.
        """
        if not self.receiver.is_connected():
            return -1, None

        self.receiver.frame_sync.capture_video()

        data = self.video_frame_sync.get_array()

        if len(data) == 0:
            return -1, None

        # The data has to be interpreted using the stride
        line_stride = self.video_frame_sync.get_line_stride()
        data_size = self.video_frame_sync.get_data_size()
        width, height = self.video_frame_sync.get_resolution()
        channels = 4

        # re-interpret data and crop to actual resolution
        image = data.reshape(int(data_size / line_stride), int(line_stride / channels), channels)
        image = image[0:height, 0:width]

        ts = int(self.video_frame_sync.get_timestamp_posix() * 1000)

        # update information
        self.width = width
        self.height = height
        self.fps = float(self.video_frame_sync.get_frame_rate())

        return self._post_process(ts, image)

    def release(self):
        """
        Releases resources by closing the Finder instance and resetting it to None.
        """
        self.finder.close()
        self.finder = None

    def get_source_by_name(self,
                           stream_name: Optional[str] = None,
                           host_name: Optional[str] = None,
                           timeout: float = 1.0) -> Optional[Source]:
        """
        Searches for an NDI source matching the given stream and host names.

        Args:
            stream_name (Optional[str]): Name of the stream to search for.
            host_name (Optional[str]): Name of the host to search for.
            timeout (float): Time to wait for sources, in seconds.

        Returns:
            Optional[Source]: A source object if a matching source is found, or None otherwise.
        """
        _ = self.finder.wait_for_sources(timeout=timeout)
        for source in self.finder.iter_sources():
            stream_match = stream_name == source.stream_name
            host_match = host_name == source.host_name

            if stream_name is None and host_match:
                return source

            if host_name is None and stream_match:
                return source

            if stream_match and host_match:
                return source

            if stream_name is None and host_name is None:
                return source

        return None

    @staticmethod
    def find_sources(timeout: float = 1.0) -> List[Source]:
        """
        Finds and lists all available NDI sources within the specified timeout.

        Args:
            timeout (float): Time to wait for sources, in seconds.

        Returns:
            List[Source]: A list of available NDI sources.
        """
        with Finder() as finder:
            _ = finder.wait_for_sources(timeout=timeout)
            sources = list(finder.iter_sources())
            return sources

    def _wait_for_connection(self, timeout: float = 5.0):
        """
        Waits for a connection to be established with the NDI source.

        Args:
            timeout (float): Maximum time to wait for a connection, in seconds.

        Raises:
            Exception: If a connection cannot be established within the timeout period.
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.receiver.is_connected():
                return

        raise Exception("Could not connect.")

    def configure(self, args: Namespace):
        """
        Configures the video input settings based on command-line arguments.

        Args:
            args (Namespace): Parsed command-line arguments for configuration.
        """
        pass

    @staticmethod
    def add_params(parser: ArgumentParser):
        """
        Adds configuration parameters to the argument parser for the NDI video input.

        Args:
            parser (ArgumentParser): The argument parser to add parameters to.
        """
        pass

    def __enter__(self):
        """
        Initializes resources when entering a context manager.

        Returns:
            NDIVideoInput: The initialized NDI video input instance.
        """
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Releases resources when exiting a context manager.
        """
        self.release()

    @property
    def is_connected(self):
        """
        Checks if the receiver is connected to an NDI source.

        Returns:
            bool: True if connected, False otherwise.
        """
        if self.receiver is None:
            return False

        return self.receiver.is_connected()

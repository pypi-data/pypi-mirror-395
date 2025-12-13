from quicktions import Fraction
from abc import ABC, abstractmethod
from typing import Union


class _VideoSource(ABC):
    """
    Abstract class that is a media source
    containing video information.
    """

    @property
    @abstractmethod
    def copy(
        self
    ):
        """
        Get a copy of this video source instance.
        """
        pass

    @property
    @abstractmethod
    def is_unchanged(
        self
    ) -> bool:
        """
        *For internal use only*

        Internal boolean flag to indicate if the source has
        been modified (or not), useful when we want to 
        optimize the way we access to the frames to render.

        If the original source has not been modified, we
        don't need to read frame by frame and apply any
        change so we can do it faster.

        (!) This property has to be modified by the specific
        video sources.
        """
        pass

    @property
    @abstractmethod
    def duration(
        self
    ):
        """
        The duration of the source.
        """
        pass

    @property
    @abstractmethod
    def size(
        self
    ):
        """
        The size of the original source, that can
        match or match not the 'output_size'.
        """
        pass

    def __init__(
        self
    ):
        pass

    @abstractmethod
    def get_video_frame_at(
        self,
        t: Union[int, float, Fraction],
        size: Union[tuple[int, int], None] = None,
        do_apply_filters: bool = True
        # TODO: Return 'VideoFrame' or 'numpy' (?)
    ):
        """
        Get the video frame that must be displayed
        at the 't' time moment.
        """
        pass

    @abstractmethod
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction],
        do_apply_filters: bool = True
        # TODO: Return 'VideoFrame' or 'numpy' (?)
    ):
        """
        Get the audio frames that must be played
        during the 't' time moment of a video.
        """
        pass

    # TODO: audio frames t (?)
        
class _AudioSource(ABC):
    """
    Abstract class that is a media source
    containing audio information.
    """

    @property
    @abstractmethod
    def copy(
        self
    ):
        """
        Get a copy of this video source instance.
        """
        pass

    @property
    @abstractmethod
    def is_unchanged(
        self
    ) -> bool:
        """
        *For internal use only*

        Internal boolean flag to indicate if the source has
        been modified (or not), useful when we want to 
        optimize the way we access to the frames to render.

        If the original source has not been modified, we
        don't need to read frame by frame and apply any
        change so we can do it faster.

        (!) This property has to be modified by the specific
        audio sources.
        """
        pass

    @property
    @abstractmethod
    def duration(
        self
    ):
        """
        The duration of the source.
        """
        pass

    def __init__(
        self
    ):
        pass

    @abstractmethod
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction],
        do_apply_filters: bool = True
        # TODO: Return 'VideoFrame' or 'numpy' (?)
    ):
        """
        Get the audio frames that must be played
        during the 't' time moment of a video.
        """
        pass


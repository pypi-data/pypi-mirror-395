"""
Video sources, that are the source from
where we will obtain the data to offer
as video in our editor.

These sources will be used by other
classes to access to the frames but 
improve the functionality and simplify
it.
"""
from yta_editor.utils.alpha import _update_transparency
from yta_editor.utils import VideoUtils
from yta_editor.utils.frame_generator import VideoFrameGenerator
from yta_editor.sources.abstract import _VideoSource
from yta_time_interval import TIME_INTERVAL_SYSTEM_LIMITS
from yta_video_pyav.reader import VideoReader
from yta_video_pyav.reader.filter.dataclass import GraphFilter
from yta_validation.parameter import ParameterValidator
from av.video.frame import VideoFrame
from PIL import Image
from quicktions import Fraction
from typing import Union

import numpy as np


STATIC_VIDEO_DURATION = TIME_INTERVAL_SYSTEM_LIMITS[1]
"""
A constant value to indicate for the
videos that are built with static
frames (frames that never change like
images or colors).
"""

class VideoFileSource(_VideoSource):
    """
    Class to represent a video, read from a video
    file, as a video media source.

    You can apply effects directly to the source via
    ffmpeg filters.
    """

    @property
    def copy(
        self
    ) -> 'VideoFileSource':
        """
        Get a copy of this instance.
        """
        return VideoFileSource(
            filename = self.filename,
            video_filters = self._video_filters,
            audio_filters = self._audio_filters
        )
    
    @property
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

        The source is unchanged if there are no audio nor
        video filters.
        """
        return (
            len(self._audio_filters) == 0 and
            len(self._video_filters) == 0
        )

    @property
    def ticks_per_frame(
        self
    ) -> int:
        """
        The number of ticks per video frame. A
        tick is the minimum amount of time and
        is the way 'pts' is measured, in ticks.

        This means that the 'pts' value will
        be increased this amount from one video
        frame to the next one.

        How we obtain it:
        - `(1 / fps) / time_base`
        """
        return self.reader.ticks_per_frame
    
    @property
    def duration(
        self
    ) -> Fraction:
        """
        The duration of the video.
        """
        return self.reader.duration
    
    @property
    def number_of_frames(
        self
    ) -> Union[int, None]:
        """
        The number of frames of the video.
        """
        return self.reader.number_of_frames
    
    @property
    def fps(
        self
    ) -> Union[Fraction, None]:
        """
        The frames per second of the video.
        """
        return self.reader.fps
    
    @property
    def pixel_format(
        self
    ) -> Union[str, None]:
        """
        The pixel format.
        """
        return self.reader.pixel_format
    
    @property
    def audio_fps(
        self
    ) -> Union[int, None]:
        """
        The frames per second of the audio.
        """
        return self.reader.audio_fps

    @property
    def codec_name(
        self
    ) -> Union[str, None]:
        """
        The name of the video codec.
        """
        return self.reader.codec_name
    
    @property
    def audio_codec_name(
        self
    ) -> Union[str, None]:
        """
        The name of the audio codec.
        """
        return self.reader.audio_codec_name
    
    @property
    def audio_layout(
        self
    ) -> Union[str, None]:
        """
        The audio layout.
        """
        return self.reader.audio_layout
    
    @property
    def audio_format(
        self
    ) -> Union[str, None]:
        """
        The audio format.
        """
        return self.reader.audio_format

    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the video frames expressed 
        like (width, height).
        """
        return self.reader.size
    
    @property
    def width(
        self
    ) -> int:
        """
        The width of the video frames in pixels.
        """
        return self.size[0]
    
    @property
    def height(
        self
    ) -> int:
        """
        The height of the video frames in pixels.
        """
        return self.size[1]
    
    @property
    def time_base(
        self
    ) -> Union[Fraction, None]:
        """
        The time base of the video.
        """
        return self.reader.time_base
    
    @property
    def audio_time_base(
        self
    ) -> Union[Fraction, None]:
        """
        The time base of the audio.
        """
        return self.reader.audio_time_base

    def __init__(
        self,
        filename: str,
        video_filters: list[GraphFilter] = [],
        audio_filters: list[GraphFilter] = []
    ):
        # TODO: Validate the 'filename' is actually
        # a valid and readable video file

        self.filename: str = filename
        """
        The filename of the original video.
        """
        # TODO: Detect the 'pixel_format' from the
        # extension (?)
        self.reader: VideoReader = VideoReader(
            filename = self.filename,
            video_filters = video_filters,
            audio_filters = audio_filters
        )
        """
        The pyav video reader.
        """
        self._video_filters = []
        """
        The filters we want to apply to each video
        frame.
        """
        self._audio_filters = []
        """
        The filters we want to apply to each audio
        frame.
        """

        self.set_video_filters(video_filters)
        self.set_audio_filters(audio_filters)

    def set_video_filters(
        self,
        filters: list[GraphFilter]
    ) -> 'VideoFileSource':
        """
        Set the 'filters' provided as the new video
        filters, replacing the previous one if 
        existing.
        """
        ParameterValidator.validate_mandatory_list_of_these_instances('filters', filters, GraphFilter)

        self._video_filters = filters
        self.reader.set_video_filters(self._video_filters)

        return self

    def add_video_filter(
        self,
        filter: GraphFilter
    ) -> 'VideoFileSource':
        """
        Add a video filter to the list of filters
        to apply.
        """
        ParameterValidator.validate_mandatory_instance_of('filter', filter, GraphFilter)

         # TODO: Maybe handle repeated ones (?)
        self._video_filters.append(filter)

        return self
    
    def set_audio_filters(
        self,
        filters: list[GraphFilter]
    ) -> 'VideoFileSource':
        """
        Set the 'filters' provided as the new audio
        filters, replacing the previous one if 
        existing.
        """
        ParameterValidator.validate_mandatory_list_of_these_instances('filters', filters, GraphFilter)

        self._audio_filters = filters
        self.reader.set_audio_filters(self._audio_filters)

        return self
    
    def add_audio_filter(
        self,
        filter: GraphFilter
    ) -> 'VideoFileSource':
        """
        Add an audio filter to the list of filters
        to apply.
        """
        ParameterValidator.validate_mandatory_instance_of('filter', filter, GraphFilter)

         # TODO: Maybe handle repeated ones (?)
        self._audio_filters.append(filter)

        return self

    def get_video_frame_at(
        self,
        t: Union[int, float, Fraction],
        # This 'size' is actually handled with the
        # video filters, but I need it because of
        # the abstractmethod declaration
        size: Union[tuple[int, int], None] = None,
        do_apply_filters: bool = True
    ) -> VideoFrame:
        """
        Get the video frame with the given 't' time
        moment, using the video cache system, read
        from the file.
        """
        return self.reader.get_frame(
            t = t,
            do_apply_filters = do_apply_filters
        )
    
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction] = None,
        do_apply_filters: bool = True
    ):
        """
        Get the audio frames for the given 't' time
        moment of the video using the audio frame
        cache.
        """
        # TODO: Refactor to 'get_audio_frames_at' en su librería
        return self.reader.get_audio_frames_at_t(
            t = t,
            video_fps = video_fps,
            do_apply_filters = do_apply_filters
        )

class VideoImageSource(_VideoSource):
    """
    Class to represent a video, made from an
    image, as a video media source.

    This source is static. The same video
    frame will be returned always.
    """

    @property
    def copy(
        self
    ) -> 'VideoImageSource':
        """
        Get a copy of this instance.
        """
        return VideoImageSource(
            filename = self.filename,
            do_include_alpha = self._do_include_alpha,
            frame_format = self._frame_format,
            audio_fps = self.audio_fps,
            audio_samples_per_frame = self.audio_samples_per_frame
        )
    
    @property
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
        """
        return True

    @property
    def duration(
        self
    ) -> float:
        """
        The duration of the source.
        """
        return STATIC_VIDEO_DURATION
    
    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the original image, before resizing
        nor converting it, expressed as (width, height).
        """
        return self._original_image.size
    
    @property
    def _original_image(
        self
    ) -> Image.Image:
        """
        The original image as it was read from the
        file without resizing nor modifying it, as
        a pillow image.
        """
        if not hasattr(self, '__original_image'):
            self.__original_image = read_image(
                filename = self.filename,
                do_include_alpha = self._do_include_alpha
            )

        return self.__original_image
    
    def __init__(
        self,
        filename: str,
        do_include_alpha: bool = True,
        frame_format: str = 'rgba',
        audio_fps: int = 44_100,
        audio_samples_per_frame: int = 1024,
    ):
        """
        If the 'size' parameter is None, the image
        size will be used as the video size. If it
        is provided, the video frames will be 
        resized to fit the value provided.

        The 'audio_fps' and 'audio_samples_per_frame'
        are needed to generate the silent frames,
        and their values must match the ones in the
        general editor Timeline.
        """
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)
        # TODO: Validate 'filename' is a valid
        # and readable image file

        self.filename: str = filename
        """
        The filename of the original image.
        """
        self._do_include_alpha: bool = do_include_alpha
        """
        The internal flag to indicate if we
        want to consider the alpha channel or
        not.
        """
        self._frame_format: str = frame_format
        """
        The frame format we want to apply.
        """
        self.audio_fps: int = audio_fps
        """
        The fps (or sample rate) of the audio.
        """
        self.audio_samples_per_frame: int = audio_samples_per_frame
        """
        The amount of samples per audio frame.
        """

    def get_frame(
        self,
        size: Union[tuple[int, int], None]
    ) -> VideoFrame:
        """
        Get a frame with the expected 'size'. This method
        uses an internal cache to avoid generating again
        frames with the same size than the last one it was
        requested.
        """
        size = (
            self.size
            if size is None else
            size
        )

        self._last_call_frame_size = (
            size
            if not hasattr(self, '_last_call_frame_size') else
            self._last_call_frame_size
        )

        self._last_call_frame = (
            # We return a copy to avoid modifying the
            # original once it's been sent
            VideoFrame.from_ndarray(
                array = np.array(
                    self._original_image.resize(size, Image.LANCZOS)
                    if size != self._original_image.size else
                    self._original_image
                ),
                format = self._frame_format
            ) if (
                not hasattr(self, '_last_call_frame') or
                self._last_call_frame_size != size
            ) else
            self._last_call_frame
        )

        return VideoUtils.video.frame.copy(self._last_call_frame)

    def get_video_frame_at(
        self,
        t: Union[int, float, Fraction],
        size: Union[tuple[int, int], None] = None,
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ) -> VideoFrame:
        """
        Get the video frame with the given 't' time
        moment.
        """
        # TODO: I keep this method to have the same
        # in all the clases, but it makes no sense
        # because it is the property itself and the
        # 't' parameter is ignored
        return self.get_frame(size)
    
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction] = None,
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ):
        """
        Get the audio frames for the given 't' time
        moment of the video using the audio frame
        cache.
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults

        for frame in TimelineDefaults().audio_empty:
            yield frame._frame
    
class VideoColorSource(_VideoSource):
    """
    Class to represent a video, made from a
    static color, as a video media source.

    This source is static. The same video
    frame will be returned always.
    """

    @property
    def copy(
        self
    ) -> 'VideoColorSource':
        """
        Get a copy of this instance.
        """
        return VideoColorSource(
            color = self._color,
            size = self.size,
            frame_format = self._frame_format,
            transparency = self._transparency,
            audio_fps = self.audio_fps,
            audio_samples_per_frame = self.audio_samples_per_frame
        )
    
    @property
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
        """
        return True

    @property
    def duration(
        self
    ) -> float:
        """
        The duration of the source.
        """
        return STATIC_VIDEO_DURATION
    
    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the original source, expressed
        as (width, height).
        """
        return self._size
    
    @property
    def output_size(
        self
    ) -> tuple[int, int]:
        """
        The size of the video frame once its been
        resized, if needed, and generated for the
        video.
        """
        return self.size

    def __init__(
        self,
        color: Union[tuple[int, int, int], tuple[int, int, int, int]],
        size: tuple[int, int] = (1920, 1080),
        frame_format: str = 'rgba',
        transparency: Union[float, None] = 1.0,
        audio_fps: int = 44_100,
        audio_samples_per_frame: int = 1024,
    ):
        """
        The `color` must be a tuple of 3 (RGB) or 4
        (RGBA) values between 0 and 255.

        The `transparency` must be a float between
        `0.0` (opaque) and `1.0` (transparent).
        """
        self._color: Union[tuple[int, int, int], tuple[int, int, int, int]] = color
        """
        The color that will be used to make the
        frame that will be played its whole
        duration.
        """
        self._size: tuple[int, int] = size
        """
        The size of the media frame requested by
        the user.
        """
        self._frame_format: str = frame_format
        """
        The frame format we want to apply.
        """

        # We need to check that the transparency
        # is according to the frame format
        transparency = _update_transparency(
            transparency = transparency,
            format = frame_format
        )

        self._transparency: Union[float, None] = transparency
        """
        The transparency we want to apply if the
        frame format provided accepts transparency.
        """
        self.audio_fps: int = audio_fps
        """
        The fps (or sample rate) of the audio.
        """
        self.audio_samples_per_frame: int = audio_samples_per_frame
        """
        The amount of samples per audio frame.
        """

    def get_frame(
        self,
        size: Union[tuple[int, int], None]
    ) -> VideoFrame:
        """
        Get a frame with the expected 'size'. This method
        uses an internal cache to avoid generating again
        frames with the same size than the last one it was
        requested.
        """
        size = (
            self._size
            if size is None else
            size
        )

        self._last_call_frame_size = (
            size
            if not hasattr(self, '_last_call_frame_size') else
            self._last_call_frame_size
        )

        self._last_call_frame = (
            # We return a copy to avoid modifying the
            # original once it's been sent
            VideoFrameGenerator.background._full_custom(
                color = self._color,
                size = self._last_call_frame_size,
                transparency = self._transparency
            ) if (
                not hasattr(self, '_last_call_frame') or
                self._last_call_frame_size != size
            ) else
            self._last_call_frame
        )

        return VideoUtils.video.frame.copy(self._last_call_frame)

    def get_video_frame_at(
        self,
        t: Union[int, float, Fraction],
        size: Union[tuple[int, int], None] = None,
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ) -> VideoFrame:
        """
        Get the video frame with the given 't' time
        moment.
        """
        # TODO: I keep this method to have the same
        # in all the clases, but it makes no sense
        # because it is the property itself and the
        # 't' parameter is ignored
        return self.get_frame(size)
    
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction] = None,
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ):
        """
        Get the audio frames for the given 't' time
        moment of the video using the audio frame
        cache.
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults

        for frame in TimelineDefaults().audio_empty:
            yield frame._frame
    
class VideoNumpySource(_VideoSource):
    """
    Class to represent a video, made from a
    numpy array, as a video media source.

    This source is static. The same video
    frame will be returned always.
    """

    @property
    def copy(
        self
    ) -> 'VideoNumpySource':
        """
        Get a copy of this instance.
        """
        return VideoNumpySource(
            array = self._array,
            fps = self.fps,
            duration = self.duration
        )
    
    @property
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
        """
        return True

    @property
    def duration(
        self
    ) -> float:
        """
        The duration of the source.
        """
        return STATIC_VIDEO_DURATION
    
    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the video frame, expressed as
        (width, height).
        """
        return (self.frame.width, self.frame.height)

    # TODO: Put some information about the
    # shape we need to pass, and also create
    # a 'size' property with the size of the
    # array
    @property
    def frame(
        self
    ) -> VideoFrame:
        """
        The frame that must be displayed.
        """
        # By default we use it accepting transparency
        # TODO: The image must be like this:
        # arr = np.array(img)  # shape (h, w, 4), dtype=uint8
        # TODO: What value if no alpha (?)
        return VideoFrame.from_ndarray(
            array = self._array,
            format = 'rgba'
        )

    def __init__(
        self,
        array: np.ndarray,
        fps: Union[int, float, Fraction] = 60,
        duration: Union[int, float, Fraction] = 1,
        audio_fps: int = 44_100,
        audio_samples_per_frame: int = 1024,
    ):
        self._array: np.ndarray = array
        """
        The array of information that will be
        used to make the frame that will be
        played its whole duration.
        """
        self.fps: Fraction = Fraction(fps)
        """
        The frames per second of this video source.
        """
        self.duration: Fraction = Fraction(duration)
        """
        The duration of this video source.
        """
        self.audio_fps: int = audio_fps
        """
        The fps (or sample rate) of the audio.
        """
        self.audio_samples_per_frame: int = audio_samples_per_frame
        """
        The amount of samples per audio frame.
        """

    def get_video_frame_at(
        self,
        t: Union[int, float, Fraction],
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ) -> VideoFrame:
        """
        Get the video frame with the given 't' time
        moment.
        """
        # TODO: I keep this method to have the same
        # in all the clases, but it makes no sense
        # because it is the property itself and the
        # 't' parameter is ignored
        return self.frame
    
    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction] = None,
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ):
        """
        Get the audio frames for the given 't' time
        moment of the video using the audio frame
        cache.
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults

        for frame in TimelineDefaults().audio_empty:
            yield frame._frame

    


# TODO: I think I have this util in another
# library, so please check it...
def read_image(
    filename: str,
    do_include_alpha: bool = True
) -> Image.Image:
    """
    Read the image file 'filename' with or without
    the alpha channel according to the 
    'do_include_alpha' parameter provided.
    """
    mode = (
        'RGBA'
        if do_include_alpha else
        'RGB'
    )

    return Image.open(filename).convert(mode)

def image_to_numpy_pillow(
    filename: str,
    do_include_alpha: bool = True,
    size: Union[tuple[int, int], None] = None
) -> 'np.ndarray':
    """
    Read the imagen file 'filename' and transform
    it into a numpy, reading also the alpha channel.

    If the 'size' parameter is None, the original
    size will be preserved. If no, it will be resized
    using the pillow LANCZOS resize method.
    """
    image = read_image(
        filename = filename,
        do_include_alpha = do_include_alpha
    )

    image = (
        image.resize(size, Image.LANCZOS)
        if size is not None else
        image
    )

    return np.array(image) 

"""
The pyav uses Pillow to load an image as
a numpy array but using not the alpha.
"""
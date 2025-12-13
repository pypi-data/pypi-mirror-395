from yta_editor.media.abstract import _Media
from yta_editor.sources.abstract import _VideoSource
from yta_editor.sources.video import VideoFileSource, VideoImageSource, VideoColorSource, VideoNumpySource
# from yta_editor.utils.effects import apply_audio_effects_to_frame_at, apply_video_effects_to_frame_at
from yta_video_frame_time.t_fraction import get_ts, fps_to_time_base, T
from yta_video_pyav.writer import VideoWriter
from yta_video_pyav.settings import Settings
from yta_video_pyav.reader.filter.dataclass import GraphFilter, GraphFilters
from yta_editor_nodes.timeline.serial import SerialNode
from yta_editor_nodes.timeline.parallel import ParallelNode
from yta_editor_nodes.timeline.utils import validate_is_edition_node
from yta_validation.parameter import ParameterValidator
from yta_colors import Color
from av.video.frame import VideoFrame
from quicktions import Fraction
from typing import Union

import copy

    
class _VideoMedia(_Media):

    @property
    def is_unchanged(
        self
    ) -> bool:
        """
        *For internal use only*

        Internal boolean flag to indicate if the media has
        been modified (or not), useful when we want to 
        optimize the way we access to the frames to render.

        If the original source has not been modified, we
        don't need to read frame by frame and apply any
        change so we can do it faster.

        The media is unchanged if the source is unchanged
        and there are no audio effects to apply.
        """
        return (
            super().is_unchanged and
            len(self._audio_effects) == 0 and
            len(self._video_effects) == 0
        )

    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the original source, expressed
        as (width, height). Check the 'output_size'
        to know the size requested by the user to
        be the size of each video frame.
        """
        return self.source.size
    
    def __init__(
        self,
        source: _VideoSource,
        t_start: Union[int, float, Fraction] = 0.0,
        t_end: Union[int, float, Fraction, None] = None,
        size: Union[tuple[int, int], None] = None,
        video_effects: list[Union['SerialNode', 'ParallelNode']] = [],
        audio_effects: list[Union['SerialNode', 'ParallelNode']] = []
    ):
        self._video_effects: list['SerialNode', 'ParallelNode'] = video_effects
        """
        The video effects we want to apply on the media.
        """

        super().__init__(
            source = source,
            t_start = t_start,
            t_end = t_end,
            audio_effects = audio_effects
        )

        self.output_size: tuple[int, int] = None
        """
        The size we expect to be used as the
        output size. It can be different from
        the original vide source size.
        """

        self.set_output_size(
            self.size
            if size is None else
            size
        )

    def set_output_size(
        self,
        output_size: tuple[int, int]
    ) -> 'VideoFileMedia':
        """
        Set the desired size for the output, that
        means the video frames when rendering. This
        method will also update the scaling filter.
        """
        self.output_size = output_size

    def add_video_effect(
        self,
        effect: Union['SerialNode', 'ParallelNode']
    ) -> 'VideoFileMedia':
        """
        Add the provided video `effect` to the list to apply
        to this media.
        """
        # TODO: Validate that it is actually a video effect
        # inside the `effect`
        validate_is_edition_node(effect)

        self._video_effects.append(effect)

        return self
    
    def set_video_effects(
        self,
        effects: list[Union['SerialNode', 'ParallelNode']]
    ) -> 'VideoFileMedia':
        """
        Set the provided video `effects` as the effects to
        apply to this media, replacing the previous ones.
        """
        # TODO: Validate that it is actually a list of video
        # effects inside the `effects`
        self._video_effects = effects

        return self
    
    def get_video_frame_with_t_source(
        self,
        t_source: Union[int, float, Fraction],
        do_apply_filters: bool = True
    ) -> Union[VideoFrame, None]:
        """
        Get the video frame with the given `t_source`
        source time moment, using the video cache system.

        The `t_source` time moment must be a value in the
        time interval `[0, source.t_end]`, that will be
        used directly to be read from the source.
        """
        ParameterValidator.validate_mandatory_number_between('t_source', t_source, 0, self.source.duration, True, False)

        print(f'Getting frame from "t_source={str(float(t_source))}".')

        frame = self.source.get_video_frame_at(
            t = t_source,
            # TODO: Fix the 'output_size'
            size = self.output_size,
            do_apply_filters = do_apply_filters
        )

        return (
            # TODO: Effects must be now applied with nodes
            # apply_video_effects_to_frame_at(
            #     effects_stack = self._video_effects,
            #     frame = frame,
            #     t = t
            # )
            frame
            if frame is not None else
            None
        )

    # @with_t_adjusted_to_source
    def get_video_frame_at(
        self,
        t_media: Union[int, float, Fraction],
        do_apply_filters: bool = True,
        do_use_source_limits: bool = False
    ) -> Union[VideoFrame, None]:
        """
        Get the video frame with the given 't_media'
        time moment, using the video cache system.

        The `t_media` time moment must be a value
        between 0 and the media duration, that will
        be transformed into the corresponding source
        time moment to be read.

        The `do_use_source_limits` parameter will make
        the video accept a `t_media` value that is
        beyond the time interval limits of that media
        but inside the source time interval limits
        (useful when accessing frames for transitions).
        """
        t_source = self._t_media_to_t_source(
            t_media = t_media,
            do_use_source_limits = do_use_source_limits
        )
        
        print(f'Getting frame from "t_media={str(float(t_media))}" that is actually "t_source={str(float(t_source))}"')

        return self.get_video_frame_with_t_source(
            t_source = t_source,
            do_apply_filters = do_apply_filters
        )
    
    def get_audio_frames_with_t_source(
        self,
        t_source: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction, None] = None,
        do_apply_filters: bool = True
    ):
        """
        Get the sequence of audio frames for the given 
        source `t_source` time moment, using the audio
        cache system.

        The `t_source` time moment must be a value in the
        time interval `[0, source.t_end]`, that will be
        used directly to be read from the source.
        """
        ParameterValidator.validate_mandatory_number_between('t_source', t_source, 0, self.source.duration, True, False)

        video_fps = (
            self.fps
            if video_fps is None else
            video_fps
        )

        print(f'Getting audio frames from "t_source={str(float(t_source))}"')

        for frame in self.source.get_audio_frames_at(
            t = t_source,
            video_fps = video_fps,
            do_apply_filters = do_apply_filters
        ):
            # TODO: We don't apply the effects like this anymore
            # yield apply_audio_effects_to_frame_at(
            #     effects_stack = self._audio_effects,
            #     frame = frame,
            #     t = t
            # )
            yield frame
        
    # @with_t_adjusted_to_source
    def get_audio_frames_at(
        self,
        t_media: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction, None] = None,
        do_apply_filters: bool = True,
        do_use_source_limits: bool = False
    ):
        """
        Get the sequence of audio frames for the 
        given video 't' time moment, using the
        audio cache system.

        The `t` time moment must be a value between
        0 and the media duration, that will be
        transformed into the corresponding source
        time moment to be read.

        This is useful when we want to write a
        video frame with its audio, so we obtain
        all the audio frames associated to it
        (remember that a video frame is associated
        with more than 1 audio frame).

        The `do_use_source_limits` parameter will make
        the video accept a `t_media` value that is
        beyond the time interval limits of that media
        but inside the source time interval limits
        (useful when accessing frames for transitions).
        """
        t_source = self._t_media_to_t_source(
            t_media = t_media,
            do_use_source_limits = do_use_source_limits
        )
        
        print(f'Getting audio frames from "t_media={str(float(t_media))}" that is actually "t_source={str(float(t_source))}"')

        return self.get_audio_frames_with_t_source(
            t_source = t_source,
            video_fps = video_fps,
            do_apply_filters = do_apply_filters
        )

    def save_as(
        self,
        output_filename: str,
        video_size: tuple[int, int] = None,
        video_fps: float = None,
        video_codec: str = None,
        video_pixel_format: str = None,
        audio_codec: str = None,
        audio_sample_rate: int = None,
        audio_layout: str = None,
        audio_format: str = None,
        do_apply_video_filters: bool = True,
        do_apply_audio_filters: bool = True
    ) -> str:
        """
        Save the file as 'output_filename'.

        This method is useful if you want to apply
        some filter and then save the video with
        those filters applied into a new one, maybe
        with a new pixel format and/or code. You can
        prepare alpha transitions, etc.
        """
        video_size = (
            getattr(self, 'size', Settings.DEFAULT_VIDEO_SIZE.value)
            if video_size is None else
            video_size
        )

        video_fps = (
            getattr(self, 'fps', Settings.DEFAULT_VIDEO_FPS.value)
            if video_fps is None else
            video_fps
        )

        video_codec = (
            getattr(self, 'codec_name', Settings.DEFAULT_VIDEO_CODEC.value)
            if video_codec is None else
            video_codec
        )

        video_pixel_format = (
            getattr(self, 'pixel_format', Settings.DEFAULT_PIXEL_FORMAT.value)
            if video_pixel_format is None else
            video_pixel_format
        )

        audio_codec = (
            getattr(self, 'audio_codec_name', Settings.DEFAULT_AUDIO_CODEC.value)
            if audio_codec is None else
            audio_codec
        )

        audio_sample_rate = (
            getattr(self, 'audio_fps', Settings.DEFAULT_AUDIO_FPS.value)
            if audio_sample_rate is None else
            audio_sample_rate
        )

        audio_layout = (
            getattr(self, 'audio_layout', Settings.DEFAULT_AUDIO_LAYOUT.value)
            if audio_layout is None else
            audio_layout
        )

        audio_format = (
            getattr(self, 'audio_format', Settings.DEFAULT_AUDIO_FORMAT.value)
            if audio_format is None else
            audio_format
        )

        writer = VideoWriter(output_filename)

        # TODO: This has to be dynamic according to the
        # video we are writing (?)
        writer.set_video_stream(
            codec_name = video_codec,
            fps = video_fps,
            size = video_size,
            pixel_format = video_pixel_format
        )
        
        writer.set_audio_stream(
            codec_name = audio_codec,
            fps = audio_sample_rate,
            layout = audio_layout,
            format = audio_format
        )

        # TODO: Maybe we need to reformat or something
        # if some of the values changed, such as fps,
        # audio sample rate, etc. (?)

        time_base = fps_to_time_base(video_fps)
        audio_time_base = fps_to_time_base(audio_sample_rate)

        for t in get_ts(0, self.t_end, video_fps):
            frame = self.get_video_frame_at(
                t = t,
                do_apply_filters = do_apply_video_filters
            )

            # TODO: What if 'frame' is None (?)
            if frame is None:
                print(f'   [ERROR] Frame not found at t:{float(t)}')
                continue

            writer.mux_video_frame(
                frame = frame
            )

            frame.time_base = time_base
            frame.pts = T(t, time_base).truncated_pts

            audio_pts = 0
            for audio_frame in self.get_audio_frames_at(
                t = t,
                video_fps = video_fps,
                do_apply_filters = do_apply_audio_filters,
                # TODO: Should this be True (?)
                do_use_source_limits = True
            ):
                # TODO: 'audio_frame' could be None or []
                # here if no audio channel
                if audio_frame is None:
                    # TODO: Generate silence audio to cover the
                    # whole video frame (?)
                    pass
                
                # We need to adjust our output elements to be
                # consecutive and with the right values
                # TODO: We are using int() for fps but its float...
                audio_frame.time_base = audio_time_base
                audio_frame.pts = audio_pts

                # We increment for the next iteration
                audio_pts += audio_frame.samples

                writer.mux_audio_frame(audio_frame)

        writer.mux_video_frame(None)
        writer.mux_audio_frame(None)
        writer.output.close()

        return output_filename
    
class VideoFileMedia(_VideoMedia):
    """
    A video media that is read from a video
    file and can be subclipped to a specific
    time range.
    """

    @property
    def copy(
        self
    ) -> 'VideoFileMedia':
        """
        Get a copy of this instance with the same
        source, time range and effects.
        """
        instance_copy = VideoFileMedia._init_with_source(
            source = self.source,
            t_start = self.t_start,
            t_end = self.t_end
        )

        # TODO: Is this working (?)
        instance_copy._video_effects = copy.deepcopy(self._video_effects)
        instance_copy._audio_effects = copy.deepcopy(self._audio_effects)

        return instance_copy

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
        return self.source.ticks_per_frame
    
    @property
    def number_of_frames(
        self
    ) -> Union[int, None]:
        """
        The number of frames of the video.
        """
        return self.source.number_of_frames
    
    @property
    def fps(
        self
    ) -> Union[Fraction, None]:
        """
        The frames per second of the video.
        """
        return self.source.fps
    
    @property
    def audio_fps(
        self
    ) -> Union[int, None]:
        """
        The frames per second of the audio.
        """
        return self.source.audio_fps
    
    @property
    def codec_name(
        self
    ) -> Union[str, None]:
        """
        The name of the video codec.
        """
        return self.source.codec_name
    
    @property
    def audio_codec_name(
        self
    ) -> Union[str, None]:
        """
        The name of the audio codec.
        """
        return self.source.audio_codec_name
    
    @property
    def audio_layout(
        self
    ) -> Union[str, None]:
        """
        The audio layout.
        """
        return self.source.audio_layout.name
    
    @property
    def audio_format(
        self
    ) -> Union[str, None]:
        """
        The audio format.
        """
        return self.source.audio_format.name
    
    @property
    def pixel_format(
        self
    ) -> Union[str, None]:
        """
        The pixel format.
        """
        return self.source.pixel_format

    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the video frames expressed 
        like (width, height).
        """
        return self.source.size
    
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
        return self.source.time_base
    
    @property
    def audio_time_base(
        self
    ) -> Union[Fraction, None]:
        """
        The time base of the audio.
        """
        return self.source.audio_time_base

    def __init__(
        self,
        filename: str,
        t_start: Union[int, float, Fraction] = 0.0,
        t_end: Union[int, float, Fraction, None] = None,
        size: Union[tuple[int, int], None] = None,
        # These are ffmpeg filters
        video_effects: list['SerialNode', 'ParallelNode'] = [],
        audio_effects: list['SerialNode', 'ParallelNode'] = [],
        video_filters: list[GraphFilter] = [],
        audio_filters: list[GraphFilter] = []
    ):
        """
        If the `t_end` parameter is not provided, the duration
        of the file source will be used.
        """
        # We first create the source with no
        # filters just to be able to know the
        # original size and properties
        source = VideoFileSource(
            filename = filename,
            video_filters = video_filters,
            audio_filters = audio_filters
        )

        t_end = (
            source.duration
            if t_end is None else
            t_end
        )

        super().__init__(
            source = source,
            t_start = t_start,
            t_end = t_end,
            size = size,
            video_effects = video_effects,
            audio_effects = audio_effects
        )
        
    # This is special, we need it as a filter
    def set_output_size(
        self,
        output_size: tuple[int, int]
    ) -> 'VideoFileMedia':
        """
        Set the desired size for the output, that
        means the video frames when rendering. This
        method will also update the scaling filter.
        """
        self.output_size = output_size
        
        if self.size != self.output_size:
            # We need to apply a resize (scale) pyav
            # filter to obtain the desired output size
            self._set_scale_filter(self.output_size)

        return self

    # TODO: Do we need this in the source instead (?)
    def _set_scale_filter(
        self,
        size: tuple[int, int]
    ) -> 'VideoFileMedia':
        """
        Set the scale 'filter' provided replacing
        any other previous scale filter set in this
        class. This is a filter that will be applied
        directly on the source to force the input to
        be read with a specific size (scaled) through
        the ffmpeg reader.
        """
        # Remove previous 'scale' filter if existing
        self.set_video_filters(
            [
                video_filter
                for video_filter in self.source._video_filters
                if video_filter.name != 'scale'
            ]
        )

        self.add_video_filter(GraphFilters.video.scale(size[0], size[1]))

        return self
    
    def add_video_filter(
        self,
        filter: GraphFilter
    ) -> 'VideoFileMedia':
        """
        Add a video filter to the list of filters
        to apply.
        """
        self.source.add_video_filter(filter)

        return self
    
    def set_video_filters(
        self,
        filters: list[GraphFilter] = []
    ) -> 'VideoFileMedia':
        """
        Set the 'filters' provided as the new video
        filters, replacing the previous one if 
        existing.
        """
        # TODO: What if 'audio' filters coming (?)
        self.source.set_video_filters(filters)

        return self
    
    def add_audio_filter(
        self,
        filter: GraphFilter
    ) -> 'VideoFileMedia':
        """
        Add an audio filter to the list of filters
        to apply.
        """
        self.source.add_audio_filter(filter)

        return self
    
    def set_audio_filters(
        self,
        filters: list[GraphFilter] = []
    ) -> 'VideoFileMedia':
        """
        Set the 'filters' provided as the new audio
        filters, replacing the previous one if 
        existing.
        """
        # TODO: What if 'video' filters coming (?)
        self.source.set_audio_filters(filters)

        return self

class VideoImageMedia(_VideoMedia):
    """
    A video media that is made by an static
    image file.
    """

    @property
    def copy(
        self
    ) -> 'VideoImageMedia':
        """
        Get a copy of this instance with the same
        source, time range and effects.
        """
        instance_copy = VideoImageMedia._init_with_source(
            source = self.source,
            t_start = self.t_start,
            t_end = self.t_end
        )

        # TODO: Is this working (?)
        instance_copy._video_effects = copy.deepcopy(self._video_effects)
        instance_copy._audio_effects = copy.deepcopy(self._audio_effects)

        return instance_copy

    @property
    def filename(
        self
    ) -> str:
        """
        The filename of the original image.
        """
        return self.source.filename

    # TODO: Maybe rename this property (?)
    @property
    def do_include_alpha(
        self
    ) -> bool:
        """
        The internal flag to indicate if we
        want to consider the alpha channel or
        not.
        """
        return self.source._do_include_alpha
    
    def __init__(
        self,
        filename: str,
        duration: Union[int, float, Fraction],
        do_include_alpha: bool = True,
        size: Union[tuple[int, int], None] = None,
        # Need this to generate the silent audio frames
        audio_fps: int = 44_100,
        audio_samples_per_frame: int = 1024,
        video_effects: list['SerialNode', 'ParallelNode'] = [],
        audio_effects: list['SerialNode', 'ParallelNode'] = []
    ):
        """
        TODO: Maybe force size provided as parameter (?)
        """
        # We need to dynamically set the frame format
        # to accept (or not) the alpha channel
        frame_format = (
            'rgba'
            if do_include_alpha else
            'rgb24'
        )

        super().__init__(
            source = VideoImageSource(
                filename = filename,
                do_include_alpha = do_include_alpha,
                frame_format = frame_format,
                audio_fps = audio_fps,
                audio_samples_per_frame = audio_samples_per_frame,
            ),
            t_start = 0,
            t_end = duration,
            size = size,
            video_effects = video_effects,
            audio_effects = audio_effects
        )

class VideoColorMedia(_VideoMedia):
    """
    A video media that is made with a static
    uniform color frame.
    """

    @property
    def copy(
        self
    ) -> 'VideoColorMedia':
        """
        Get a copy of this instance with the same
        source, time range and effects.
        """
        instance_copy = VideoColorMedia._init_with_source(
            source = self.source,
            t_start = self.t_start,
            t_end = self.t_end
        )

        # TODO: Is this working (?)
        instance_copy._video_effects = copy.deepcopy(self._video_effects)
        instance_copy._audio_effects = copy.deepcopy(self._audio_effects)

        return instance_copy
    
    @property
    def color(
        self
    ) -> tuple[int, int, int]:
        """
        The color that will be used to make the
        frame that will be played its whole
        duration.
        """
        return self.source._color
    
    @property
    def size(
        self
    ) -> tuple[int, int]:
        """
        The size of the media frame.
        """
        return self.source.size

    def __init__(
        self,
        color: Color,
        duration: Union[int, float, Fraction],
        size: tuple[int, int] = (1920, 1080),
        transparency: Union[float, None] = 0.0,
        # TODO: Should we accept 'frame_format' (?)
        #frame_format: str = 'rgba',
        # Need this to generate the silent audio frames
        audio_fps: int = 44_100,
        audio_samples_per_frame: int = 1024,
        video_effects: list['SerialNode', 'ParallelNode'] = [],
        audio_effects: list['SerialNode', 'ParallelNode'] = [],
    ):
        # TODO: What about the 'transparency' if they
        # provide a 'color' also with 'transparency' (?)
        color = Color.parse(color)

        frame_format = (
            'rgba'
            if transparency is not None else
            'rgb24'
        )

        super().__init__(
            source = VideoColorSource(
                color = color.rgb_not_normalized,
                size = size,
                frame_format = frame_format,
                transparency = transparency,
                audio_fps = audio_fps,
                audio_samples_per_frame = audio_samples_per_frame,
            ),
            t_start = 0,
            t_end = duration,
            size = size,
            video_effects = video_effects,
            audio_effects = audio_effects
        )

# TODO: Create 'VideoNumpyMedia'
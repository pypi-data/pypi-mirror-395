from yta_editor.media.abstract import _Media
from yta_editor.sources.abstract import _AudioSource
from yta_editor.sources.audio import AudioFileSource, AudioNumpySource
# from yta_editor.utils.effects import apply_audio_effects_to_frame_at
from yta_video_pyav.reader.filter.dataclass import GraphFilter
from quicktions import Fraction
from typing import Union

import copy


class _AudioMedia(_Media):
    """
    Abstract class to be inherited by any
    media element.

    The media element is an element that
    includes a source and a 't_start' and
    't_end' values to be able to subclip that
    media source and use only the part we
    want to use.
    """

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
            len(self._audio_effects) == 0
        )

    def __init__(
        self,
        source: _AudioSource,
        t_start: Union[int, float, Fraction] = 0.0,
        t_end: Union[int, float, Fraction, None] = None,
        audio_effects: list['SerialNode', 'ParallelNode'] = []
    ):
        super().__init__(
            source = source,
            t_start = t_start,
            t_end = t_end,
            audio_effects = audio_effects
        )

    def get_audio_frames_with_t_source(
        self,
        t_source: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction]
    ):
        """
        Get the sequence of audio frames for a 
        given video 't_source' time moment, using
        the audio cache system.

        The `t_source` time moment must be a value in
        the time interval `[0, source.t_end]`, that will
        be used directly to be read from the source.

        This is useful when we want to write a
        video frame with its audio, so we obtain
        all the audio frames associated to it
        (remember that a video frame is associated
        with more than 1 audio frame).
        """
        from yta_validation.parameter import ParameterValidator

        ParameterValidator.validate_mandatory_number_between('t_source', t_source, 0, self.source.duration, True, False)

        print(f'Getting audio frames from "t_source={str(float(t_source))}"')
        
        for frame in self.source.get_audio_frames_at(t_source, video_fps):
            # TODO: Effects must be now applied with nodes
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
        video_fps: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ):
        """
        Get the sequence of audio frames for a 
        given video 't_media' time moment, using
        the audio cache system.

        The `t_media` time moment must be a value
        between 0 and the media duration, that will
        be transformed into the corresponding source
        time moment to be read.

        This is useful when we want to write a
        video frame with its audio, so we obtain
        all the audio frames associated to it
        (remember that a video frame is associated
        with more than 1 audio frame).
        """
        # TODO: Validate (?)
        t_source = self._t_media_to_t_source(
            t_media = t_media,
            do_use_source_limits = do_use_source_limits
        )

        print(f'Getting audio frames from "t_media={str(float(t_media))}" that is actually "t_source={str(float(t_source))}"')
        for frame in self.source.get_audio_frames_at(t_source, video_fps):
            # TODO: Effects must be now applied with nodes
            # yield apply_audio_effects_to_frame_at(
            #     effects_stack = self._audio_effects,
            #     frame = frame,
            #     t = t
            # )
            yield frame

class AudioFileMedia(_AudioMedia):
    """
    An audio media that is read from an audio
    file and can be subclipped to a specific
    time range.
    """

    @property
    def copy(
        self
    ) -> 'AudioFileMedia':
        """
        Get a copy of this instance with the same
        source, time range and effects.
        """
        instance_copy = AudioFileMedia._init_with_source(
            source = self.source,
            t_start = self.t_start,
            t_end = self.t_end,
            audio_effects = copy.deepcopy(self._audio_effects)
        )

        return instance_copy

    @property
    def audio_fps(
        self
    ) -> Union[int, None]:
        """
        The frames per second of the audio.
        """
        return self.source.audio_fps
    
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
        # These are ffmpeg filters
        audio_effects: list[Union['SerialNode', 'ParallelNode']] = [],
        audio_filters: list[GraphFilter] = []
    ):
        super().__init__(
            source = AudioFileSource(
                filename = filename,
                audio_filters = audio_filters
            ),
            t_start = t_start,
            t_end = t_end,
            audio_effects = audio_effects
        )

    def add_audio_filter(
        self,
        filter: GraphFilter
    ) -> 'AudioFileMedia':
        """
        Add an audio filter to the list of filters
        to apply.
        """
        self.source.add_audio_filter(filter)

        return self
    
    def set_audio_filters(
        self,
        filters: list[GraphFilter] = []
    ) -> 'AudioFileMedia':
        """
        Set the 'filters' provided as the new audio
        filters, replacing the previous one if 
        existing.
        """
        # TODO: What if 'video' filters coming (?)
        self.source.set_audio_filters(filters)

        return self

# TODO: Create 'AudioNumpyMedia'

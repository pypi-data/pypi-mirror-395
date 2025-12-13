"""
Note for the developers:
- All the media have, at least, audio, so we put
the audio effects array as a common one.
"""
from yta_editor_nodes.timeline.utils import validate_is_edition_node
from yta_validation.parameter import ParameterValidator
from yta_validation import PythonValidator
from yta_time_interval import TimeInterval
from quicktions import Fraction
from typing import Union
from abc import ABC, abstractmethod


class _Media(ABC):
    """
    Abstract class to be inherited by any media element.

    The media element is an element that includes a source
    and a pair of `t_start` and `t_end` values to be able to
    subclip that media source and use only the part we are
    interested in.

    A media will be always limited to the source duration,
    and the `t_start` and `t_end` time moments will be also
    limited to `0` and the duration of the source.
    """

    @property
    @abstractmethod
    def copy(
        self
    ) -> '_Media':
        """
        Get a copy of this instance with the same
        source, time range and effects.
        """
        pass

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

        (!) This property has to be modified by the specific
        video medias.
        """
        return (
            self.source.is_unchanged and
            self.head == 0 and
            self.tail == 0 and
            len(self._audio_effects) == 0
        )

    @property
    def head(
        self
    ) -> Fraction:
        """
        The time remaining at the begining of this
        Media source, which is the value between `0`
        and the `t_start` time moment.

        This value can be useful for transitions.

        The formula:
        - `self._time_interval.head`
        """
        return self._time_interval.head
    
    @property
    def tail(
        self
    ) -> Fraction:
        """
        The time remaining at the t_end of this Media
        source, which is the value between the `t_end`
        time moment and the total duration of the
        source.

        This value can be useful for transitions.

        The formula:
        - `self._time_interval.tail`
        """
        return self._time_interval.tail
    
    @property
    def t_start(
        self
    ) -> Fraction:
        """
        The time moment of the source in which this media
        should t_start being played.
        """
        return self._time_interval.t_start
    
    @property
    def t_end(
        self
    ) -> Fraction:
        """
        The time moment of the source in which this media
        should stop being played.
        """
        return self._time_interval.t_end
    
    @property
    def start_limit(
        self
    ) -> Fraction:
        """
        The lower time moment value that can be used to get
        the frame from the source. This value can be reached
        only if some boolean parameters are provided to force
        this limit, or the normal `[0, self.duration]` time
        interval should be used as the limit instead.

        If the media is pointing to the whole source duration,
        this limit will be `0`.
        """
        return -self.head

    @property
    def end_limit(
        self
    ) -> Fraction:
        """
        The upper time moment value that can be used to get
        the frame from the source. This value can be reached
        only if some boolean parameters are provided to force
        this limit, or the normal `[0, self.duration]` time
        interval should be used as the limit instead.

        If the media is pointing to the whole source duration,
        this limit will be `self.duration`.
        """
        return self.duration + self.tail
    
    @property
    def duration(
        self
    ) -> Fraction:
        """
        The duration of the media in this specific moment
        as it has been defined by the user (that could
        have modified it) according to the current `t_start`
        and `t_end` values.

        The formula:
        - `self._time_interval.duration`
        """
        return self._time_interval.duration
    
    @property
    def max_duration(
        self
    ) -> Fraction:
        """
        The maximum duration of the media, that is the
        duration of the file source (if existing) or the
        one defined when instantiating it.

        The formula:
        - `self._time_interval.t_end_limit`
        """
        return self._time_interval.t_end_limit

    def __init__(
        self,
        source: Union['AudioFileSource', 'AudioNumpySource', 'VideoFileSource', 'VideoColorSource', 'VideoImageSource', 'VideoNumpySource'],
        t_start: Union[int, float, Fraction] = 0.0,
        t_end: Union[int, float, Fraction, None] = None,
        audio_effects: list[Union['SerialNode', 'ParallelNode']] = [],
    ):
        self.source: Union['AudioFileSource', 'AudioNumpySource', 'VideoFileSource', 'VideoColorSource', 'VideoImageSource', 'VideoNumpySource'] = source
        """
        The source of this media element that is the entity
        from which we can obtain the frames.
        """
        self._audio_effects: list['SerialNode', 'ParallelNode'] = []
        """
        The audio effects we want to apply on the media.
        """
        if (
            not PythonValidator.is_instance_of(source, ['AudioFileSource', 'VideoFileSource']) and
            t_end is None
        ):
            raise Exception('The `t_end` parameter is mandatory when the source is not a video/audio file.')
        
        # TODO: Here we don't have `fps` to be able to use them,
        # but we will limit with all the limits as we know how
        # long can the media be
        end_limit = (
            self.source.duration
            if self.source.duration is not None else
            # TODO: What do we do with this? It can't be None...
            None
        )

        self._time_interval: TimeInterval = TimeInterval(
            t_start = t_start,
            t_end = t_end,
            t_start_limit = 0,
            t_end_limit = end_limit,
            duration_limit = end_limit,
            fps = None
        )
        """
        *For internal use only*

        Internal time interval to handle the duration and be
        able to limit it to the real source duration.
        """
        
        self.set_audio_effects(audio_effects)

    def shift_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_start` value by adding the `delta` provided
        (that can be positive to make it start later, or negative
        to make it start earlier), and also the `t_end` the same
        amount.

        This is useless when the media is pointing to the time
        interval `[2, 4)` of the source, for example, and we want
        to make it point to the `[3, 5)`. We can use a `shift_by(1)`
        in this case to achieve this purpose.
        """
        self._time_interval.shift_by(delta)

        return self
    
    def shift_to(
        self,
        t: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_start` value to the time moment provided as
        `t`, and also the `t_end` the same amount of time and in
        the same direction).

        This is useful when the media is pointing to the time
        interval `[2, 4)` of the source, for example, and we want
        to make it point to the `[3, 5)`. We can use a `shift_to(3)`
        in this case to achieve this purpose.
        """
        self._time_interval.shift_to(t)

        return self

    def shift_start_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_start` value by adding the `delta` provided
        (that can be positive to make it start later or negative
        to make it start earlier).
        """
        self._time_interval.shift_start_by(delta)

        return self
    
    def shift_start_to(
        self,
        t: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_start` value to the `t` time moment
        provided (that can be greater or smaller than the
        current `t_start`), if possible and valid.
        """
        self._time_interval.shift_start_to(t)

        return self
    
    def shift_end_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_end` value by adding the `delta` provided
        (that can be positive to make it end later or negative
        to make it end earlier).
        """
        self._time_interval.shift_end_by(delta)

        return self
    
    def shift_end_to(
        self,
        t: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Update the `t_end` value to the `t` time moment
        provided (that can be greater or smaller than the
        current `t_end`), if possible and valid.
        """
        self._time_interval.shift_end_to(t)

        return self
    
    def split(
        self,
        t: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Split the media by the `t` time moment provided
        and return the 2 new instances.
        """
        new_time_intervals = self._time_interval.split(t)

        left = self.copy
        right = self.copy

        left._time_interval.with_start_and_end(new_time_intervals[0].t_start, new_time_intervals[0].t_end)
        right._time_interval.with_start_and_end(new_time_intervals[1].t_start, new_time_intervals[1].t_end)

        return (
            left,
            right
        )
    
    def cut(
        self,
        t_start: Union[int, float, Fraction],
        t_end: Union[int, float, Fraction]
    ) -> '_Media':
        """
        Cut the media by the `t_start` and `t_end` time moments
        provided and get the new instance.
        """
        self._time_interval.cut(t_start, t_end)

        return self
    
    def add_audio_effect(
        self,
        effect: Union['SerialNode', 'ParallelNode']
    ) -> 'VideoFileMedia':
        """
        Add the provided audio `effect` to the list to apply
        to this media.
        """
        # TODO: Validate that it is actually an audio effect
        # inside the `effect`
        validate_is_edition_node(effect)

        self._audio_effects.append(effect)

        return self
    
    def set_audio_effects(
        self,
        effects: list[Union['SerialNode', 'ParallelNode']]
    ) -> 'VideoFileMedia':
        """
        Set the provided audio `effects` as the effects to
        apply to this media, replacing the previous ones.
        """
        # TODO: Validate that it is actually a list of audio
        # effects inside the `effects`
        self._audio_effects = effects

        return self
    
    # TODO: This method has been created
    # to be inherited by the other classes
    # and being able to copy the instance
    # properly by using the same 'source'
    # reference and creating not a new one
    @classmethod
    def _init_with_source(
        cls,
        source: Union['AudioFileSource', 'AudioNumpySource', 'VideoFileSource', 'VideoColorSource', 'VideoImageSource', 'VideoNumpySource'],
        t_start: Union[int, float, Fraction] = 0.0,
        t_end: Union[int, float, Fraction, None] = None,
        audio_effects: list[Union['SerialNode', 'ParallelNode']] = [],
    ):
        """
        *For internal use only*

        Alternative '__init__' to create the
        instance from the 'source' directly. This
        method must be called by the specific
        implementations of this abstract class
        to be able to instantiate them directly
        from the 'source' to make copies.

        We created this method to avoid generating
        a new 'source' instance but preserving the
        same reference.
        """
        # Create new instance skipping '__init__'
        instance = cls.__new__(cls)
        super(cls, instance).__init__(
            source = source,
            t_start = t_start,
            t_end = t_end,
            audio_effects = audio_effects
        )

        return instance
    
    def _t_media_to_t_source(
        self,
        t_media: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ) -> Fraction:
        """
        Transform the `t_media` received to the corresponding
        `t_source` according to the media duration.

        Imagine a source that lasts `8s`, and a media that is
        pointing to the time interval `[2, 4)` of that source,
        that is a time interval `[0, 2)` because of the 2s of
        duration. If they ask for the `t_media=1` (which is
        valid because it is in the `[0, 2)` valid interval),
        they are really asking for the `t_source=3` 
        (the `t_media` plus the `media.t_start`).

        The `do_use_source_limits` boolean parameter will allow
        us to use values beyond the media limits (to be able to
        obtain frames from the source that could be useful when
        a transition is being built).
        """
        start_limit = (
            self.start_limit
            if do_use_source_limits else
            0
        )

        end_limit = (
            self.end_limit
            if do_use_source_limits else
            self.duration
        )

        """
        Source [0, 8]
        Media  [2, 4] => [0, 2]
        t_media = -3 not in [0, 2] => -1 not in [0, 8]
        t_media = -2 not in [0, 2] => 0 in [0, 8]
        t_media = -1 not in [0, 2] => 1 in [0, 8]
        t_media = 0 in [0, 2] => 2 in [0, 8]
        t_media = 1 in [0, 2] => 3 in [0, 8]
        t_media = 2 in [0, 2] => 4 in [0, 8]
        t_media = 3 not in [0, 2] => 5 in [0, 8]
        t_media = 6 not in [0, 2] => 8 in [0, 8]
        t_media = 7 not in [0, 2] => 9 not in [0, 8]
        """
        ParameterValidator.validate_mandatory_number_between('t_media', t_media, start_limit, end_limit, True, False)

        return t_media + self.t_start
    
    def __str__(
        self
    ) -> str:
        """
        Method to return the information about this media as
        a printable str.
        """
        return f'TimeInterval: [{self.t_start}, {self.t_end}). Limits: [{self.start_limit}, {self.end_limit}).'
    
"""
If the source has a duration of 8s, it means that
the time interval is [0, 8). The media will have
a maximum duration of 8s and the limits will be
those values (0 and 8). The media can be set to
[2, 4), which means that will be reading that time
interval of the source, but will be [0, 2) 
internally, so you should ask for t_media=1 to
obtain the media value, which will be transformed
into the t_source=3. Considering these, you should
be able to ask for t_media=-1, that would be
transformed into the t_source=1 that is valid.

The media will be placed (contained) in an item of
the track, that will be set in a time interval of
that track. So, the t_track=8, if that item (that
includes that media) is set in the track time
interval [7, 9), asking for the t_track=8 will be
transformed (by the item) into ask for the
t_media=1, that will be also transformed (by the
media) into the t_source=3.
"""
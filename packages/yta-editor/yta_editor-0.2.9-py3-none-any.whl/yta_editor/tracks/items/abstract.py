from yta_editor.utils.frame_wrapper import AudioFrameWrapped, VideoFrameWrapped
from yta_editor.utils.frame_generator import VideoFrameGenerator
from yta_video_frame_time.t_fraction import fps_to_time_base
from yta_time_interval import TimeInterval, TIME_INTERVAL_SYSTEM_LIMITS
from yta_validation.parameter import ParameterValidator
from quicktions import Fraction
from typing import Union
from abc import ABC, abstractmethod


# TODO: This is reapeated and not used everywhere
Number = Union[int, float, Fraction]
"""
Numeric type we accept as parameter.
"""

class _TrackItem(ABC):
    """
    Abstract class to represent an element that is on
    the track, that can be an empty space, a video, a
    transition or an audio.

    The time moments of this instance will be always a
    multiple of `1/fps`, using the `fps` of the track
    in which the item is located.
    
    This class must be inherited by our own custom item
    classes.
    """

    @property
    def t_start(
        self
    ) -> Fraction:
        """
        The time moment of the track in which this track item is
        placed, representing the moment in which it should start
        being played.
        """
        return self._time_interval.t_start

    @property
    def t_end(
        self
    ) -> Fraction:
        """
        The time moment of the track in which this track item is
        placed, representing the moment in which it should stop
        being played.
        """
        return self._time_interval.t_end
    
    @property
    def _t_first_frame(
        self
    ) -> Fraction:
        """
        *For internal use only*

        The time moment of the track in which the first frame of
        this track item starts being played, which is the `t_start`
        of this track item.

        The formula:
        - `self.t_start`
        """
        return self.t_start

    @property
    def _t_last_frame(
        self
    ) -> Fraction:
        """
        *For internal use only*

        The time moment of the track in which the last frame of
        this track item starts being played, which is the end of
        it minus 1/fps.

        The formula:
        - `self.t_end - (1 / self.fps)`
        """
        return self._get_frame_t_from_t_end(1)
    
    @property
    def duration(
        self
    ) -> Fraction:
        """
        The duration of this track item, based on its `t_start`
        and `t_end` time moments.

        The formula:
        - `self.t_end - self.t_start`
        """
        return self.t_end - self.t_start

    @property
    def fps(
        self
    ) -> float:
        """
        The fps of the track item, that is the same value as
        the track fps.
        """
        return self._track.fps
    
    @property
    def audio_fps(
        self
    ) -> float:
        """
        The audio fps of the track item, that is the same value
        as the track audio fps.
        """
        return self._track.audio_fps

    @property
    def t_start(
        self
    ) -> Fraction:
        """
        The global `t_start` time moment of this track item, which
        is obtained from the internal time interval.
        """
        return self._time_interval.t_start
    
    @property
    def t_end(
        self
    ) -> Fraction:
        """
        The global `t_end` time moment of this track item, which
        is obtained from the internal time interval.
        """
        return self._time_interval.t_end
    
    @property
    def duration(
        self
    ) -> Fraction:
        """
        The total duration of this track item based on its global
        `t_start` and `t_end` time moments.
        """
        return self._time_interval.duration
    
    @property
    @abstractmethod
    def copy(
        self
    ) -> '_TrackItem':
        """
        A copy of the current instance.
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

    def __init__(
        self,
        track: Union['AudioTrack', 'VideoTrack'],
        t_start: Union[int, float, Fraction],
        duration: Union[int, float, Fraction],
        item_in: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        transition_in: Union['TransitionTrackItem', None] = None,
        transition_out: Union['TransitionTrackItem', None] = None
    ):
        """
        The `t_start` and `duration` values will be transformed into
        multiples of `1/fps`.
        """
        ParameterValidator.validate_mandatory_positive_number('t_start', t_start, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)

        self._track: Union['AudioTrack', 'VideoTrack'] = track
        """
        The instance of the track this track item belongs to.
        """

        self._time_interval: TimeInterval = TimeInterval(
            t_start = t_start,
            t_end = t_start + duration,
            t_start_limit = None,
            t_end_limit = None,
            # TODO: This 'duration' has to be used when media
            duration_limit = None,
            fps = self.fps
        )
        """
        *For internal use only*

        Internal time interval instance to be able to manage the
        `t_start` and `t_end` time moments properly.
        """

        self.item_in: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None
        """
        The previous track item.
        """
        self.item_out: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None
        """
        The next track item.
        """
        self.transition_in: Union['TransitionTrackItem'] = None
        """
        The transition that will make the previous item in the
        track be mixed with this one at the begining.
        """
        self.transition_out: Union['TransitionTrackItem'] = None
        """
        The transition that will make the next item in the
        track be mixed with this one at the t_end.
        """

        # We will set it like this to force recalculations if needed
        if item_in is not None:
            self.set_item_in(item_in)
        if item_out is not None:
            self.set_item_out(item_out)
        if transition_in is not None:
            self.set_transition_in(transition_in)
        if transition_out is not None:
            self.set_transition_out(transition_out)

    def set_item_in(
        self,
        item: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem'],
        do_propagate: bool = True,
    ) -> '_TrackItem':
        """
        Set the provided `item` as the previous one (`.item_in`),
        and this one (self) as the `.item_out` of the one provided
        as parameter, only if the `do_propagate` parameter is True.
        """
        # TODO: Validate as one of those instances and not None
        self.item_in = item

        if (
            item.item_out is not self and
            do_propagate
        ):
            item.set_item_out(
                item = self,
                do_propagate = False
            )
        # TODO: Update the others affected if necessary (?)

        return self
    
    def unset_item_in(
        self,
        do_propagate: bool = True
    ) -> '_TrackItem':
        """
        Unset the previous item (`.item_in`) from this instance
        but also unset the `.item_out` of the previous one only if
        the `do_propagate` parameter is True.
        """
        if self.item_in is not None:
            item = self.item_in
            self.item_in = None
            # TODO: Setting 'None' maybe should be setting a Gap...

            if (
                item.item_out is self and
                do_propagate
            ):
                item.unset_item_out(do_propagate = False)

        return self
    
    def set_item_out(
        self,
        item: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem'],
        do_propagate: bool = True
    ) -> '_TrackItem':
        """
        Set the provided `item` as the next one (`.item_out`),
        and this item (self) as the `.item_in` of the `item`
        provided only if the `do_propagate` parameter is True.
        """
        self.item_out = item

        if (
            item.item_in is not self and
            do_propagate
        ):
            item.set_item_in(
                item = self,
                do_propagate = False
            )
        # TODO: Update the others affected if necessary (?)
        
        return self
    
    def unset_item_out(
        self,
        do_propagate: bool = True
    ) -> '_TrackItem':
        """
        Unset the previous item (`.item_out`) from this instance
        but also unset the `.item_in` of the previous one only if
        the `do_propagate` parameter is True.
        """
        if self.item_out is not None:
            item = self.item_out
            self.item_out = None
            # TODO: Setting 'None' maybe should be setting a Gap...

            if (
                item.item_in is self and
                do_propagate
            ):
                item.unset_item_in(do_propagate = False)

        return self
    
    def set_transition_in(
        self,
        transition: 'TransitionTrackItem'
    ) -> '_TrackItem':
        """
        Set the `transition` provided as the transition to be applied
        to mix the previous item `.item_in` with this one.
        
        TODO: Do the 'decrease' here or in the 'in' (?)

        This method will update the `t_start` time of the next items 
        (decreasing it) according to the duration of the transition
        applied, as the next items will appear earlier.
        """
        if self.item_in is None:
            raise Exception('There is no `.item_in` (previous item) to transition with.')
        
        self.transition_in = transition
        # TODO: We need to update (decrease 'self.duration') the next
        # items starts

        return self
    
    def unset_transition_in(
        self
    ) -> '_TrackItem':
        """
        Unset the transition with the previous item (`.transition_in`).

        TODO: Do the 'reset' here or in the 'in' (?)

        This method will update the `t_start` time of the next items 
        (increasing it) according to the duration of the transition
        applied, as the next items will appear later.
        """
        self.transition_in = None
        # TODO: We need to update (increase 'self.duration') the next
        # items starts

        return self
    
    def set_transition_out(
        self,
        transition: 'TransitionTrackItem'
    ) -> '_TrackItem':
        """
        Set the `transition` provided as the transition to be applied
        to mix the next item `.item_out` with this one.
        
        TODO: Do the 'decrease' here or in the 'in' (?)
        
        This method will update the `t_start` time of the next items 
        (decreasing it) according to the duration of the transition
        applied, as the next items will appear earlier.
        """
        if self.item_out is None:
            raise Exception('There is no `.item_out` (next item) to transition with.')
        
        self.transition_out = transition
        # TODO: The 'decrease' will be done here or in the 'set_transition_in' (?)

        return self
    
    def unset_transition_out(
        self
    ) -> '_TrackItem':
        """
        Unset the transition with the next item (`.transition_out`).

        TODO: Do the 'reset' here or in the 'in' (?)

        This method will update the `t_start` time of the next items 
        (increasing it) according to the duration of the transition
        applied, as the next items will appear later.
        """
        self.transition_out = None
        # TODO: The 'decrease' will be done here or in the 'set_transition_in' (?)

        return self
    
    """
    Functionality related to the time interval below.
    """

    def _shift_by(
        self,
        delta: Number
    ) -> '_TrackItem':
        """
        *For internal use only*

        This method should be called by the `Track` instance that
        holds this item.

        Move the `t_start` and `t_end` value of this item the amount
        of time defined by the `delta` provided parameter, that
        can be positive or negative (and will be truncated to be
        a multiple of `1/fps`).

        The `t_end` value will never go beyond the system's limit,
        so the duration of the item will be enshortened when delta
        is too high.
        """
        if (self.t_end + delta) >= TIME_INTERVAL_SYSTEM_LIMITS[1]:
            self._time_interval.with_start_and_end(
                t_start = self.t_start + delta,
                t_end = TIME_INTERVAL_SYSTEM_LIMITS[1]
            )
        else:
            self._time_interval.shift_by(delta)

        return self
    
    # TODO: Separate the other methods as '_shift_by' and 'shift_by'
    def shift_to(
        self,
        t_track: Number
    ) -> '_TrackItem':
        """
        Move the `t_start` and `t_end` value of this item to the time
        moment defined by the `t_track` parameter provided. The
        change will not modify the duration of the item.
        """
        return self._shift_by(
            delta = t_track - self.t_start
        )
    
    def shift_start_by(
        self,
        delta: Number
    ) -> '_TrackItem':
        """
        Update the `t_start` value by adding the `delta` provided
        (that can be positive to make it start later or negative
        to make it start earlier).
        """
        self._time_interval.shift_start_by(delta)

        return self
    
    def shift_start_to(
        self,
        t_track: Number
    ) -> '_TrackItem':
        """
        Update the `t_start` value to the one provided as `t_track`
        (that can be before or after the current one).
        """
        return self.shift_start_by(
            delta = t_track - self.t_start
        )
    
    def shift_end_by(
        self,
        delta: Number
    ) -> '_TrackItem':
        """
        Update the `t_end` value by adding the `delta` provided
        (that can be positive to make it start later or negative
        to make it start earlier).
        """
        self._time_interval.shift_end_by(delta)

        return self
    
    def shift_end_to(
        self,
        t_track: Number
    ) -> '_TrackItem':
        """
        Update the `t_end` value to the one provided as `t_track`
        (that can be before or after the current one).
        """
        return self.shift_end_by(
            delta = t_track - self.t_end
        )
    
    def split(
        self,
        t_track: Number
    ) -> '_TrackItem':
        """
        Split the current item at the `t_track` track time
        moment provided and get the 2 new TimeInterval
        instances as a tuple:
        - A: `[t_start, t_track)`
        - B: `[t_track, t_end)`.
        """
        return self._time_interval.split(t_track)
    
    def cut(
        self,
        track_start: Number,
        track_end: Number
    ) -> '_TrackItem':
        """
        Transform this track item into a new one which
        `track_start` and `track_end` are now the ones
        provided as parameters.
        """
        # TODO: What if 't_start' and 't_end' are greater than
        # before? It is not actually cutting...
        self._time_interval.cut(track_start, track_end)

        return self
    
    # TODO: What (?)
    #def propagate_
    
    """
    Functionality related to the time interval above.
    """
    
    def __str__(
        self
    ) -> str:
        """
        Function to stringify the instance and show the in
        and out items next to the item itself.
        """
        item_in: str = (
            f'{self.item_in.__class__.__name__} [{str(float(self.item_in.t_start))}, {str(float(self.item_in.t_end))}]'
            if self.item_in is not None else
            '--'
        )

        item_out: str = (
            f'{self.item_out.__class__.__name__} [{str(float(self.item_out.t_start))}, {str(float(self.item_out.t_end))}]'
            if self.item_out is not None else
            '--'
        )

        return f'  > (In: {item_in}) -   | {self.__class__.__name__} [{str(float(self.t_start))}, {str(float(self.t_end))}] |   - (Out: {item_out})'
    
    def _get_frame_t_from_t_start(
        self,
        number_of_frames: int
    ):
        """
        *For internal use only*

        Get the exact time moment of the frame that is 'number_of_frames'
        ahead of the 't_start' time moment of this track item.
        """
        ParameterValidator.validate_mandatory_positive_int('number_of_frames', number_of_frames, True)

        return self._time_interval._t_handler.t.next(self.t_start, number_of_frames) 

    def _get_frame_t_from_t_end(
        self,
        number_of_frames: int
    ):
        """
        *For internal use only*

        Get the exact time moment of the frame that is 'number_of_frames'
        before the 't_end' time moment of this track item.
        """
        ParameterValidator.validate_mandatory_positive_int('number_of_frames', number_of_frames, True)

        return self._time_interval._t_handler.t.previous(self.t_end, number_of_frames)
    
class _TrackItemWithMedia(_TrackItem):
    """
    Abstract class to represent a track item that includes a
    media file to obtain the frames from. This item is 
    special because its time interval and cannot be shifted
    randomly.

    Here you have some specific cases:
    - If the item is shifted in general, only the item time
    interval will be moved, the media time interval will be
    the same.
    - If the start of the item is shifted, the media's start
    will be also shifted to fit the same duration (this is
    like enshorting or enlarging a video from the left).
    - If the end of the item is shifted, the media's end will
    be also shifted to fit the same duration (this is like
    enshorting or enlarging a video from the right).

    Based on this before, if you need an item to

    """

    @property
    def start_limit(
        self
    ) -> Fraction:
        """
        The global time moment that is the minimum `t` time moment
        this item should be able to handle according to the media
        and the source related to this media.

        Considering a source of 8s, if this item is placed in the
        [9, 11) of the track, it should accept any `t` time moment
        in between those 9 and 11 limits. But, as the media associated
        could be, for example, [1, 3), a `t_track=8` could be accepted
        in special cases (transitions) because it would be transformed
        into `t_media=-1`, which would return `t_source=0` that is
        valid. But not a `t_track=7`, because it would be `t_media=-2`,
        which is `t_source=-1` (invalid).

        This `start_limit` must be used carefully and only for
        special cases (such as transitions).
        """
        # The 'self.media.start_limit' will be always negative or 0
        return self.t_start + self.media.start_limit

    @property
    def end_limit(
        self
    ) -> Fraction:
        """
        The global time moment that is the maximum `t` time moment
        this item should be able to handle according to the media
        and the source related to this media.
        
        Considering a source of 8s, if this item is placed in the
        [9, 11) of the track, it should accept any `t` time moment
        in between those 9 and 11 limits. But, as the media associated
        could be, for example, [2, 4), a `t_track=12` could be accepted
        in special cases (transitions) because it would be transformed
        into `t_media=3`, which would return `t_source=5` that is
        valid. But not a `t_track=16`, because it would be `t_media=7`,
        which is `t_source=9` (invalid).

        This `end_limit` must be used carefully and only for
        special cases (such as transitions).
        """
        return self.t_start + self.media.end_limit
    
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
        return self.media.is_unchanged

    def __init__(
        self,
        t_start: Number,
        media: Union['AudioMedia', 'VideoMedia'],
        **kwargs
    ):
        # TODO: I think I don't need 'AudioTime' nor 'VideoTimed'
        # but only 'AudioMedia' and 'VideoMedia'
        # ParameterValidator.validate_mandatory_instance_of('media', media, ['AudioMedia', 'VideoMedia'])

        # TODO: I think I don't need 'AudioTime' nor 'VideoTimed'
        # but only 'AudioMedia' and 'VideoMedia'
        self.media: Union['AudioMedia', 'VideoMedia'] = media
        """
        The media associated to this track item.
        """

        super().__init__(
            t_start = t_start,
            duration = media.duration,
            **kwargs
        )
        
        self._time_interval.duration_limit = self.media.max_duration
        
    def _t_track_to_t_media(
        self,
        t_track: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ) -> Fraction:
        """
        *For internal use only*

        Get the local `t` time moment value for the media
        associated, based on the global `t` time moment
        provided.

        This method will raise an exception if the `t`
        time moment provided is not included in this track
        item time interval and the `do_use_source_limits`
        parameter is not `True`. Send it as `True` if you
        need to force reading the media maybe for transitions.

        The formula:
        - `t_track - self.t_start`
        """
        start_limit = (
            self.start_limit
            if do_use_source_limits else
            self._time_interval.t_start
        )

        end_limit = (
            self.end_limit
            if do_use_source_limits else
            self._time_interval.t_end
        )

        ParameterValidator.validate_mandatory_number_between('t_track', t_track, start_limit, end_limit, True, False)
        
        """
        Imagine that we have this item in [4, 8] and we
        receive t=6. The local_t=6-4=2. The media we have
        available has 4s of duration (so [0, 4]), but it
        is actually cropped to [1, 3], so the moment we
        need to read is the t=2 of the cropped version,
        so: t_media=1+2=3. But is the media who will
        calculate that internal t, we only need to ask him
        for the t=2 and he will make the conversion (that
        is currently being done by a decorator).

        That means that we could actually ask for the t=-1
        to the media, that would be turned into the t=0 of
        the source which is actually available, so we have
        to be very careful with this...

        Source [0, 8)
        Media [0, 2) but of the source [2, 4)
        TrackItem [11, 13)
        -> Ask t_t=12 => t_media=1 => t_source = 3
            Is valid and included in the normal limits
        -> Ask t_t=10 => t_media=-1 => t_source=1
            Is valid only if forcing to use the source
            limits because t_source=1, but t_t=10 is out
            of the [11, 13) time interval
        """

        return t_track - self.t_start
    
    # The super() methods will shift only the item
    """
    These methods below will shift the media only.
    """
    def shift_media_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the media's `t_start` and `t_end` time moments by
        the `delta` amount of time provided.

        I'll give you one example below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_media_by(1)`.
        The item will be still [1, 4), but the media will be
        pointing to the [3, 6) time interval of the source.
        """
        self.media.shift_by(delta)
    
        return self
    
    def shift_media_start_and_item_end_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the media's `t_start` time moment by the `delta`
        amount of time provided, but the `t_end` of the media is
        not affected, and updates the item `t_end` time moment by
        that same `delta` amount of time, affecting not to the
        item's `t_start` time moment.

        I'll give you one example below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do
        `.shift_media_start_and_item_end_by(1)`. The item will be
        [1, 3), but the media will be pointing to the [4, 6) time
        interval of the source.
        """
        self.media.shift_start_by(delta)

        self._time_interval.shift_end_by(-delta)

        return self

    def shift_media_to(
        self,
        t_media: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the media's `t_start` to the `t_media` time moment
        provided, and the `t_end` the same amount of time.

        I'll give you one example below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_media_to(3)`.
        The item will be still [1, 4), but the media will be
        pointing to the [3, 6) time interval of the source.
        """
        delta = t_media - self.media.t_start

        return self.shift_media_by(delta)

    """
    These methods below will shift both the item and the media.
    """
    def shift_item_and_media_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        TODO: Shifting item and media at the same time? I don't
        think so... (?)

        Update the item `t_start` time moment by the `delta` value
        provided but also the media's `t_start` by the same `delta`
        value, and the `t_end` time moment of both will be also
        modified with the same amount of time. This value can be
        positive (will make it start later) or negative (will make
        it start earlier).

        I'll give you some examples below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do
        `.shift_item_and_media_by(1)`. The item will be now [2, 5),
        and the media will be pointing to the [3, 6) time interval
        of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the media, and we do
        `.shift_item_and_media_by(-1)`. The item will be now [0, 3),
        and the media will be pointing to the [1, 4) time interval
        of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do
        `.shift_item_and_media_by(-3)`. The item can be [0, 6)
        because the duration of the media is 8s, but the media would
        be pointing to the source's [-1, 2) time interval, which is
        not possible because is out of the limits (minimum `t_start
        value is 0)..
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        # TODO: Validate that the new `start` is valid according
        # to the item time interval limits
        # TODO: Validate that the new `media_start` is valid
        # according to the media interval limit
        # TODO: Is this above validated when 'shifting' (?)
        self.media.shift_by(delta)

        self._shift_by(delta)

        return self

    def shift_item_and_media_to(
        self,
        t_track: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        TODO: Shifting item and media at the same time? I don't
        think so... (?)

        Update the item `t_start` time moment to the `t_track` time
        moment provided but also the media's `t_start` time 
        variation, and the `t_end` time moment of both will be also
        modified with the same amount of time. This value can be
        greater (will make it start later) or lower (will make
        it start earlier) than the current track `t_start` time
        moment.

        I'll give you some examples below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do
        `.shift_item_and_media_to(2)`. The item will be now [2, 5),
        and the media will be pointing to the [3, 6) time interval
        of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the media, and we do
        `.shift_item_and_media_to(0)`. The item will be now [0, 3),
        and the media will be pointing to the [1, 4) time interval
        of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do
        `.shift_item_and_media_to(0)`. The item can be [0, 6)
        because the duration of the media is 8s, but the media would
        be pointing to the source's [-1, 2) time interval, which is
        not possible because is out of the limits (minimum `t_start
        value is 0)..
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        delta = t_track - self.t_start
        
        return self.shift_item_and_media_by(delta)

    """
    These methods below will shift the start and the end
    of the item and the media at the same time.
    """
    def shift_start_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the item `t_start` time moment by the `delta` value
        provided but also the media's `t_start` by the same `delta`
        value. This value can be positive (will make it last less
        time) or negative (will make it longer).

        I'll give you some examples below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_start_by(1)`.
        The item will be now [2, 4), and the media will be pointing
        to the [3, 5) time interval of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the media, and we do `.shift_start_by(-1)`.
        The item will be now [0, 4), and the media will be pointing
        to the [1, 5) time interval of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_start_by(-3)`.
        The item can be [0, 6) because the duration of the media is
        8s, but the media would be pointing to the source's [-1, 2)
        time interval, which is not possible because is out of the
        limits (minimum `t_start` value is 0)..
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        # TODO: Validate that the new `start` is valid according
        # to the item time interval limits
        # TODO: Validate that the new `media_start` is valid
        # according to the media interval limit
        # TODO: Is this above validated when 'shifting' (?)
        self.media.shift_start_by(delta)

        super().shift_start_by(delta)

        return self
    
    def shift_start_to(
        self,
        t_track: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the item `t_start` time moment to the `t_track` time
        moment value provided, but also the media the same amount
        of time than the item (only if possible). Be careful with
        the limits of the media's time interval.

        I'll give you some examples below with a media with 8s of
        duration:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_start_to(3)`.
        The item will be now [3, 4), and the media will be pointing
        to the [4, 5) of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_start_to(0)`.
        The item will be now [0, 4), and the media will be pointing
        to the [1, 5) of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_start_to(0)`.
        The item can be [0, 6) because the duration of the media is
        8s, but the media would be pointing to the source's [-1, 2)
        time interval, which is not possible because is out of the
        limits (minimum `t_start` value is 0).
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        delta = t_track - self.t_start

        # This will force the 2 shifts according to their limits
        return self.shift_start_by(delta)
    
    def shift_end_by(
        self,
        delta: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the item `t_end` time moment by the `delta` value
        provided but also the media's `t_end` by the same `delta`
        value. This value can be positive (will make it last more
        time) or negative (will make it shorter).

        I'll give you some examples below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_end_by(1)`.
        The item will be now [1, 5), and the media will be pointing
        to the [2, 6) time interval of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the media, and we do `.shift_end_by(-1)`.
        The item will be now [1, 3), and the media will be pointing
        to the [2, 4) time interval of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_end_by(4)`.
        The item can be [3, 10) because the duration of the media is
        8s, but the media would be pointing to the source's [2, 9)
        time interval, which is not possible because is out of the
        limits (maximum `t_end` value is 8).
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        # TODO: Validate that the new `start` is valid according
        # to the item time interval limits
        # TODO: Validate that the new `media_start` is valid
        # according to the media interval limit
        # TODO: Is this above validated when 'shifting' (?)
        self.media.shift_end_by(delta)

        super().shift_end_by(delta)

        return self
    
    def shift_end_to(
        self,
        t_track: Union[int, float, Fraction]
    ) -> '_TrackItemWithMedia':
        """
        Update the item `t_end` time moment to the `t_track` time
        moment value provided, but also the media the same amount
        of time than the item (only if possible). Be careful with
        the limits of the media's time interval.

        I'll give you some examples below:
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_end_to(5)`.
        The item will be now [1, 5), and the media will be pointing
        to the [2, 6) time interval of the source.
        - We have the item at [1, 4), and the media is pointing to
        the [2, 5) of the media, and we do `.shift_end_to(3)`.
        The item will be now [1, 3), and the media will be pointing
        to the [2, 4) time interval of the source.
        - We have the item at [3, 6), and the media is pointing to
        the [2, 5) of the source, and we do `.shift_end_to(10)`.
        The item can be [3, 10) because the duration of the media is
        8s, but the media would be pointing to the source's [2, 9)
        time interval, which is not possible because is out of the
        limits (maximum `t_end` value is 8).
        
        This is limited, at first, by the item time interval limit
        but also by the media time interval limit.
        """
        delta = t_track - self.t_end

        # This will force the 2 shifts according to their limits
        return self.shift_end_by(delta)
    
    # TODO: We need these methods:
    # - shift_only_item: moves the item time interval but not media
    # - shift: moves the item time interval but also the media
    # - shift_only_media: moves the media time interval only
    # Any other method (shift_start, shift_end) will shift both
    # because it is necessary to do it

class _TrackItemWithAudio(_TrackItem):
    """
    Abstract class to implement a track item that is capable
    of providing audio frames.
    """

    # def __init__(
    #     # track: 'AudioTrack',
    #     **kwargs
    # ):
    #     # ParameterValidator.validate_mandatory_instance_of('track', track, 'AudioTrack')

    #     super().__init__(
    #         # track = track,
    #         **kwargs
    #     )

    @property
    def _first_audio_frames(
        self
        # TODO: What about the type (?)
    ):
        """
        *For internal use only*
        
        The audio frames of the first video frame (as a generator),
        to be used when the item is in a transition in which the
        first and last frames are frozen to not affect the duration.
        """
        if not hasattr(self, '__first_audio_frames'):
            self.__first_audio_frames = self.get_audio_frames_at(
                t_track = self._t_first_frame,
                video_fps = self._track.fps,
                do_use_source_limits = False
            )

        return self.__first_audio_frames
    
    @property
    def _last_audio_frames(
        self
        # TODO: What about the type (?)
    ):
        """
        *For internal use only*
        
        The audio frames of the last video frame (as a generator),
        to be used when the item is in a transition in which the
        first and last frames are frozen to not affect the duration.
        """
        if not hasattr(self, '__last_audio_frames'):
            self.__last_audio_frames = self.get_audio_frames_at(
                # TODO: Should it be the inmediate time momet before 't_end' (?)
                t_track = self._t_last_frame,
                video_fps = self._track.fps,
                do_use_source_limits = False
            )

        return self.__last_audio_frames

    def get_audio_frames_at(
        self,
        t_track: Union[int, float, Fraction],
        # TODO: Ignore this, we have the 'self.fps' here
        video_fps: Union[int, float, Fraction] = None,
        do_use_source_limits: bool = False
    ):
        """
        Iterate over all the audio frames that
        exist at the time moment 't' provided.
        """
        # frames = []
        # # TODO: This should be different with the new gap item
        # if not self.is_empty_part:
        #     # TODO: What do we do in this case (?)
        #     frames = list(self._get_audio_frames_at(t_track))

        #     if len(frames) == 0:
        #         print(f'   [ERROR] Audio frame {str(float(t_track))} was not obtained')
        #     else:
        #         frames = [
        #             AudioFrameWrapped(
        #                 frame = frame,
        #                 is_from_gap = False
        #             )
        #             for frame in frames
        #         ]
        # TODO: Remove this on top if below is working

        frames = list(self._get_audio_frames_at(
            t_track = t_track,
            video_fps = video_fps,
            do_use_source_limits = do_use_source_limits
        ))

        if len(frames) == 0:
            print(f'   [ERROR] Audio frame {str(float(t_track))} was not obtained')
        else:
            # TODO: We should not receive AudioFrame and 
            # AudioFrameWrapped here, only one. Fix it (!)
            from yta_validation import PythonValidator
            frames = [
                (
                    AudioFrameWrapped(
                        frame = frame,
                        is_from_gap = False
                    )
                )
                if PythonValidator.is_instance_of(frame, 'AudioFrame') else
                frame
                for frame in frames
            ]

        # This could be because is empty part or
        # because we couldn't obtain the frames
        from yta_editor.timeline import TimelineDefaults

        frames = (
            TimelineDefaults().audio_empty
            if len(frames) == 0 else
            frames
        )

        for frame in frames:
            yield frame

    @abstractmethod
    def _get_audio_frames_at(
        self,
        t_track: Union[int, float, Fraction],
        # TODO: Ignore this, we have 'self.fps' here
        video_fps: Union[int, float, Fraction] = None,
        do_use_source_limits: bool = False
    ):
        """
        Get the audio frames of the provided `t` global time
        moment according to the internal configuration of 
        the track item.

        TODO: This method must be overwritten by the
        specific class implementations.
        """
        pass

class TrackItemWithAudioMedia(_TrackItemWithAudio, _TrackItemWithMedia):
    """
    A track item that is capable of providing audio
    frames by obtaining them from the media it contains.
    """

    def __init__(
        self,
        track: 'AudioTrack',
        t_start: Union[int, float, Fraction],
        media: 'AudioMedia',
        item_in: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        transition_in: Union['TransitionTrackItem', None] = None,
        transition_out: Union['TransitionTrackItem', None] = None
    ):
        super().__init__(
            track = track,
            t_start = t_start,
            media = media,
            item_in = item_in,
            item_out = item_out,
            transition_in = transition_in,
            transition_out = transition_out
        )

    def __init__(
        self,
        media: 'AudioTimed',
        **kwargs
    ):
        ParameterValidator.validate_mandatory_instance_of('media', media, 'AudioTimed')

        super().__init__(
            media = media,
            **kwargs
        )

    def _get_audio_frames_at(
        self,
        t_track: Union[int, float, Fraction],
        # TODO: Ignore this, we have 'self.fps' here
        video_fps: Union[int, float, Fraction] = None,
        do_use_source_limits: bool = False
    ):
        """
        Get the audio frames for the provided `t` global
        time moment, that is transformed into the media
        local time moment, from the audio media this
        instance contains.

        The `do_use_source_limits` method should be used
        when we want to access to a `t_track` that is out
        of the time interval of this track item but it is
        actually accepted by the internal source time
        interval limits.
        """
        t_media = self._t_track_to_t_media(
            t_track = t_track,
            do_use_source_limits = do_use_source_limits
        )
        
        return self.media.get_audio_frames_at(
            t_media = t_media,
            video_fps = self.fps,
            do_use_source_limits = do_use_source_limits
        )
    
class _TrackItemWithVideo(_TrackItem):
    """
    Abstract class to implement a track item that is capable
    of providing audio frames.
    """

    @property
    def _frame_not_found(
        self
    ):
        """
        *For internal use only*

        The frame we want to send to the editor when
        we were not able to find the frame we were
        looking for (due to an error or that the file
        was unreadable in that specific moment).

        This property has been created to avoid
        creating these empty frames again and again,
        as they will be always the same.

        TODO: This should not happen, it is an
        internal way to point an error, and of
        course should be removed in a future 
        version when we don't suffer it.
        """
        if not hasattr(self, '__frame_not_found'):
            self.__frame_not_found = VideoFrameGenerator.background.full_red(
                size = self._track.size,
                time_base = fps_to_time_base(self._track.fps)
            )

        return self.__frame_not_found
    
    @property
    def _first_video_frame(
        self
        # TODO: What about the type (?)
    ):
        """
        *For internal use only*

        The first video frame of this track item, useful when using
        the item in a transition in which the first and the last
        frames are frozen to not affect the duration.
        """
        if not hasattr(self, '__first_video_frame'):
            self.__first_video_frame = self.get_video_frame_at(
                t_track = self._t_first_frame,
                do_use_source_limits = False
            )

        return self.__first_video_frame
    
    @property
    def _last_video_frame(
        self
        # TODO: What about the type (?)
    ):
        """
        *For internal use only*

        The last video frame of this track item, useful when using
        the item in a transition in which the first and the last
        frames are frozen to not affect the duration.
        """
        if not hasattr(self, '__last_video_frame'):
            self.__last_video_frame = self.get_video_frame_at(
                # TODO: Should it be the inmediate time momet before 't_end' (?)
                t_track = self._t_last_frame,
                do_use_source_limits = False
            )

        return self.__last_video_frame

    # def __init__(
    #     self,
    #     # track: 'VideoTrack',
    #     **kwargs
    # ):
    #     # ParameterValidator.validate_mandatory_instance_of('track', track, 'VideoTrack')

    #     super().__init__(
    #         # track = track,
    #         **kwargs
    #     )

    def __init__(
        self,
        is_empty_part: bool = False,
        **kwargs
    ):
        super().__init__(
            **kwargs
        )

        self._is_empty_part: bool = is_empty_part
        """
        *For internal use only*

        Internal flag to indicate if this track item is an
        empty part or not.

        TODO: This is a remaining part of the previous way
        to handle the empty parts, so maybe we can remove
        it soon.
        """

    def get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ) -> 'VideoFrameWrapped':
        """
        Get the frame that must be displayed at 
        the given 't_track' global time moment.
        """
        frame: Union['VideoFrame', None] = self._get_video_frame_at(t_track, do_use_source_limits)
        # TODO: This can be None, why? I don't know...
        # TODO: Remove this below, its to be copied...
        # frame = self.media.get_video_frame_at(t)

        if frame is None:
            print(f'   [ERROR] Frame {str(float(t_track))} was not obtained')

        frame = (
            # I'm using a red full frame to be able to detect
            # fast the frames that were not available, but
            # I need to find the error and find a real solution
            # TODO: This shouldn't happen, its an error
            self._frame_not_found
            if frame is None else
            frame
        )

        # TODO: What about the 'format' (?)
        # TODO: Maybe I shouldn't set the 'time_base'
        # here and do it just in the Timeline 'render'
        #return get_black_background_video_frame(self._track.size)
        # TODO: This 'time_base' maybe has to be related
        # to a Timeline general 'time_base' and not the fps

        # TODO: We need to remove the 'is_from_gap' maybe (?)
        frame = VideoFrameWrapped(
            frame = frame,
            is_from_gap = self._is_empty_part
        )

        # TODO: This should not happen because of
        # the way we handle the videos here but the
        # video could send us a None frame here, so
        # do we raise exception (?)
        if frame._frame is None:
            #frame = get_black_background_video_frame(self._track.size)
            # TODO: By now I'm raising exception to check if
            # this happens or not because I think it would
            # be malfunctioning
            raise Exception(f'Video is returning None video frame at t={str(t_track)}.')
        
        """
        The 'track' (because of the 'timeline' it belongs
        to) has a size, so we must respect, so we need to
        use a strategy to make it fit the desired size.
        """
        # TODO: Maybe this sould be done in the 'timeline'
        # that combines the frames and not here...
        return frame
    
    @abstractmethod
    def _get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ) -> Union['VideoFrame', None]:
        """
        Get the video frame for the `t_track` time moment
        provided according to the internal configuration of
        this instance.
        """
        pass

class TrackItemWithVideoMedia(_TrackItemWithVideo, _TrackItemWithAudio, _TrackItemWithMedia):
    """
    A track item that is capable of providing video and
    audio frames by obtaining them from the video media
    it contains.
    """

    @property
    def copy(
        self
    ) -> 'TrackItemWithVideoMedia':
        """
        A copy of the current track item with media
        instance.
        """
        return TrackItemWithVideoMedia(
            track = self._track,
            t_start = self.t_start,
            media = self.media,
            item_in = self.item_in,
            item_out = self.item_out,
            transition_in = self.transition_in,
            transition_out = self.transition_out
        )

    def __init__(
        self,
        track: 'VideoTrack',
        t_start: Union[int, float, Fraction],
        media: 'VideoMedia',
        item_in: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        transition_in: Union['TransitionTrackItem', None] = None,
        transition_out: Union['TransitionTrackItem', None] = None,
    ):
        super().__init__(
            track = track,
            t_start = t_start,
            media = media,
            item_in = item_in,
            item_out = item_out,
            transition_in = transition_in,
            transition_out = transition_out,
        )

    def _get_audio_frames_at(
        self,
        t_track: Union[int, float, Fraction],
        # TODO: Ignore this, we have 'self.fps' here
        video_fps: Union[int, float, Fraction] = None,
        do_use_source_limits: bool = False
    ):
        """
        Get the audio frames for the provided `t_track`
        global time moment from the audio media this instance
        contains.

        The `do_use_source_limits` method should be used
        when we want to access to a `t_track` that is out
        of the time interval of this track item but it is
        actually accepted by the internal source time
        interval limits.
        """
        t_media = self._t_track_to_t_media(
            t_track = t_track,
            do_use_source_limits = do_use_source_limits
        )

        return self.media.get_audio_frames_at(
            t_media = t_media,
            video_fps = self.fps,
            do_use_source_limits = do_use_source_limits
        )

    def _get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction],
        do_use_source_limits: bool = False
    ) -> Union['VideoFrame', None]:
        """
        Get the video frame for the provided `t_track` time
        moment from the video media this instance contains.

        The `do_use_source_limits` method should be used
        when we want to access to a `t_track` that is out
        of the time interval of this track item but it is
        actually accepted by the internal source time
        interval limits.
        """
        t_media = self._t_track_to_t_media(
            t_track = t_track,
            do_use_source_limits = do_use_source_limits
        )

        return self.media.get_video_frame_at(
            t_media = t_media,
            do_use_source_limits = do_use_source_limits
        )
    

"""
Note for the developers:
- We have 3 different types of items:
    *Item part: An item (there are different options) 
    that is occupying that part of the track, being a
    media item, a transition item...
    *Gap part in between: An empty part that is before
    the first media or in between 2 different medias.
    *Gap part at the t_end: An empty part that is at the
    t_end of the track, after the last media, making the
    track virtually infinite.

Check the 'Track' class to see the interaction and
creation.
"""
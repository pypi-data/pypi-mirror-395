from yta_editor.tracks.items.abstract import _TrackItem
from yta_time_interval import TIME_INTERVAL_SYSTEM_LIMITS
from quicktions import Fraction
from typing import Union


# TODO: This is reapeated and not used everywhere
Number = Union[int, float, Fraction]
"""
Numeric type we accept as parameter.
"""
# TODO: What about the inheritance (?)
# TODO: Replace the 'empty' video and audio logic with
# this class
class GapTrackItem(_TrackItem):
    """
    A simple class to replace the logic related to 'empty'
    video track items and be more simple and understandable.

    This item will be placed when there is a gap in between
    2 real clips.
    """

    @property
    def _is_last_gap(
        self
    ) -> bool:
        """
        *For internal use only*

        Flag to indicate that the gap instance is the last one
        in the track, which means that the 't_end' is the system's
        limit of
        `yta_video_frame_time.interva.TIME_INTERVAL_SYSTEM_LIMITS`.
        """
        return self.t_end == TIME_INTERVAL_SYSTEM_LIMITS[1]

    @property
    def copy(
        self
    ) -> 'GapTrackItem':
        """
        A copy of the current gap instance.
        """
        return GapTrackItem(
            track = self._track,
            t_start = self.t_start,
            duration = self.duration,
            item_in = self.item_in,
            item_out = self.item_out
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

        (!) This property is useless here as it is a gap.
        """
        return True

    def __init__(
        self,
        track: 'Track',
        t_start: float,
        duration: float,
        item_in: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None
    ):
        # TODO: Maybe use the **kwargs (?)
        super().__init__(
            track = track,
            t_start = t_start,
            duration = duration,
            item_in = item_in,
            item_out = item_out,
            transition_in = None,
            transition_out = None
        )

    """
    The gap track item is special because it can be the
    last item of the track and have an t_end that is the
    system's t_end value and that 't_end' value must be kept
    as it is, so when manipulating the time interval we
    have to do it carefully and in an special way using
    the internal `_is_last_gap` flag.
    """

    def _shift_by(
        self,
        delta: Number
    ) -> '_TrackItem':
        """
        Move the `t_start` and `t_end` value of this item the amount
        of time defined by the `delta` provided parameter, that
        can be positive or negative (and will be truncated to be
        a multiple of `1/fps`).
        """
        if self._is_last_gap:
            return self.shift_start_by(delta)
        
        self._time_interval.shift_by(delta)
        
        return self
    
    def shift_to(
        self,
        t_track: Number
    ) -> '_TrackItem':
        """
        Move the `t_start` and `t_end` value of this item to the time
        moment defined by the `t_track` parameter provided. The
        change will not modify the duration of the item.
        """
        if self._is_last_gap:
            return self.shift_start_to(t_track)
        
        self._time_interval.shift_by(
            delta = t_track - self.t_start
        )
        
        return self
    
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
        if self._is_last_gap:
            return self
        
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
        if self._is_last_gap:
            return self
        
        return self.shift_end_by(
            delta = t_track - self.t_end
        )
    
    def get_audio_frames_at(
        self,
        t_media: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction, None] = None,
        do_apply_filters: bool = True,
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
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults

        return TimelineDefaults().audio_empty
    
    def _get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction]
    ) -> Union['VideoFrameWrapped', None]:
        """
        Get the video frame for the provided `t_track` time
        moment, that will be always a black frame because 
        this is a gap instance.

        The empty frames we need to send to the editor
        as the content when we don't have any frame to
        show, that can be because we have a gap (black
        screen) in that specific moment.

        This property has been created to avoid
        creating these empty frames again and again,
        as they will be always the same.
        """
        # TODO: Move the import (?)
        from yta_editor.timeline import TimelineDefaults

        return TimelineDefaults().video_empty_frame
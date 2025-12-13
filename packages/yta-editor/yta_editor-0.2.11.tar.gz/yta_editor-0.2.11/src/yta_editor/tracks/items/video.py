from yta_editor.tracks.items.abstract import TrackItemWithAudioMedia, _TrackItemWithVideo
from yta_validation.parameter import ParameterValidator
from quicktions import Fraction
from typing import Union


# TODO: Having the 'TrackItemWithVideoMedia' I don't need this
class _VideoTrackItem(TrackItemWithAudioMedia, _TrackItemWithVideo):
    """
    Class to represent an element that is on the
    track, that can be an empty space or a video.
    """

    def __init__(
        self,
        track: 'VideoTrack',
        t_start: Union[int, float, Fraction],
        t_end: Union[int, float, Fraction],
        media: Union['VideoTimed', None] = None,
        item_in: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None
    ):
        ParameterValidator.validate_instance_of('media', media, 'VideoTimed')

        super().__init__(
            track = track,
            t_start = t_start,
            t_end = t_end,
            media = media,
            item_in = item_in,
            item_out = item_out
        )

        self.transition_in: Union['TransitionTrackItem'] = None
        """
        The transition that will make the previous video in the
        track be mixed with this one at the begining.
        """
        self.transition_out: Union['TransitionTrackItem'] = None
        """
        The transition that will make the next video in the
        track be mixed with this one at the t_end.
        """
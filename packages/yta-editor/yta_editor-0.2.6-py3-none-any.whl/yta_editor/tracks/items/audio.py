from yta_editor.tracks.items.abstract import TrackItemWithAudioMedia
from yta_validation.parameter import ParameterValidator
from quicktions import Fraction
from typing import Union


class _AudioTrackItem(TrackItemWithAudioMedia):
    """
    Class to represent an element that is on the
    track, that can be an empty space or an audio.
    """

    def __init__(
        self,
        track: 'AudioTrack',
        t_start: Union[int, float, Fraction],
        t_end: Union[int, float, Fraction],
        media: Union['AudioTimed', None] = None,
        item_in: Union['_AudioTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_AudioTrackItem', 'GapTrackItem', None] = None
    ):
        ParameterValidator.validate_instance_of('media', media, 'AudioTimed')

        super().__init__(
            track = track,
            t_start = t_start,
            t_end = t_end,
            media = media,
            item_in = item_in,
            item_out = item_out
        )
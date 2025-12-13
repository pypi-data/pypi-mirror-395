"""
The video track module.
"""
from yta_editor.tracks.abstract import _TrackWithAudio, _TrackWithVideo


class VideoTrack(_TrackWithVideo, _TrackWithAudio):
    """
    Class to represent a track in which we place
    videos to build a video project.
    """

    def __init__(
        self,
        timeline: 'Timeline',
        index: int,
        size: tuple[int, int],
        audio_samples_per_frame: int,
        audio_layout: str,
        audio_format: str
    ):
        super().__init__(
            timeline = timeline,
            index = index,
            size = size,
            audio_samples_per_frame = audio_samples_per_frame,
            audio_layout = audio_layout,
            audio_format = audio_format
        )
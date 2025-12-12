"""
The audio track module.
"""
from yta_editor.tracks.abstract import _TrackWithAudio


class AudioTrack(_TrackWithAudio):
    """
    Class to represent a track in which we place
    audios to build a video project.
    """

    def __init__(
        self,
        timeline: 'Timeline',
        index: int,
        audio_fps: float,
        audio_samples_per_frame: int,
        audio_layout: str,
        audio_format: str
    ):
        super().__init__(
            timeline = timeline,
            index = index,
            audio_fps = audio_fps,
            audio_samples_per_frame = audio_samples_per_frame,
            audio_layout = audio_layout,
            audio_format = audio_format
        )
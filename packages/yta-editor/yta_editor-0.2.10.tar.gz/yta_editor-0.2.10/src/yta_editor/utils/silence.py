from yta_editor.utils.frame_wrapper import AudioFrameWrapped
from yta_editor.utils import VideoUtils
from yta_constants.ffmpeg import FfmpegAudioLayout, FfmpegAudioFormat
from yta_video_frame_time.t_fraction import fps_to_time_base
from quicktions import Fraction
from typing import Union


# TODO: Is this method here ok (?)
def generate_silent_frames(
    video_fps: float,
    audio_fps: int,
    audio_samples_per_frame: int,
    layout: str = FfmpegAudioLayout.STEREO.value,
    format: str = FfmpegAudioFormat.FLTP.value,
    is_from_gap: bool = False
) -> list[AudioFrameWrapped]:
    """
    Get the audio silent frames we need for
    a video with the given `video_fps`,
    `audio_fps` and `audio_samples_per_frame`,
    using the also provided `layout` and
    `format` for the audio frames.

    This method is used when we have empty
    items on our tracks and we need to 
    provide the frames, that are passed as
    AudioFrameWrapped instances and tagged as
    coming from empty items.
    """
    # Check how many full and partial silent
    # audio frames we need
    number_of_frames, number_of_remaining_samples = _audio_frames_and_remainder_per_video_frame(
        video_fps = video_fps,
        sample_rate = audio_fps,
        number_of_samples_per_audio_frame = audio_samples_per_frame
    )
    
    frames = (
        [
            AudioFrameWrapped(
                # This could be created once and then copied
                frame = VideoUtils.audio.frame.silent(
                    sample_rate = audio_fps,
                    number_of_samples = audio_samples_per_frame,
                    layout = layout,
                    format = format,
                    pts = None,
                    time_base = None
                ),
                is_from_gap = is_from_gap,
                is_silent = True
            )
        ] * number_of_frames
        if number_of_frames > 0 else
        []
    )

    # The remaining partial silent frames we need
    if number_of_remaining_samples > 0:
        silent_frame = VideoUtils.audio.frame.silent(
            sample_rate = audio_fps,
            number_of_samples = number_of_remaining_samples,
            # TODO: Check where do we get this value from
            layout = layout,
            # TODO: Check where do we get this value from
            format = format,
            pts = None,
            time_base = None
        )
        
        frames.append(
            AudioFrameWrapped(
                frame = silent_frame,
                is_from_gap = is_from_gap,
                is_silent = True
            )
        )

    return frames

def _audio_frames_and_remainder_per_video_frame(
    # TODO: Maybe force 'fps' as int (?)
    video_fps: Union[float, Fraction],
    sample_rate: int, # audio_fps
    number_of_samples_per_audio_frame: int
) -> tuple[int, int]:
    """
    *For internal use only*

    Get how many full silent audio frames we
    need and the remainder for the last one
    (that could be not complete), according
    to the parameters provided.

    This method returns a tuple containing
    the number of full silent audio frames
    we need and the number of samples we need
    in the last non-full audio frame.
    """
    # Video frame duration (in seconds)
    time_base = fps_to_time_base(video_fps)
    sample_rate = Fraction(int(sample_rate), 1)

    # Example:
    # 44_100 / 60 = 735  ->  This means that we
    # will have 735 samples of sound per each
    # video frame
    # The amount of samples per frame is actually
    # the amount of samples we need, because we
    # are generating it...
    samples_per_frame = sample_rate * time_base
    # The 'nb_samples' is the amount of samples
    # we are including on each audio frame
    full_audio_frames_needed = samples_per_frame // number_of_samples_per_audio_frame
    remainder = samples_per_frame % number_of_samples_per_audio_frame
    
    return int(full_audio_frames_needed), int(remainder)
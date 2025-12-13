"""
Some examples of valid video formats in
ffmpeg library:
- YUV formats: yuv420p, yuv422p, yuv444p, yuva420p, etc.
- RGB formats: rgb24, rgba, bgra, bgr0, etc.
- Grayscale formats: gray, ya8, etc.
- Special or compressed formats: nv12, nv21, p010le, etc.
- 10/12 bits formats: yuv420p10le, yuv444p12le, etc.
"""
from av.video.format import VideoFormat


# TODO: Maybe 'rgb24' should be removed in
# favor of yuv420p which is more compatible
ACCEPTED_OUTPUT_FORMATS = ['rgb24', 'rgba', 'yuv420p', 'yuva420p']
"""
The only pyav and ffmpeg video formats we
accept to export a video.
"""
VALID_OUTPUTS = {
    # Non-alpha below
    'rgb24': {'mp4', 'mov', 'avi', 'mkv', 'webm'},
    'yuv420p': {'mp4', 'mov', 'avi', 'mkv', 'webm'},
    # Alpha below
    'rgba': {'mov', 'avi', 'mkv'},
    'yuva420p': {'mov', 'webm', 'mkv'}
}
"""
A dictionary containing the video file
extensions that can handle the different
video formats we accept.
"""


class Validator:
    """
    Class to simplify validation with static
    methods.
    """

    @staticmethod
    def validate_output_video_format(
        format: str
    ) -> None:
        """
        Raise an exception if the provided
        'format' is not one of the formats
        we accept as output:
        - `rgb24`
        - `rgba`
        - `yuv420p`
        - `yuva420p`
        """
        if not format.lower() in ACCEPTED_OUTPUT_FORMATS:
            raise Exception(f'The provided format "{format}" is not one of our accepted output video formats: {", ".join(ACCEPTED_OUTPUT_FORMATS)}')
        
    @staticmethod
    def validate_filename_for_output_video_format(
        filename: str,
        format: str
    ) -> None:
        """
        Raise an exception if the extension of
        the provided 'filename' is not valid for
        the also given 'format', or if that
        'format' is not even valid by itself.
        """
        Validator.validate_output_video_format(format)

        valid_formats = VALID_OUTPUTS.get(format, set())
        if filename.split('.')[-1] not in valid_formats:
            raise Exception(f'The extension of the provided filename "{filename}" is not valid for the also given format "{format}". The filename must have one of these extensions: .{", .".join(valid_formats)}')

    
def validate_ffmpeg_video_format(
    format: str
) -> None:
    """
    Raise an exception if the provided
    'format' is not a valid ffmpeg video
    format.

    The video format will be validated
    according to the version of the ffmpeg
    library that is installed in this
    system.
    """
    if not format.lower() in VideoFormat.formats.values():
        raise Exception(f'The provided format "{format}" is not a valid video frame format for the current ffmpeg library (if installed).')
"""
Audio sources, that are the source from
where we will obtain the data to offer
as audio in our editor.

These sources will be used by other
classes to access to the frames but 
improve the functionality and simplify
it.
"""
from yta_editor.sources.abstract import _AudioSource
from yta_video_pyav.reader.filter.dataclass import GraphFilter
from yta_video_pyav.reader import AudioReader
from yta_validation.parameter import ParameterValidator
from av.audio.frame import AudioFrame
from quicktions import Fraction
from typing import Union

import numpy as np


class AudioFileSource(_AudioSource):
    """
    Class to represent an audio, read from an audio
    file, as an audio media source.

    You can apply effects directly to the source via
    ffmpeg filters.
    """

    @property
    def copy(
        self
    ) -> 'AudioFileSource':
        """
        Get a copy of this instance.
        """
        return AudioFileSource(
            filename = self.filename,
            audio_filters = self._audio_filters
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

        The source is considered unchanged if there are no
        filters to apply.
        """
        return len(self._audio_filters) == 0

    @property
    def duration(
        self
    ) -> Fraction:
        """
        The duration of the audio.
        """
        return self.reader.audio_duration
    
    @property
    def audio_fps(
        self
    ) -> Union[int, None]:
        """
        The frames per second of the audio.
        """
        return self.reader.audio_fps
    
    @property
    def audio_codec_name(
        self
    ) -> Union[str, None]:
        """
        The name of the audio codec.
        """
        return self.reader.audio_codec_name
    
    @property
    def audio_layout(
        self
    ) -> Union[str, None]:
        """
        The audio layout.
        """
        return self.reader.audio_layout
    
    @property
    def audio_format(
        self
    ) -> Union[str, None]:
        """
        The audio format.
        """
        return self.reader.audio_format
    
    @property
    def audio_time_base(
        self
    ) -> Union[Fraction, None]:
        """
        The time base of the audio.
        """
        return self.reader.audio_time_base
    
    def __init__(
        self,
        filename: str,
        audio_filters: list[GraphFilter] = []
    ):
        self.filename: str = filename
        """
        The filename of the original audio.
        """
        self._audio_filters = audio_filters
        """
        The filters we want to apply to each audio
        frame.
        """
        self.reader: AudioReader = AudioReader(
            filename = self.filename,
            audio_filters = self._audio_filters
        )
        """
        The pyav audio reader.
        """

    def add_audio_filter(
        self,
        filter: GraphFilter
    ) -> 'AudioFileSource':
        """
        Add an audio filter to the list of filters
        to apply.
        """
        ParameterValidator.validate_mandatory_instance_of('filter', filter, GraphFilter)

        # TODO: Maybe handle repeated ones (?)
        self._audio_filters.append(filter)

        return self

    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction],
        do_apply_filters: bool = True
    ):
        """
        Get the sequence of audio frames for a 
        given video 't' time moment, using the
        audio cache system.

        This is useful when we want to write a
        video frame with its audio, so we obtain
        all the audio frames associated to it
        (remember that a video frame is associated
        with more than 1 audio frame).
        """
        for frame in self.reader.get_audio_frames_at(
            t = t,
            video_fps = video_fps,
            do_apply_filters = do_apply_filters
        ):
            yield frame

# TODO: This 'AudioNumpySource' class is
# very experimental, it needs refactor
# and I don't know if we will use it...
class AudioNumpySource(_AudioSource):
    """
    Class to represent an audio, made from a
    numpy array, as an audio media source.

    This source is static. The same audio
    frame will be returned always.
    """

    @property
    def copy(
        self
    ) -> 'AudioNumpySource':
        """
        Get a copy of this instance.
        """
        return AudioNumpySource(self._array)
    
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
        return True

    @property
    def duration(
        self
    ):
        """
        The duration of the source.
        """
        # TODO: Should I return something like 999 (?)
        return None

    # TODO: Put some information about the
    # shape we need to pass, and also create
    # a 'duration' property
    @property
    def frame(
        self
    ) -> AudioFrame:
        """
        The frame that must be played.
        """
        # TODO: What 'format' do we use? I think we
        # need to inspect the array to auto detect
        # it

        # return {
        #     's16': np.int16,
        #     'flt': np.float32,
        #     'fltp': np.float32
        # }.get(audio_format, None)
    
        # By now I'm forcing to this
        return AudioFrame.from_ndarray(
            array = self._array,
            format = 'fltp',
            layout = 'stereo'
        )

    def __init__(
        self,
        array: np.ndarray,
        # TODO: I think I need more information
        # to know how to read it
        # sample_rate (?)
    ):
        self._array: np.ndarray = array
        """
        The array of information that will be
        used to make the frame that will be
        played its whole duration.
        """
        # TODO: We should autodetect format,
        # layout and 'duration' and 'sample_rate'
        # that we will call 'audio_fps' through
        # a property

    def get_audio_frames_at(
        self,
        t: Union[int, float, Fraction],
        video_fps: Union[int, float, Fraction],
        # TODO: I need it but it is not used
        do_apply_filters: bool = False
    ):
        """
        Get the sequence of audio frames for a 
        given video 't' time moment.

        This is useful when we want to write a
        video frame with its audio, so we obtain
        all the audio frames associated to it
        (remember that a video frame is associated
        with more than 1 audio frame).

        As this is an audio from a static numpy
        array, the duration must fit 1/video_fps.
        """
        # TODO: We need to concatenate the audio
        # to make it fit the 1/video_fps duration
        # or maybe this class is unnecessary...
        yield self.frame
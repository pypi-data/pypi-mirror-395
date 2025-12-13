# from yta_editor.tracks.items.abstract import TrackItemWithAudioMedia, _TrackItemWithVideo
from yta_editor.tracks.items.video import _VideoTrackItem
from yta_editor.tracks.items.abstract import _TrackItemWithVideo, _TrackItemWithAudio
from yta_constants.enum import YTAEnum as Enum
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from quicktions import Fraction
from typing import Union


# TODO: Move it
class TransitionMode(Enum):
    """
    The modes the TransitionTrackItem accept as mode to
    implement it, that is the way you handle the frames
    of the previous and the next clip.
    """

    TRIM = 'trim'
    """
    The transition will use the real frames of both the
    previous and the next clip, which will make both 
    clips last less time.

    It means that from:
    - `[ClipA] [Gap] [ClipB]`
    We will move to:
    - `[ClipA_trimmed] [Transition] [ClipB_trimmed]`
    """
    FREEZE_TAIL = 'freeze_tail'
    """
    The transition will use the last frame of the 
    previous clip but frozen, which means that it will
    be used for the whole transition duration. The next
    clip 'start' time moment will be increased because
    the previous clip is not trimmed and the transition
    will last an additional amount of time.

    It means that from:
    - `[ClipA] [Gap] [ClipB]`
    We will move to:
    - `[ClipA] [Transition] [ClipB_delayed]`
    """
    FREEZE_HEAD = 'freeze_head'
    """
    The transition will use the first frame of the next
    clip but frozen, which means that it will be used
    for the whole transition duration. The next clip
    'start' time moment will be increased because the
    previous clip is not trimmed and the transition will
    last an additional amount of time.

    It means that from:
    - `[ClipA] [Gap] [ClipB]`
    We will move to:
    - `[ClipA] [Transition] [ClipB_delayed]`
    """
    FREEZE_BOTH = 'freeze_both'
    """
    The transition will use the last frame of the
    previous clip and the first frame of the next one,
    but frozen, which means that they will be used for
    the whole transition duration. The next clip 'start'
    time moment will be increased because the previous
    clip is not trimmed and the transition will last an
    additional amount of time.

    It means that from:
    - `[ClipA] [Gap] [ClipB]`
    We will move to:
    - `[ClipA] [Transition] [ClipB_delayed]`
    """

class TransitionTrackItem(_TrackItemWithVideo, _TrackItemWithAudio):
    """
    A track item that is built by joining 2 different video
    items that are consecutive.
    """

    @property
    def copy(
        self
    ) -> '_TrackItem':
        """
        A copy of the current instance.
        """
        return TransitionTrackItem(
            track = self._track,
            t_start = self.t_start,
            duration = self.duration,
            type = self.type,
            mode = self.mode,
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

        (!) This property is useless here as it is a
        transition.
        """
        return True

    def __init__(
        self,
        track: 'VideoTrack',
        t_start: Union[int, float, Fraction],
        # TODO: We need to be able to handle options
        # different than the 50% of each clip
        duration: Union[int, float, Fraction],
        # TODO: How do we handle the type? Maybe a full config instead (?)
        type: str,
        mode: TransitionMode = TransitionMode.TRIM,
        # TODO: This is a special one so this should be different
        item_in: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None,
        item_out: Union['_AudioTrackItem', '_VideoTrackItem', 'TransitionTrackItem', 'GapTrackItem', None] = None
    ):
        mode = TransitionMode.to_enum(mode)

        super().__init__(
            track = track,
            t_start = t_start,
            duration = duration,
            item_in = item_in,
            item_out = item_out,
            # TODO: I think I don't need these transition fields
            # in this kind of item
            transition_in = None,
            transition_out = None
        )

        self.mode: TransitionMode = mode
        """
        The mode in which the transition must be implemented.
        """
        self._transition_calculator: _TransitionCalculator = _TransitionCalculator(
            duration = self.duration
            #  TODO: The 'rate_function' has to come in the configuration
        )
        """
        *For internal use only*

        A transition calculator to simplify the way we handle
        the calculations to obtain the frames we need.
        """

    def _get_audio_frames_at(
        self,
        t_track: Union[int, float, Fraction],
        # TODO: Ignore this, we have 'self.fps' here
        video_fps: Union[int, float, Fraction] = None,
        # TODO: Ignore this, we don't need it...
        do_use_source_limits: bool = True
    ) -> Union['AudioFrame', None]:
        """
        Get the audio frames of the provided `t_track`
        global time moment according to the internal
        configuration of the track item.

        TODO: This method must be overwritten by the
        specific class implementations.
        """
        # TODO: Is this the correct way? Is it generating
        # audio frames for a whole video frame (?)
        from yta_editor.timeline import TimelineDefaults

        item_in_audio_frames = (
            self.item_in.get_audio_frames_at(
                t_track = t_track,
                # TODO: We should not receive the param
                do_use_source_limits = True
            )
            if self.mode not in [TransitionMode.FREEZE_HEAD, TransitionMode.FREEZE_BOTH] else
            TimelineDefaults().audio_empty
        )

        item_out_audio_frames = (
            self.item_out.get_audio_frames_at(
                # t_track = t_track + self.duration,
                t_track = t_track,
                # TODO: We should not receive the param
                do_use_source_limits = True
            )
            if self.mode not in [TransitionMode.FREEZE_HEAD, TransitionMode.FREEZE_BOTH] else
            TimelineDefaults().audio_empty
        )

        # Obtain the local 't_track' of the transition (for the progress)
        transition_t = t_track - (self.t_end - self.duration)

        # TODO: Implement this as a combination of the audio
        # coming from clips at the same time, but by now I'm
        # just returning something
        return item_in_audio_frames

    def _get_video_frame_at(
        self,
        t_track: Union[int, float, Fraction]
    ) -> Union['VideoFrame', None]:
        """
        Get the frame of the transition for the global
        `t_track` time moment provided.
        """
        # TODO: The 't' must be the global value of the timeline
        # Obtain the frames from each video
        # TODO: I actually need to obtain a frame that will be
        # out of the current 'item_in' valid time interval, as
        # it has been trimmed because of this transition, and 
        # the part we are using is just after (for the
        # 'item_in', before for the 'item_out') the last part
        # we are showing in the video
        # TODO: Calculate the 't' based on the 'item_in' t_end
        # TODO: We need to read the 'item_in.t_end' + 'local_t'
        # for the transition

        """
        Imagine this context:
        - item_in: [0, 2)   Transition: [2, 3)   item_out: [3, 4)
        The global t=2.5 is actually the 0.5 inside the 
        transition, that should read the 'item_in.t_end+0.5' (out
        of the time interval that is being shown) of the item_in.

        Now imagine that the item_in is [0, 2) but the media 
        inside is actually [0, 8) and it is reading from [3, 5).
        That means that the transition for the global t=2.5, 
        is a local_t=0.5, should be reading the t=2.5 (out of
        time interval), that is actually the t_media=5.5.
        """

        """
        As the media has been enshortened due to the transition,
        we need to use `t_track` values that are out of the 
        current item media limits, thats why we force the values
        to be allowed with the `do_use_source_limits` parameter.

        But, as the transition could be based on frozen frames,
        we 
        """
        frame_item_in = (
            self.item_in.get_video_frame_at(
                t_track = t_track,
                do_use_source_limits = True
            )
            if self.mode not in [TransitionMode.FREEZE_HEAD, TransitionMode.FREEZE_BOTH] else
            # TODO: Return as the one on top is doing
            self.item_in._last_video_frame
        ).as_rgba_numpy

        frame_item_out = (
            self.item_out.get_video_frame_at(
                #t_track = t_track + self.duration,
                t_track = t_track,
                do_use_source_limits = True
            )
            if self.mode not in [TransitionMode.FREEZE_TAIL, TransitionMode.FREEZE_BOTH] else
            # TODO: Return as the one on top is doing
            self.item_out._first_video_frame
        ).as_rgba_numpy

        # Obtain the local 't' of the transition (for the progress)
        local_t = t_track - self.t_start

        """
        *Representacion con t(global) de clips*
        Clip A: [0, 3)   Clip B: [3, 5)
        - Añadimos transition de 1s
        Clip A: [0, 2)   Transition: [2, 3)   Clip B: [3, 4)
        - La 'Transition' tiene [2, 3) de A y [0, 1) de B
        - El t(global)=2.5 ahora cae en la transición, que se
          convierte a t(local)=2.5-(3.0-1.0)=0.5, y dado que
          la duration es 1.0; 0.5 es el t_progress=0.5
        """

        transition_calculator = _TransitionCalculator(
            duration = self.duration
            #  TODO: The 'rate_function' has to come in the configuration
        )

        t_progress = transition_calculator.get_progress_at(local_t)

        frame = transition_calculator._process_frame(
            frame_a = frame_item_in,
            frame_b = frame_item_out,
            t_progress = t_progress
        )

        # TODO: Improve this
        from yta_editor.utils.frame_wrapper import VideoFrameWrapped

        return VideoFrameWrapped(frame)
    
    # TODO: What if I have another abstract class to inherit
    # from that is different having not the transitions 
    # instead of blocking these methods here? Maybe a 
    # TrackItem, TrackItemWithTransitions (?)
    #  TODO: Should I remove this (?)
    def set_transition_in(self, transition):
        raise Exception('This class can not have transitions')
    
    def set_transition_out(self, transition):
        raise Exception('This class can not have transitions')
    
    def unset_transition_in(self):
        raise Exception('This class can not have transitions')
    
    def unset_transition_out(self):
        raise Exception('This class can not have transitions')  






from yta_math.rate_functions.rate_function import RateFunction
from yta_editor_nodes.processor.video.transitions import CrossfadeTransitionProcessor, CircleOpeningTransitionProcessor
from av.video.frame import VideoFrame

import numpy as np

# TODO: This class below could be repeated and I just
# created because I needed to (at least by now)
# TODO: If I keep this calculator method, apply it in
# the '_TransitionMedia' class if I also keep it
class _TransitionCalculator:
    """
    *For internal use only*

    A class to simplify the way we make the calculations
    related to a transition. This class must be used within
    a transition item that needs these kind of calculations.
    """

    def __init__(
        self,
        duration: float,
        rate_function: RateFunction = RateFunction.LINEAR,
    ):
        self.duration: float = duration
        """
        The duration of the transition.
        """
        self.rate_function: RateFunction = RateFunction.to_enum(rate_function)
        """
        The rate function to be applied in the transition
        progress to handle its speed.
        """
        # TODO: This depends on each node implementation and the
        # arguments are different. By now I'm forcing this
        self._transition_node: CrossfadeTransitionProcessor = CrossfadeTransitionProcessor(
            do_use_gpu = True,
            output_size = (1920, 1080)
        )
        """
        The node that will process the transition, that must
        be implemented by the child class.
        """

    def get_progress_at(
        self,
        t: float
    ) -> float:
        """
        Get the transition progress value, that will
        be in the `[0.0, 1.0]` range, according to the
        `t` time moment provided and the `rate_function`
        that must be applied in this transition.

        This method should be called only when the
        transition has to be applied, so the `t` is
        a time moment in which the two frames are 
        being played together.

        The `t` value here must be a value in the range
        [0, self.duration] and it must be calculated
        before calling this method.
        """

        """
        By now, the transition we are applying is
        as simple as being in the middle of the 2
        clips provided and lasting the 'duration'
        provided, being executed with a linear t.
        """
        # TODO: We force it, by now, to be calculated
        # outside as in this [0, self.duration] range
        ParameterValidator.validate_mandatory_number_between('t', t, 0, self.duration)

        return (
            0.0
            if t < 0 else
            1.0
            if t > self.duration else
            self.rate_function.get_n_value(
                n = max(
                    0.0,
                    min(
                        1.0,
                        t / self.duration
                    )
                )
            )
        )
    
    # TODO: This method can be overwritten to change
    # its behaviour if the specific transition needs
    # it
    def _process_frame(
        self,
        frame_a: Union['moderngl.Texture', 'np.ndarray'],
        frame_b: Union['moderngl.Texture', 'np.ndarray'],
        t_progress: float,
    ):
        # TODO: Maybe this can be placed in the general
        # class if it doesn't change

        # TODO: This can be a texture
        processed_frame = self._get_process_frame_array(
            frame_a = frame_a,
            frame_b = frame_b,
            t_progress = t_progress
        # TODO: Force this with the 'yta-numpy' utils to 'np.uint8'
        )

        if PythonValidator.is_numpy_array(processed_frame):
            processed_frame = processed_frame.astype(np.uint8)

            # frame = VideoFrame.from_ndarray(
            #     # TODO: Force this with the 'yta-numpy' utils to 'np.uint8'
            #     array = processed_frame,
            #     format = 'rgb24'
            # )
        elif PythonValidator.is_instance_of(processed_frame, 'Texture'):
            # buffer = ctx.buffer(reserve=texture.width * texture.height * 3)
            # texture.read_into(buffer, components=3, dtype='u1')

            # import numpy as np
            # rgb = np.frombuffer(buffer.read(), dtype=np.uint8).reshape((h, w, 3))
            # TODO: Apparently, there is another way to use a reusable
            # buffer to transform a texture into a numpy array, so 
            # please refactor when possible (check the code above)
            # from moderngl import Texture
            # processed_frame: Texture
            #data = processed_frame.read(components = 3, dtype = 'u1')

            # OpenGL uses textures flipped, so maybe (?)
            data = processed_frame.read()
            w, h = processed_frame.size

            # data = np.flip(data, axis = 0)

            # TODO: I'm removing the alpha channel here...
            data = np.frombuffer(data, dtype = np.uint8).reshape((h, w, 4))
            data = np.flip(data, axis = 0)
            processed_frame  = data[:, :, :3]
        else:
            # TODO: Wtf? This should not happen
            raise Exception('Wowowowooo, no texture, no np.ndarray... wtf?')
        
        frame = VideoFrame.from_ndarray(
            # TODO: Force this with the 'yta-numpy' utils to 'np.uint8'
            array = processed_frame,
            format = 'rgb24'
        )

        # The 'pts' and that is not important here but...
        frame.pts = None
        frame.time_base = Fraction(1, 60)

        return frame
    
    # TODO: Overwrite this method to make it custom (?)
    def _get_process_frame_array(
        self,
        frame_a: Union['moderngl.Texture', 'np.ndarray'],
        frame_b: Union['moderngl.Texture', 'np.ndarray'],
        t_progress: float,
    ) -> np.ndarray:
        """
        Get the numpy array that will be used to build the
        pyav VideoFrame that will be returned.
        """
        return self._transition_node.process(
            first_input = frame_a,
            second_input = frame_b,
            progress = t_progress
        )

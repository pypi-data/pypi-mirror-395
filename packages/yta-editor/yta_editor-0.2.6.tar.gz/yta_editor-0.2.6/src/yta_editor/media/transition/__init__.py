# from yta_editor.tracks.media.video import VideoTimed
# from yta_editor.media.video import _VideoMedia
# from yta_video_frame_time.t_fraction import get_ts, fps_to_time_base, T
# from yta_math.rate_functions.rate_function import RateFunction
# from yta_video_pyav.writer import VideoWriter
# from yta_video_pyav.settings import Settings
# from yta_validation.parameter import ParameterValidator
# from av.video.frame import VideoFrame
# from quicktions import Fraction
# from typing import Union

# import numpy as np


# class _TransitionMedia:
#     """
#     *For internal use only*

#     This class must be inherited by the transitions
#     that have the specific implementation.

#     Class to wrap a transition clip, that is a
#     clip in which 2 clips are joined with some logic.

#     TODO: This class, by now, is only handling clips
#     that are played together during the 'transition'
#     period of time. No frozen frames, no diferent
#     time moments. When the transition is executed
#     both videos are being played at the same time.
#     """

#     @property
#     def _t_start(
#         self
#     ) -> Fraction:
#         """
#         *For internal use only*

#         The moment in which the transition clip starts
#         being played, that will be in some moment of
#         the first clip, and it should be also the 
#         moment in which the second clip starts being
#         played (with the corresponding transition
#         blending).
#         """
#         # TODO: This value is only valid for the transition
#         # applied in the middle with 50%-50% strategy
#         return self._clip_a.duration - self.duration
    
#     @property
#     def _t_end(
#         self
#     ) -> Fraction:
#         """
#         *For internal use only*

#         The moment in which the whole clip built with
#         the transition in the middle must stop being
#         played, so the second clip has finished.
#         """
#         return self._clip_b.end

#     def __init__(
#         self,
#         # TODO: This '_MediaTimed' has to be renamed 
#         # because here it is not on a track but the class
#         # we need is this one
#         # TODO: Maybe it has to be just a Media, not OnTrack
#         clip_a: _VideoMedia,
#         clip_b: _VideoMedia,
#         duration: float,
#         rate_function: RateFunction = RateFunction.LINEAR,
#     ):
#         """
#         The clips must come ordered, so the `clip_a` must be
#         playing before the `clip_b`.
#         """
#         print(type(clip_a))
#         # TODO: Here we are receiving VideoTimed
#         ParameterValidator.validate_subclass_of('clip_a', clip_a, _VideoMedia)
#         ParameterValidator.validate_subclass_of('clip_b', clip_b, _VideoMedia)

#         if clip_b.start > clip_a.start:
#             raise Exception('The `clip_a` must start before the `clip_b`.')

#         if (
#             clip_a.duration < duration or
#             clip_b.duration < duration
#         ):
#             raise Exception('The duration of one of the clips is smaller than the transition duration requested.')

#         # TODO: Apply Union[AlphaBlendTransition, ...]
#         self.duration: float = duration
#         """
#         The duration of the transition.
#         """
#         self.rate_function: RateFunction = RateFunction.to_enum(rate_function)
#         """
#         The rate function to be applied in the transition
#         progress to handle its speed.
#         """

#         self._clip_a: VideoTimed = VideoTimed(
#             media = clip_a,
#             start = 0
#         )
#         """
#         The first clip to join in with the transition.
#         """
#         self._clip_b: VideoTimed = VideoTimed(
#             media = clip_b,
#             start = self._t_start
#         )
#         """
#         The second clip to join in with the transition.
#         """

#         self._transition_node: 'TransitionNode' = None
#         """
#         The node that will process the transition, that must
#         be implemented by the child class.
#         """

#         # TODO: Set '_transition_node' in children and remove
#         # this below
#         # TODO: The child class must implement the
#         # 'self.opengl_node' variable
#         # self.opengl_node: '_OpenglNodeBase' = CrossfadeTransitionNode(
#         #     opengl_context = OpenGLContext().context,
#         #     # TODO: Do not hardcode, please
#         #     size = (1920, 1080),
#         # )
    
#     def get_transition_progress_at(
#         self,
#         t: float
#     ) -> float:
#         """
#         Get the transition progress value, that will
#         be in the [0.0, 1.0] range, according to the
#         `t` time moment provided and the `rate_function`
#         that must be applied in this transition.

#         This method should be called only when the
#         transition has to be applied, so the `t` is
#         a time moment in which the two frames are 
#         being played together.
#         """

#         """
#         By now, the transition we are applying is
#         as simple as being in the middle of the 2
#         clips provided and lasting the 'duration'
#         provided, being executed with a linear t.
#         """
#         # The transition can start in a time moment
#         # different than 0 so we recalculate it
#         t -= self._t_start

#         return (
#             0.0
#             if t < 0 else
#             1.0
#             if t > self.duration else
#             self.rate_function.get_n_value(
#                 n = max(
#                     0.0,
#                     min(
#                         1.0,
#                         t / self.duration
#                     )
#                 )
#             )
#         )
    
#     def get_video_frame_at(
#         self,
#         t: Union[int, float, Fraction],
#         do_apply_filters: bool = False
#     ) -> VideoFrame:
#         """
#         The `t` time moment provided must be a global
#         time value pointing to a moment in the general
#         timeline. That value will be transformed to the
#         internal `t` value to get the frame.
#         """
#         # Test with OpenGL
#         frame_a = self._clip_a.get_video_frame_at(t)
#         frame_b = self._clip_b.get_video_frame_at(t)

#         if (
#             frame_a is None and
#             frame_b is None
#         ):
#             print('Both None, wtf')
#             #return None

#         """
#         There is a moment in which we are not in
#         the transition section but on the clips
#         so we just need to return the clip frames.
#         """
#         if frame_b is None:
#             # Not transition time, just one clip
#             out_frame = frame_a
#             out_frame.pts = None
#             out_frame.time_base = Fraction(1, 60)

#             return out_frame
        
#         if frame_a is None:
#             # Not transition time, just one clip
#             out_frame = frame_b
#             out_frame.pts = None
#             out_frame.time_base = Fraction(1, 60)

#             return out_frame
        
#         # Render loop
#         # TODO: Why as 'rgb24' and 'np.float32' and no 'np.uint8' (?)
#         # TODO: We should try to read with GPU maybe
#         # TODO: What if it comes from a numpy and not a file as VideoFrame (?)
#         frame_a = frame_a.to_ndarray(format = 'rgb24').astype(np.float32)
#         frame_b = frame_b.to_ndarray(format = 'rgb24').astype(np.float32)

#         # TODO: Do we need the alpha (not rgb24?) maybe
#         # to mix with something else
#         return self._process_frame(
#             frame_a = frame_a,
#             frame_b = frame_b,
#             t_progress = self.get_transition_progress_at(t)
#         )
    
#     # TODO: This method can be overwritten to change
#     # its behaviour if the specific transition needs
#     # it
#     def _process_frame(
#         self,
#         frame_a: Union['moderngl.Texture', 'np.ndarray'],
#         frame_b: Union['moderngl.Texture', 'np.ndarray'],
#         t_progress: float,
#     ):
#         # TODO: Maybe this can be placed in the general
#         # class if it doesn't change
#         frame = VideoFrame.from_ndarray(
#             array = self._get_process_frame_array(
#                 frame_a = frame_a,
#                 frame_b = frame_b,
#                 t_progress = t_progress
#             # TODO: Force this with the 'yta-numpy' utils to 'np.uint8'
#             ).astype(np.uint8),
#             format = 'rgb24'
#         )

#         # frame = VideoFrame.from_ndarray(
#         #     array = texture_to_frame(
#         #         texture = self._transition_node.process(
#         #             input_a = frame_a,
#         #             input_b = frame_b,
#         #             progress = t_progress
#         #         ),
#         #         do_include_alpha = False
#         #     ).astype(np.uint8),
#         #     format = 'rgb24'
#         # )

#         # The 'pts' and that is not important here but...
#         frame.pts = None
#         frame.time_base = Fraction(1, 60)

#         return frame
    
#     # TODO: Overwrite this method to make it custom (?)
#     def _get_process_frame_array(
#         self,
#         frame_a: Union['moderngl.Texture', 'np.ndarray'],
#         frame_b: Union['moderngl.Texture', 'np.ndarray'],
#         t_progress: float,
#     ) -> np.ndarray:
#         """
#         Get the numpy array that will be used to build the
#         pyav VideoFrame that will be returned.
#         """
#         return self._transition_node.process(
#             input_a = frame_a,
#             input_b = frame_b,
#             progress = t_progress
#         )
    
#     # TODO: Add 'save_frame_as'

#     def save_as(
#         self,
#         output_filename: str,
#         video_size: tuple[int, int] = None,
#         video_fps: float = None,
#         video_codec: str = None,
#         video_pixel_format: str = None,
#         audio_codec: str = None,
#         audio_sample_rate: int = None,
#         audio_layout: str = None,
#         audio_format: str = None,
#         do_apply_video_filters: bool = True,
#         do_apply_audio_filters: bool = True
#     ) -> str:
#         """
#         Save the file as 'output_filename'.

#         This method is useful if you want to apply
#         some filter and then save the video with
#         those filters applied into a new one, maybe
#         with a new pixel format and/or code. You can
#         prepare alpha transitions, etc.
#         """
#         video_size = (
#             getattr(self, 'size', Settings.DEFAULT_VIDEO_SIZE.value)
#             if video_size is None else
#             video_size
#         )

#         video_fps = (
#             getattr(self, 'fps', Settings.DEFAULT_VIDEO_FPS.value)
#             if video_fps is None else
#             video_fps
#         )

#         video_codec = (
#             getattr(self, 'codec_name', Settings.DEFAULT_VIDEO_CODEC.value)
#             if video_codec is None else
#             video_codec
#         )

#         video_pixel_format = (
#             getattr(self, 'pixel_format', Settings.DEFAULT_PIXEL_FORMAT.value)
#             if video_pixel_format is None else
#             video_pixel_format
#         )

#         audio_codec = (
#             getattr(self, 'audio_codec_name', Settings.DEFAULT_AUDIO_CODEC.value)
#             if audio_codec is None else
#             audio_codec
#         )

#         audio_sample_rate = (
#             getattr(self, 'audio_fps', Settings.DEFAULT_AUDIO_FPS.value)
#             if audio_sample_rate is None else
#             audio_sample_rate
#         )

#         audio_layout = (
#             getattr(self, 'audio_layout', Settings.DEFAULT_AUDIO_LAYOUT.value)
#             if audio_layout is None else
#             audio_layout
#         )

#         audio_format = (
#             getattr(self, 'audio_format', Settings.DEFAULT_AUDIO_FORMAT.value)
#             if audio_format is None else
#             audio_format
#         )

#         writer = VideoWriter(output_filename)

#         # TODO: This has to be dynamic according to the
#         # video we are writing (?)
#         writer.set_video_stream(
#             codec_name = video_codec,
#             fps = video_fps,
#             size = video_size,
#             pixel_format = video_pixel_format
#         )
        
#         writer.set_audio_stream(
#             codec_name = audio_codec,
#             fps = audio_sample_rate,
#             layout = audio_layout,
#             format = audio_format
#         )

#         # TODO: Maybe we need to reformat or something
#         # if some of the values changed, such as fps,
#         # audio sample rate, etc. (?)

#         time_base = fps_to_time_base(video_fps)
#         audio_time_base = fps_to_time_base(audio_sample_rate)

#         for t in get_ts(0, self._t_end, video_fps):
#             frame = self.get_video_frame_at(
#                 t = t,
#                 do_apply_filters = do_apply_video_filters
#             )

#             # TODO: What if 'frame' is None (?)
#             if frame is None:
#                 print(f'   [ERROR] Frame not found at t:{float(t)}')
#                 continue

#             writer.mux_video_frame(
#                 frame = frame
#             )

#             frame.time_base = time_base
#             frame.pts = T(t, time_base).truncated_pts

#             # TODO: Make this work
#             # audio_pts = 0
#             # for audio_frame in self.get_audio_frames_at(
#             #     t = t,
#             #     video_fps = video_fps,
#             #     do_apply_filters = do_apply_audio_filters
#             # ):
#             #     # TODO: 'audio_frame' could be None or []
#             #     # here if no audio channel
#             #     if audio_frame is None:
#             #         # TODO: Generate silence audio to cover the
#             #         # whole video frame (?)
#             #         pass
                
#             #     # We need to adjust our output elements to be
#             #     # consecutive and with the right values
#             #     # TODO: We are using int() for fps but its float...
#             #     audio_frame.time_base = audio_time_base
#             #     audio_frame.pts = audio_pts

#             #     # We increment for the next iteration
#             #     audio_pts += audio_frame.samples

#             #     writer.mux_audio_frame(audio_frame)

#         writer.mux_video_frame(None)
#         writer.mux_audio_frame(None)
#         writer.output.close()

#         return output_filename
    
# from yta_editor_nodes.processor.video.transitions import CrossfadeTransitionProcessor
    
# # TODO: This should be moved, maybe, to another file
# class CrossfadeTransitionMedia(_TransitionMedia):
#     """
#     A simple crossfade transition.
#     """

#     def __init__(
#         self,
#         clip_a: _VideoMedia,
#         clip_b: _VideoMedia,
#         duration: float,
#         rate_function: RateFunction = RateFunction.LINEAR,
#     ):
#         super().__init__(
#             clip_a = clip_a,
#             clip_b = clip_b,
#             duration = duration,
#             rate_function = rate_function
#         )
        
#         self._transition_node: CrossfadeTransitionProcessor = CrossfadeTransitionProcessor(
#             do_use_gpu = True,
#             output_size = (1920, 1080)
#         )
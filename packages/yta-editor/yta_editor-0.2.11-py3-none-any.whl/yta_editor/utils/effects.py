# from yta_numpy.rgba.utils import RGBAFrameUtils
# from yta_editor_nodes.old_opengl.effects import AudioEffectsStack, VideoEffectsStack
# from yta_validation import PythonValidator
# from yta_validation.parameter import ParameterValidator
# from av.video.frame import VideoFrame
# from av.audio.frame import AudioFrame
# from quicktions import Fraction
# from typing import Union


# # TODO: These methods below are old version and
# # now we are implementing effects through nodes
# """
# These methods below are shared by the
# Audio and Video class that handle and
# wrap an audio or video.
# """
# def apply_video_effects_to_frame_at(
#     effects_stack: VideoEffectsStack,
#     frame: VideoFrame,
#     t: Union[int, float, 'Fraction']
# ) -> Union[VideoFrame, 'ndarray']:
#     """
#     Apply the video effects to the given
#     'frame' on the 't' time moment provided.

#     This method should be called before 
#     yielding any frame.
#     """
#     ParameterValidator.validate_mandatory_instance_of('frame', frame, VideoFrame)
#     ParameterValidator.validate_mandatory_instance_of('effects_stack', effects_stack, VideoEffectsStack)

#     if len(effects_stack.effects) == 0:
#         return frame

#     # TODO: I think this has to preserve the
#     # transparency if any of the video frames
#     # that are passed to this method (from 
#     # the different layers) have an alpha
#     # channel or we will lose it in the
#     # process... By now I'm just forcing the
#     # format that comes. Or maybe not,
#     # because when a frame comes and has no
#     # transparency, the next frames will be
#     # not visible (if coming ordered by
#     # priority)... Well... maybe I'm confused
#     # right now and this just modifies a 
#     # single frame or a frame that has been
#     # combined previously, so no worries...

#     # We handle frames as 'rgb24' or 'rgba' and
#     # then reformat to the expected format (if
#     # needed)
#     temp_format = (
#         'rgba'
#         if (
#             frame.format.name != 'rgba' and
#             'a' in frame.format.name
#         ) else
#         'rgb24'
#         if (
#             frame.format.name != 'rgb24' and
#             'a' not in frame.format.name
#         ) else
#         frame.format.name
#     )

#     # Need to send the frame as a numpy for
#     # the effects
#     new_frame = effects_stack.apply_effects_at(
#         frame = frame.to_ndarray(
#             format = temp_format
#         ),
#         # The 't' here is the internal valid one
#         t = t
#     )

#     """
#     When applying the video effects we use
#     opengl textures that return, always, an
#     alpha channel, so we need to remove it
#     if we don't actually need it
#     """
#     new_frame = (
#         RGBAFrameUtils.remove_alpha_channel_from_frame(new_frame)
#         if temp_format == 'rgb24' else
#         new_frame
#     )

#     # Rebuild the VideoFrame
#     new_frame = VideoFrame.from_ndarray(
#         array = new_frame,
#         format = temp_format
#     )

#     new_frame = (
#         new_frame.reformat(format = frame.format.name)
#         if frame.format.name != temp_format else
#         new_frame
#     )

#     """
#     We need 'time_base' and 'pts' values to
#     be identified by pyav as valid frames 
#     but we don't actually care about the
#     values because the Timeline that renders
#     will overwrite them
#     """
#     new_frame.time_base = (
#         frame.time_base
#         if frame.time_base is not None else
#         Fraction(1, 60)
#     )

#     new_frame.pts = (
#         frame.pts
#         if frame.pts is not None else
#         0
#     )

#     return new_frame

# def apply_audio_effects_to_frame_at(
#     effects_stack: AudioEffectsStack,
#     frame: Union['AudioFrame', 'ndarray'],
#     t: Union[int, float, 'Fraction']
# ) -> Union['AudioFrame', 'ndarray']:
#     """
#     Apply the audio effects to the given
#     'frame' on the 't' time moment provided.

#     This method should be called before 
#     yielding any frame.
#     """
#     # TODO: I think we shouldn't receive a
#     # 'ndarray' here, it must be AudioFrame
#     ParameterValidator.validate_mandatory_instance_of('frame', frame, [AudioFrame, 'ndarray'])

#     # Need the frame as a numpy
#     new_frame = (
#         frame.to_ndarray()
#         if PythonValidator.is_instance_of(frame, AudioFrame) else
#         frame
#     )
    
#     new_frame = effects_stack.apply_effects_at(
#         frame = new_frame,
#         # The 't' here is the internal valid one
#         t = t
#     )

#     # Rebuild the AudioFrame
#     new_frame = AudioFrame.from_ndarray(
#         array = new_frame,
#         format = frame.format,
#         layout = frame.layout
#     )

#     new_frame.sample_rate = frame.sample_rate

#     """
#     When applying the video effects we use
#     opengl textures that return, always, an
#     alpha channel, so we need to remove it
#     if we don't actually need it
#     """
#     new_frame.time_base = (
#         frame.time_base
#         if frame.time_base is not None else
#         Fraction(1, 60)
#     )

#     new_frame.pts = (
#         frame.pts
#         if frame.pts is not None else
#         0
#     )

#     return new_frame


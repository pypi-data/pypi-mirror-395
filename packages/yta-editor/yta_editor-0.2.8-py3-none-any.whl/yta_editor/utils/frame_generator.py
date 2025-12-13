"""
The video frames must be built using the
(height, width) size when giving the numpy
array that will be used for it. We will
receive the values as (width, height) but
we will invert them when needed.

The frames that come from an empty part
are flagged with the .metadata attribute
'is_from_gap' so we can recognize
them and ignore when combining on the
timeline. We have that metadata in the
wrapper class we created.

TODO: Check because we have a similar
module in other project or projects.
"""
from yta_editor.utils.alpha import _update_transparency, _transparency_to_alpha
from yta_numpy.rgba.generator import RGBAFrameGenerator
from av.video.frame import VideoFrame
from typing import Union

import numpy as np


class _BackgroundFrameGenerator:
    """
    Internal class to simplify the way we
    access to the generation of background
    frames form the general generator class.
    """

    @staticmethod
    def full_black(
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ) -> VideoFrame:
        """
        Get a video frame that is completely black
        and of the given `size`.

        The `transparency` must be a float between
        `0.0` (opaque) and `1.0` (transparent) to be
        set, or None if you don't want transparency.

        Providing `transparency` as None will 
        result in a numpy with only 3 dimensions.
        """
        return _BackgroundFrameGenerator._full_color(
            color = 'black',
            size = size,
            dtype = dtype,
            pts = pts,
            time_base = time_base,
            transparency = transparency
        )
    
    @staticmethod
    def full_white(
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ) -> VideoFrame:
        """
        Get a video frame that is completely white
        and of the given 'size'.

        The 'transparency' must be a float between
        0.0 (opaque) and 1.0 (transparent) to be
        set, or None if you don't want transparency.

        Providing 'transparency' as None will 
        result in a numpy with only 3 dimensions.
        """
        return _BackgroundFrameGenerator._full_color(
            color = 'white',
            size = size,
            dtype = dtype,
            pts = pts,
            time_base = time_base,
            transparency = transparency
        )

    @staticmethod
    def full_red(
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ) -> VideoFrame:
        """
        Get a video frame that is completely red
        and of the given 'size'.

        The 'transparency' must be a float between
        0.0 (opaque) and 1.0 (transparent) to be
        set, or None if you don't want transparency.

        Providing 'transparency' as None will 
        result in a numpy with only 3 dimensions.
        """
        return _BackgroundFrameGenerator._full_color(
            color = 'red',
            size = size,
            dtype = dtype,
            pts = pts,
            time_base = time_base,
            transparency = transparency
        )
    
    # TODO: Refactor all this please
    @staticmethod
    def full_green(
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ) -> VideoFrame:
        """
        Get a video frame that is completely green
        and of the given 'size'.

        The 'transparency' must be a float between
        0.0 (opaque) and 1.0 (transparent) to be
        set, or None if you don't want transparency.

        Providing 'transparency' as None will 
        result in a numpy with only 3 dimensions.
        """
        return _BackgroundFrameGenerator._full_color(
            color = 'green',
            size = size,
            dtype = dtype,
            pts = pts,
            time_base = time_base,
            transparency = transparency
        )

    @staticmethod
    def full_blue(
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ) -> VideoFrame:
        """
        Get a video frame that is completely blue
        and of the given 'size'.

        The 'transparency' must be a float between
        0.0 (opaque) and 1.0 (transparent) to be
        set, or None if you don't want transparency.

        Providing 'transparency' as None will 
        result in a numpy with only 3 dimensions.
        """
        return _BackgroundFrameGenerator._full_color(
            color = 'blue',
            size = size,
            dtype = dtype,
            pts = pts,
            time_base = time_base,
            transparency = transparency
        )
    
    @staticmethod
    def _full_custom(
        color: tuple[int, int, int],
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ):
        """
        *For internal use only*

        Create an array of the given RGB 'color'
        with the 'size' and 'dtype' provided, using
        the also given 'transparency'.
        """
        format = (
            'rgba'
            if transparency is not None else
            'rgb24'
        )

        transparency = _update_transparency(
            transparency = transparency,
            format = format
        )

        frame = RGBAFrameGenerator.color._get_numpy_array(
            color = color,
            size = size,
            dtype = dtype,
            alpha = _transparency_to_alpha(transparency)
        )

        return numpy_to_video_frame(
            frame = frame,
            format = format,
            pts = pts,
            time_base = time_base
        )
    
    @staticmethod
    def _full_color(
        color: str,
        size: tuple[int, int] = (1920, 1080),
        dtype: np.dtype = np.uint8,
        # TODO: I disable format by now because I
        # make it dynamic according to the 
        # 'transparency' value provided
        #format: str = 'rgb24',
        pts: Union[int, None] = None,
        time_base: Union['Fraction', None] = None,
        transparency: Union[float, None] = None
    ):
        """
        *For internal use only*

        Method that dynamically calls the internal
        method to generate the numpy according to
        the 'color' provided, that must fit the
        name of an existing method of the 
        '_FrameGenerator' class.
        """
        format = (
            'rgba'
            if transparency is not None else
            'rgb24'
        )

        transparency = _update_transparency(
            transparency = transparency,
            format = format
        )

        generator_method = getattr(RGBAFrameGenerator.color, color)
        
        frame = generator_method(
            size = size,
            dtype = dtype,
            alpha = _transparency_to_alpha(transparency)
        )

        return numpy_to_video_frame(
            frame = frame,
            format = format,
            pts = pts,
            time_base = time_base
        )

class VideoFrameGenerator:
    """
    Class to wrap the functionality related to
    generating a pyav video frame.

    This class is useful when we need to 
    generate the black background for empty
    items within the tracks and in other 
    situations.
    """

    background: _BackgroundFrameGenerator = _BackgroundFrameGenerator
    """
    Shortcut to the background generation.
    """

def numpy_to_video_frame(
    frame: np.ndarray,
    format: str = 'rgb24',
    pts: Union[int, None] = None,
    time_base: Union['Fraction', None] = None
) -> VideoFrame:
    """
    Transform the given numpy 'frame' into a
    pyav video frame with the given 'format'
    and also the 'pts' and/or 'time_base' if
    provided.
    """
    frame = VideoFrame.from_ndarray(
        # TODO: What if we want alpha (?)
        array = frame,
        format = format
    )

    if pts is not None:
        frame.pts = pts

    if time_base is not None:
        frame.time_base = time_base

    return frame
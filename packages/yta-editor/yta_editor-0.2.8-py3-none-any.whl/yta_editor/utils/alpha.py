from typing import Union


def _update_transparency(
    transparency: Union[float, None],
    format: Union[str, None] = None
) -> Union[float, None]:
    """
    *For internal use only*

    Update the provided 'transparency' value,
    that must be a value in the [0.0, 1.0] range,
    if necessary.

    If the 'format' is provided:
    - Alpha format will force an opaque alpha
    transparency if it is None
    - Non-alpha format will force a None value
    if transparency is provided
    """
    return (
        # Alpha format, no transparency => opaque
        0.0
        if (
            transparency is None and
            format is not None and
            'a' in format 
        ) else
        # Non-alpha format but transparency => None
        None
        if (
            transparency is not None and
            format is not None and
            'a' not in format
        ) else
        # Lower than 0.0 limit
        0.0
        if (
            transparency is not None and
            transparency < 0.0
        ) else
        # Greater than 1.0 limit
        1.0
        if (
            transparency is not None and
            transparency > 1.0
        ) else
        transparency
    )

def _transparency_to_alpha(
    transparency: Union[float, None]
) -> Union[int, None]:
    """
    *For internal use only*

    The `transparency` value provided must be a
    None or a value in the `[0.0, 1.0]` range,
    meaning  this:
    - `0.0`: No transparency, full color
    - `1.0`: Full transparent, no color

    The `alpha` value returned is the one that
    will be used as the alpha channel of an RGBA
    color, in which 255 means the full presence
    of the color, meaning no transparency, and 0
    the absence of color, meaning that it is full
    transparent.

    The formula:
    - `int(255 - transparency * 255)`
    """
    return (
        int(255 - transparency * 255)
        if transparency is not None else
        transparency
    )
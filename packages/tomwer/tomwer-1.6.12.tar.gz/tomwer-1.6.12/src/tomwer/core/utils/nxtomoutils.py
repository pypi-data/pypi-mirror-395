from __future__ import annotations

import numpy
from nxtomo.nxobject.nxdetector import ImageKey


def get_n_series(image_key_values: tuple | list, image_key_type: ImageKey) -> int:
    """
    Return the number of series of an image_key. Image key can be dark, flat, or projection.
    A series is defined as a contiguous elements in image_key_values

    :param image_key_values: list or tuple of image_keys to consider. Can be integers or tomoscan.esrf.scan.hdf5scan.ImageKey
    """
    image_key_type = ImageKey(image_key_type)
    if image_key_type is ImageKey.INVALID:
        raise ValueError(
            "we can't count Invalid image keys series because those are ignored from tomoscan"
        )
    image_key_values = [ImageKey(img_key) for img_key in image_key_values]

    # remove invalid frames
    image_key_values = numpy.array(
        image_key_values
    )  # for filtering invalid value a numpy aray is requested
    image_key_values = image_key_values[image_key_values != ImageKey.INVALID]

    n_series = 0
    is_in_a_serie = False
    for frame in image_key_values:
        if frame == image_key_type and not is_in_a_serie:
            is_in_a_serie = True
            n_series += 1
        elif frame != image_key_type:
            is_in_a_serie = False
    return n_series

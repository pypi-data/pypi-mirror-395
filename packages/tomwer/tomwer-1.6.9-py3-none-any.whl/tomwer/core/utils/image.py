from __future__ import annotations

import enum
import logging

import numpy
from numpy.linalg import inv

_logger = logging.getLogger(__file__)
try:
    from scipy.ndimage import shift as shift_scipy

    has_scipy_shift = True
except ImportError:
    has_scipy_shift = False
    _logger.info("no scipy.ndimage.shift detected, will use numpy.fft instead")


def shift_img(
    data: numpy.ndarray,
    dx: float,
    dy: float,
    cval: float = 0.0,
    use_scipy=True,
) -> numpy.ndarray:
    """
    Apply simple 2d image shift in 'constant mode'.

    :param data:
    :param dx: x translation to be applied
    :param dy: y translation to be applied
    :param cval: value to replace the shifted values

    :return: shifted image
    """
    assert data.ndim == 2
    assert dx is not None
    assert dy is not None
    _logger.debug(f"apply shift dx={dx}, dy={dy} ")

    if use_scipy and has_scipy_shift:
        return shift_scipy(
            input=data, shift=(dy, dx), order=1, mode="constant", cval=cval
        )
    else:
        if use_scipy:
            _logger.warning(
                "scipy not installed. Will shift image from local shift routine"
            )
        ynum, xnum = data.shape
        xmin = int(-numpy.fix(xnum / 2))
        xmax = int(numpy.ceil(xnum / 2) - 1)
        ymin = int(-numpy.fix(ynum / 2))
        ymax = int(numpy.ceil(ynum / 2) - 1)

        nx, ny = numpy.meshgrid(
            numpy.linspace(xmin, xmax, xnum), numpy.linspace(ymin, ymax, ynum)
        )
        # cast variables to float
        ny = numpy.asarray(ny, numpy.float32)
        nx = numpy.asarray(nx, numpy.float32)
        res = abs(
            numpy.fft.ifft2(
                numpy.fft.fft2(data)
                * numpy.exp(1.0j * 2.0 * numpy.pi * (-dy * ny / ynum + -dx * nx / xnum))
            )
        )

        # apply constant filter
        if dx > 0:
            res[:, 0 : int(numpy.ceil(dx))] = cval
        elif dx < 0:
            res[:, xnum + int(numpy.ceil(dx)) :] = cval
        return res


class ImageScaleMethod(enum.Enum):
    RAW = "raw"
    MEAN = "mean"
    MEDIAN = "median"


def scale_img2_to_img1(
    img_1: numpy.array,
    img_2: numpy.array,
    method: ImageScaleMethod = ImageScaleMethod.MEAN,
):
    """
    scale image2 relative to image 1 in such a way they have same min and
    max. Scale will be apply from and to 'data' / raw data

    :param img_1: reference image
    :param img_2: image to scale
    :param method: method to apply scaling
    :return:
    """
    assert method in ImageScaleMethod
    assert img_1.ndim == 2
    assert img_2.shape == img_1.shape
    min1 = img_2.min()
    max1 = img_2.max()
    min0 = img_1.min()
    max0 = img_1.max()

    if method is ImageScaleMethod.RAW:
        a = (min0 - max0) / (min1 - max1)
        b = (min1 * max0 - min0 * max1) / (min1 - max1)
        return a * img_2 + b
    else:
        if method is ImageScaleMethod.MEAN:
            me0 = img_1.mean()
            me1 = img_2.mean()
        elif method is ImageScaleMethod.MEDIAN:
            me0 = img_1.median()
            me1 = img_2.median()
        else:
            raise ValueError("method not managed", method)

        vec0 = numpy.asmatrix([[min0], [me0], [max0]])
        matr = numpy.asmatrix(
            [[min1 * min1, min1, 1.0], [me1 * me1, me1, 1.0], [max1 * max1, max1, 1.0]]
        )
        vec1 = inv(matr) * vec0
        return (
            float(vec1[0]) * (img_2 * img_2) + float(vec1[1]) * img_2 + float(vec1[2])
        )

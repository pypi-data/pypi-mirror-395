import numpy
import pytest

from tomwer.core.utils.image import ImageScaleMethod, scale_img2_to_img1, shift_img


@pytest.mark.parametrize(
    "use_scipy, dx, dy, cval", ((True, 1.0, -2.3, 0), (False, 0.0, 3.6, 2))
)
def test_shift_image(use_scipy, dx, dy, cval):
    data = numpy.linspace(0, 12, 100 * 100).reshape(100, 100)
    assert isinstance(
        shift_img(data=data, dx=dx, dy=dy, cval=cval, use_scipy=use_scipy),
        numpy.ndarray,
    )


def test_scale_img2_to_img1():
    """
    test scale_img2_to_img1 function
    """
    img_1 = numpy.linspace(0, 10, 100 * 100, dtype=numpy.float16).reshape(100, 100)
    img_2 = numpy.linspace(20, 100, 100 * 100, dtype=numpy.float16).reshape(100, 100)

    rescale_img = scale_img2_to_img1(img_2, img_1, method=ImageScaleMethod.MEAN)
    numpy.testing.assert_array_almost_equal(
        img_2,
        rescale_img,
        decimal=1,
    )

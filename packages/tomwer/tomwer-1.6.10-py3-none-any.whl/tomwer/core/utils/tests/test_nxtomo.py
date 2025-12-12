# coding: utf-8

import pytest
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.utils.nxtomoutils import get_n_series


def test_get_n_series():
    """test tomwer.core.utils.nxtomoutils.get_n_series function"""
    array_1 = (
        [ImageKey.DARK_FIELD] * 2
        + [ImageKey.FLAT_FIELD]
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.FLAT_FIELD]
    )

    with pytest.raises(ValueError):
        get_n_series(array_1, ImageKey.INVALID)
    with pytest.raises(ValueError):
        get_n_series(array_1, 3)

    assert len(array_1) == 8
    assert get_n_series(array_1, ImageKey.DARK_FIELD) == 1
    assert get_n_series(array_1, ImageKey.FLAT_FIELD) == 2
    assert get_n_series(array_1, ImageKey.PROJECTION) == 1
    assert get_n_series(array_1, 0) == 1

    array_2 = (
        [ImageKey.FLAT_FIELD.value]
        + [ImageKey.PROJECTION.value] * 4
        + [ImageKey.INVALID.value] * 2
        + [ImageKey.PROJECTION.value] * 3
        + [ImageKey.FLAT_FIELD.value]
    )
    assert get_n_series(array_2, ImageKey.DARK_FIELD) == 0
    assert get_n_series(array_2, ImageKey.PROJECTION) == 1
    assert get_n_series(array_2, ImageKey.FLAT_FIELD) == 2

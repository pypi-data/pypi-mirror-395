from __future__ import annotations

import os
import pytest
import numpy
from tomwer.tests.conftest import nxtomo_scan_180  # noqa F811
from tomwer.core.process.drac.rawdataset import DracRawDataset


def test_IcatRawDataset(nxtomo_scan_180):  # noqa F811
    """
    test CreateRawDataScreenshotsTask task
    """
    # test nothing requested
    dataset = DracRawDataset(
        tomo_obj=nxtomo_scan_180,
        raw_projections_required=False,
        raw_darks_required=False,
        raw_flats_required=False,
    )

    assert not os.path.exists(dataset.get_gallery_dir())
    dataset.build_gallery()
    assert not os.path.exists(dataset.get_gallery_dir())

    # test only flat requested
    dataset = DracRawDataset(
        tomo_obj=nxtomo_scan_180,
        raw_projections_required=False,
        raw_darks_required=False,
        raw_flats_required=True,
    )
    dataset.build_gallery()
    assert len(os.listdir(dataset.get_gallery_dir())) == 1

    # test only dark requested
    dataset = DracRawDataset(
        tomo_obj=nxtomo_scan_180,
        raw_projections_required=False,
        raw_darks_required=True,
        raw_flats_required=False,
    )
    dataset.gallery_overwrite = False
    with pytest.raises(RuntimeError):
        dataset.build_gallery()
    dataset.gallery_overwrite = True
    dataset.build_gallery()
    assert len(os.listdir(dataset.get_gallery_dir())) == 1

    # test only projection requested
    dataset = DracRawDataset(
        tomo_obj=nxtomo_scan_180,
        raw_projections_required=True,
        raw_darks_required=False,
        raw_flats_required=False,
    )
    dataset.gallery_overwrite = True
    dataset.build_gallery()
    assert len(os.listdir(dataset.get_gallery_dir())) == 2

    # test all requested
    dataset = DracRawDataset(
        tomo_obj=nxtomo_scan_180,
        raw_projections_required=True,
        raw_darks_required=True,
        raw_flats_required=True,
        raw_projections_each=10,
    )
    dataset.gallery_overwrite = True
    dataset.build_gallery()
    assert len(os.listdir(dataset.get_gallery_dir())) == 12


def test_select_angles():
    """test the select_angles function"""
    numpy.testing.assert_allclose(
        DracRawDataset.select_angles(
            numpy.linspace(start=-20, stop=40, num=201, endpoint=True), each_angle=20
        ),
        numpy.array([-20, 0.1, 19.9, 40]),
    )

    assert DracRawDataset.select_angles((), each_angle=20) == ()
    assert DracRawDataset.select_angles((10,), each_angle=10) == (10,)
    angles = DracRawDataset.select_angles(
        numpy.linspace(start=0, stop=10, num=400, endpoint=False), each_angle=1
    )
    assert len(angles) == 11
    assert numpy.isclose(angles[0], 0, atol=0.1)
    assert numpy.isclose(angles[-1], 10, atol=0.1)

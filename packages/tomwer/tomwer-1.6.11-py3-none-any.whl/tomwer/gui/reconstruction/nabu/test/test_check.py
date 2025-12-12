# coding: utf-8
from __future__ import annotations


import os

import pytest
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo
from tomwer.gui.reconstruction.nabu import check


def test_check_dark_series(tmpdir):
    """test check.check_dark_series function"""
    full_edf_path = os.path.join(tmpdir, "my", "aquisition", "folder")
    MockEDF.fastMockAcquisition(full_edf_path)
    edf_scan = EDFTomoScan(full_edf_path)
    with pytest.raises(TypeError):
        assert check.check_dark_series(edf_scan)

    full_hdf5_scan = os.path.join(tmpdir, "hdf5_scan")
    scan = MockNXtomo(
        scan_path=full_hdf5_scan,
        n_proj=20,
        n_ini_proj=20,
        dim=10,
    ).scan
    scan._image_keys = (
        [ImageKey.DARK_FIELD] * 2
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.DARK_FIELD] * 2
    )
    assert check.check_dark_series(scan, logger=None, user_input=False) is False
    scan._image_keys = [ImageKey.DARK_FIELD] * 2 + [ImageKey.PROJECTION] * 4
    assert check.check_dark_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.PROJECTION] * 4
    assert check.check_dark_series(scan, logger=None, user_input=False) is False


def test_check_flat_series(tmpdir):
    """test check.check_flat_series function"""
    full_edf_path = os.path.join(tmpdir, "my", "aquisition", "folder")
    MockEDF.fastMockAcquisition(full_edf_path)
    edf_scan = EDFTomoScan(full_edf_path)
    with pytest.raises(TypeError):
        assert check.check_flat_series(edf_scan)

    full_hdf5_scan = os.path.join(tmpdir, "hdf5_scan")
    scan = MockNXtomo(
        scan_path=full_hdf5_scan,
        n_proj=20,
        n_ini_proj=20,
        dim=10,
    ).scan
    scan._image_keys = (
        [ImageKey.FLAT_FIELD] * 2
        + [ImageKey.PROJECTION] * 4
        + [ImageKey.FLAT_FIELD] * 2
    )
    assert check.check_flat_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.FLAT_FIELD] * 2 + [ImageKey.PROJECTION] * 4
    assert check.check_flat_series(scan, logger=None, user_input=False) is True
    scan._image_keys = [ImageKey.PROJECTION] * 4
    assert check.check_flat_series(scan, logger=None, user_input=False) is False

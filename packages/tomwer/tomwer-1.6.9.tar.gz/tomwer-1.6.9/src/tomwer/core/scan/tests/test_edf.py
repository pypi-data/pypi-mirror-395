# coding: utf-8
from __future__ import annotations

import os

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.utils.scanutils import MockEDF


def test_scan_dir(tmpdir):
    full_path = os.path.join(tmpdir, "my", "aquisition", "folder")
    MockEDF.fastMockAcquisition(full_path)
    scan = EDFTomoScan(full_path)
    assert scan.scan_dir_name() == "folder"
    assert scan.scan_basename() == full_path


def test_working_directory():
    """test behavior of the working directory function"""
    scan = EDFTomoScan(scan=None)
    assert scan.working_directory is None
    scan = EDFTomoScan(scan="my_folder")
    assert str(scan.working_directory) == os.path.abspath("my_folder")
    scan = EDFTomoScan(scan="/full/path/to/my/folder")
    assert str(scan.working_directory) == os.path.abspath("/full/path/to/my/folder")

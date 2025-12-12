# coding: utf-8
from __future__ import annotations

from tomwer.core.process.reconstruction.darkref.darkrefs import (
    requires_reduced_dark_and_flat,
)
from tomwer.core.utils.scanutils import MockEDF, MockNXtomo


def test_quick_run_necessary_edf(tmpdir):
    """test the `quick_run_necessary` function for EDFTomoScan"""
    scan = MockEDF.mockScan(scanID=str(tmpdir), start_dark=True, start_flat=True)
    assert scan.reduced_darks in (None, {})
    assert scan.reduced_flats in (None, {})
    requires_reduced_dark_and_flat(scan=scan)
    assert len(scan.reduced_darks) == 1
    assert len(scan.reduced_flats) == 1


def test_quick_run_necessary_hdf5(tmpdir):
    """test the `quick_run_necessary` function for NXtomoScan"""
    scan = MockNXtomo(
        scan_path=tmpdir,
        n_proj=20,
        n_ini_proj=20,
        dim=10,
    ).scan
    assert scan.reduced_darks in (None, {})
    assert scan.reduced_flats in (None, {})
    computed = requires_reduced_dark_and_flat(scan=scan)
    assert len(computed) == 2
    assert len(scan.reduced_darks) == 1
    assert len(scan.reduced_flats) == 1

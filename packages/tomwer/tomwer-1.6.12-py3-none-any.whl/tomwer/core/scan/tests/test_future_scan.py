# coding: utf-8

"""Unit test for the scan defined at the hdf5 format"""
from __future__ import annotations

import asyncio
import os

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import MockNXtomo


def test_simple_future_tomo_obj(tmpdir):
    """Simple test of the FutureTomwerScan API"""
    scan = MockNXtomo(
        scan_path=os.path.join(tmpdir, "scan_test"),
        n_proj=10,
        n_ini_proj=10,
        create_ini_dark=False,
        create_ini_flat=False,
        dim=10,
    ).scan
    future = asyncio.Future()
    future.set_result(None)

    future_tomo_obj = FutureTomwerObject(
        tomo_obj=scan,
        futures=[
            future,
        ],
    )

    future_tomo_obj.results()
    assert future_tomo_obj.exceptions() is None
    assert future_tomo_obj.cancelled() is False

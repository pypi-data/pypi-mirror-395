from tomwer.tests.conftest import qtapp  # noqa F401
import asyncio
import os

import pytest

from orangecontrib.tomwer.widgets.cluster.FutureSupervisorOW import FutureSupervisorOW
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_FutureSupervisorOW(
    qtapp,  # noqa F811
    tmp_path,
):
    window = FutureSupervisorOW()
    test_dir = tmp_path / "scans_folder"
    test_dir.mkdir()

    # set up scans
    scans = []
    future_tomo_objs = []
    for i in range(5):
        # create scan
        scan = MockNXtomo(
            scan_path=os.path.join(test_dir, f"scan_test{i}"),
            n_proj=10,
            n_ini_proj=10,
            create_ini_dark=False,
            create_ini_flat=False,
            dim=10,
        ).scan
        scans.append(scan)

        # create future
        future = asyncio.Future()
        if i == 1:
            future.set_result(None)
        future_tomo_objs.append(
            FutureTomwerObject(
                tomo_obj=scan,
                futures=(future,),
            )
        )

    window.close()

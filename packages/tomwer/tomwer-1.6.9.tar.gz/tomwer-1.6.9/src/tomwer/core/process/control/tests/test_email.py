import os
import numpy
from tomwer.core.process.control.emailnotifier import format_email_info, _ls_tomo_obj
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.utils.scanutils import HDF5MockContext


def test__ls_tomo_obj(tmp_path):
    """simple test of the `_ls_tomo_obj` function"""
    for i in range(2):
        open(os.path.join(tmp_path, f"{i}.nx"), "a").close()

    scan = NXtomoScan(
        scan=os.path.join(tmp_path, "1.nx"),
        entry="entry0000",
    )
    assert isinstance(scan, NXtomoScan)

    assert len(_ls_tomo_obj(scan)) == 2

    volume = HDF5Volume(
        file_path=os.path.join(tmp_path, "myvolume.hdf5"),
        data_path="myvolume",
        data=numpy.linspace(0, 10, 100 * 100 * 3).reshape(  # pylint: disable=E1121
            3, 100, 100
        ),
    )
    volume.save()
    assert len(_ls_tomo_obj(volume)) == 3


def test_format_email_info(tmp_path):
    """
    simple test of formatting some information related to an email
    """
    with HDF5MockContext(
        scan_path=os.path.join(tmp_path, "test", "scan"), n_proj=100
    ) as scan:
        res = format_email_info(
            my_str="{tomo_obj_short_id} \n {tomo_obj_id} \n {ls_tomo_obj} \n {timestamp} \n {footnote}",
            tomo_obj=scan,
        )

        for keyword in (
            "{tomo_obj_short_id}",
            "{tomo_obj_id}",
            "{ls_tomo_obj}",
            "{timestamp}",
            "{footnote}",
        ):
            assert keyword not in res

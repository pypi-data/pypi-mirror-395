import os

from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import format_output_location


def test_format_output_location(tmp_path):
    """
    test different use cases of 'format_output_location'
    """
    bliss_raw_dir = tmp_path / "raw"
    bliss_raw_dir.mkdir()
    bliss_sample_dir = bliss_raw_dir / "sample"
    bliss_sample_dir.mkdir()
    bliss_master_file = bliss_sample_dir / "dataset.h5"

    bliss_proposal_file = bliss_raw_dir / "ihsample.h5"
    bliss_proposal_file = os.path.abspath(bliss_proposal_file)

    bliss_scan = BlissScan(
        master_file=bliss_master_file, entry="1.1", proposal_file=bliss_proposal_file
    )
    expected_path = os.path.join(tmp_path, "reduced", "sample")
    assert (
        format_output_location(
            location="{scan_parent_dir_basename}/../reduced/{scan_dir_name}",
            scan=bliss_scan,
        )
        == expected_path
    )

    edf_scan = EDFTomoScan("/test/my/folder/")
    assert (
        format_output_location(
            location="{scan_parent_dir_basename}/output", scan=edf_scan
        )
        == "/test/my/output"
    )

    hdf5_scan = NXtomoScan("/ddsad/my/file.hdf5", entry="nxtomos/entry0000")
    assert (
        format_output_location(location="{scan_basename}/output.nx", scan=hdf5_scan)
        == "/ddsad/my/output.nx"
    )
    assert format_output_location(
        location="{scan_file_name}/{scan_entry}.nx", scan=hdf5_scan
    ) == os.path.abspath("file/nxtomos_entry0000.nx")

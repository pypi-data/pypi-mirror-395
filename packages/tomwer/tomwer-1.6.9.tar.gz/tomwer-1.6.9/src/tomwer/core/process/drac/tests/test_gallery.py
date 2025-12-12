from tomwer.core.process.drac.gallery import (
    deduce_dataset_gallery_location,
    deduce_proposal_GALLERY_location,
    PROPOSAL_GALLERY_DIR_NAME,
)
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan


def test_deduce_dataset_gallery_dir():
    """test the deduce_gallery_dir function"""
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/my_scan.nx", entry="entry")
        )
        == "/path/to/PROCESSED_DATA/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/path/to/RAW_DATA/collection/my_scan.nx", entry="entry")
        )
        == "/path/to/PROCESSED_DATA/collection/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            NXtomoScan(scan="/any/random/path/my_scan.nx", entry="entry")
        )
        == "/any/random/path/gallery"
    )
    assert (
        deduce_dataset_gallery_location(
            EDFTomoScan(scan="/path/to/PROCESSED_DATA/dataset/toto")
        )
        == "/path/to/PROCESSED_DATA/dataset/toto/gallery"
    )
    assert (
        deduce_dataset_gallery_location(EDFTomoScan(scan="/path/to/dataset/toto"))
        == "/path/to/dataset/toto/gallery"
    )


def test_deduce_proposal_gallery_dir():
    """test the deduce_gallery_dir function"""
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/my_scan.nx", entry="entry")
        )
        == f"/path/to/{PROPOSAL_GALLERY_DIR_NAME}"
    )
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/path/to/PROCESSED_DATA/dataset/my_scan.nx", entry="entry")
        )
        == f"/path/to/{PROPOSAL_GALLERY_DIR_NAME}/dataset"
    )
    assert (
        deduce_proposal_GALLERY_location(
            NXtomoScan(scan="/any/random/path/my_scan.nx", entry="entry")
        )
        == f"/any/random/path/{PROPOSAL_GALLERY_DIR_NAME}"
    )
    assert (
        deduce_proposal_GALLERY_location(
            EDFTomoScan(scan="/path/to/PROCESSED_DATA/dataset/toto")
        )
        == "/path/to/GALLERY/dataset/toto"
    )
    assert (
        deduce_proposal_GALLERY_location(EDFTomoScan(scan="/path/to/dataset/toto"))
        == "/path/to/dataset/toto/GALLERY"
    )

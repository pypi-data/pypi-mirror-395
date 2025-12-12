from __future__ import annotations

import os

from nxtomomill.converter.hdf5.utils import PROCESSED_DATA_DIR_NAME, RAW_DATA_DIR_NAME

from tomwer.io.utils.raw_and_processed_data import to_processed_data_path
from tomwer.core.scan.scanbase import TomwerScanBase
from .output import DATASET_GALLERY_DIR_NAME, PROPOSAL_GALLERY_DIR_NAME

__all__ = ["deduce_dataset_gallery_location", "deduce_proposal_GALLERY_location"]


def deduce_dataset_gallery_location(scan_obj: TomwerScanBase) -> str:
    """
    From scan path deduce the 'dataset' path to the gallery.
    Warning: dataset gallery is different then the 'proposal' gallery
    """
    if not isinstance(scan_obj, TomwerScanBase):
        raise TypeError(f"'scan_obj' is expected to be an instance of {TomwerScanBase}")

    file_path = os.path.abspath(scan_obj.path)

    split_path = file_path.split(os.sep)
    # reverse it to find the lower level value of 'PROCESSED_DATA_DIR_NAME' or 'RAW_DATA_DIR_NAME' if by any 'chance' has several in the path
    # then we will replace the 'lower one' in the string. This is where the GALLERY will be added
    split_path = split_path[::-1]
    # check if already contain in a "PROCESSED_DATA" directory
    try:
        index_processed_data = split_path.index(PROCESSED_DATA_DIR_NAME)
    except ValueError:
        pass
        index_processed_data = None
    try:
        index_raw_data = split_path.index(RAW_DATA_DIR_NAME)
    except ValueError:
        # if the value is not in the list
        index_raw_data = None

    if index_processed_data is None and index_raw_data is None:
        # if not in any "PROCESSED_DATA" or "RAW_DATA" directory
        return scan_obj.get_relative_file(
            file_name=DATASET_GALLERY_DIR_NAME, with_dataset_prefix=False
        )
    elif index_processed_data is not None and index_raw_data is not None:
        if index_raw_data > index_processed_data:
            # if PROCESSED_DATA lower in the path than RAW_DATA
            split_path[index_processed_data] = RAW_DATA_DIR_NAME
    # reorder path to original
    split_path = list(split_path[::-1])
    split_path.append(DATASET_GALLERY_DIR_NAME)
    # move it to PROCESSED_DATA when possible
    path = os.sep.join(split_path)
    path = to_processed_data_path(path)
    return path


def deduce_proposal_GALLERY_location(scan_obj: TomwerScanBase) -> str:
    """
    Policy: look if the scan_obj.path is in 'PROCESSED_DATA_DIR_NAME' or 'RAW_DATA_DIR_NAME' directories.
    If find any (before any 'GALLERY_DIR_NAME' directory) replace it "GALLERY_DIR_NAME".
    If none of those are found then create it at the same level as the scan

    :param scan_obj: scan_obj for which we want the GALLERY directory
    :return: gallery path (to save screenshots for example)
    """
    if not isinstance(scan_obj, TomwerScanBase):
        raise TypeError(f"'scan_obj' is expected to be an instance of {TomwerScanBase}")

    file_path = os.path.abspath(scan_obj.path)

    split_path = file_path.split(os.sep)
    # reverse it to find the lower level value of 'PROCESSED_DATA_DIR_NAME' or 'RAW_DATA_DIR_NAME' if by any 'chance' has several in the path
    # then we will replace the 'lower one' in the string. This is where the GALLERY will be added
    split_path = split_path[::-1]
    # check if already contain in a "PROCESSED_DATA" directory
    try:
        index_processed_data = split_path.index(PROCESSED_DATA_DIR_NAME)
    except ValueError:
        pass
        index_processed_data = None
    try:
        index_raw_data = split_path.index(RAW_DATA_DIR_NAME)
    except ValueError:
        # if the value is not in the list
        index_raw_data = None

    if index_processed_data is None and index_raw_data is None:
        # if not in any "PROCESSED_DATA" or "RAW_DATA" directory
        return scan_obj.get_relative_file(
            file_name=PROPOSAL_GALLERY_DIR_NAME, with_dataset_prefix=False
        )
    elif index_processed_data is not None and index_raw_data is not None:
        if index_raw_data > index_processed_data:
            # if PROCESSED_DATA lower in the path than RAW_DATA
            split_path[index_processed_data] = PROPOSAL_GALLERY_DIR_NAME
        else:
            # if RAW_DATA lower in the path than PROCESSED_DATA
            split_path[index_raw_data] = PROPOSAL_GALLERY_DIR_NAME
    elif index_raw_data is not None:
        # if the path contains only PROCESSED_DATA or RAW_DATA (expected behavior for online acquistion)
        split_path[index_raw_data] = PROPOSAL_GALLERY_DIR_NAME
    else:
        assert index_processed_data is not None, "index_processed_data is None"
        split_path[index_processed_data] = PROPOSAL_GALLERY_DIR_NAME

    # reorder path to original
    split_path = split_path[::-1]
    return os.sep.join(split_path)

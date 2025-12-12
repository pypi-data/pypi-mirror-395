"""some utils to move a path to process_data or to raw_data"""

import os
from nxtomomill.converter.hdf5.utils import (
    RAW_DATA_DIR_NAME,
    PROCESSED_DATA_DIR_NAME,
)


def to_raw_data_path(file_path: str):
    """convert a path to 'RAW_DATA' when possible"""
    split_path = file_path.split(os.sep)
    # reverse it to find the lower level value of 'PROCESSED_DATA_DIR_NAME' if by any 'chance' has several in the path
    # in this case this is most likely what we want
    split_path = split_path[::-1]
    # check if already contain in a "RAW_DATA_DIR_NAME" directory
    try:
        index_raw_data = split_path.index(RAW_DATA_DIR_NAME)
    except ValueError:
        index_raw_data = None

    try:
        index_processed_data = split_path.index(PROCESSED_DATA_DIR_NAME)
    except ValueError:
        # if the value is not in the list
        pass
    else:
        if index_raw_data is None or index_raw_data > index_processed_data:
            # make sure we are not already in a 'PROCESSED_DATA' directory. Not sure it will never happen but safer
            split_path[index_processed_data] = RAW_DATA_DIR_NAME

    # reorder path to original
    split_path = split_path[::-1]
    return os.sep.join(split_path)


def to_processed_data_path(file_path: str):
    """convert a path to 'PROCESSED_DATA' when possible"""
    split_path = file_path.split(os.sep)
    # reverse it to find the lower level value of '_RAW_DATA_DIR_NAME' if by any 'chance' has several in the path
    # in this case this is most likely what we want
    split_path = split_path[::-1]
    # check if already contain in a "PROCESSED_DATA" directory
    try:
        index_processed_data = split_path.index(PROCESSED_DATA_DIR_NAME)
    except ValueError:
        index_processed_data = None

    try:
        index_raw_data = split_path.index(RAW_DATA_DIR_NAME)
    except ValueError:
        # if the value is not in the list
        pass
    else:
        if index_processed_data is None or index_raw_data < index_processed_data:
            # make sure we are not already in a 'PROCESSED_DATA' directory. Not sure it will never happen but safer
            split_path[index_raw_data] = PROCESSED_DATA_DIR_NAME

    # reorder path to original
    split_path = split_path[::-1]
    return os.sep.join(split_path)


def file_is_on_processed_data(file_path: str):
    """Util that raises an error if path is not in PROCESSED_DATA folder"""
    split_path = file_path.split(os.sep)
    # reverse it to find the lower level value of 'PROCESSED_DATA_DIR_NAME' if by any 'chance' has several in the path
    # in this case this is most likely what we want
    split_path = split_path[::-1]
    # check if already contain in a "RAW_DATA_DIR_NAME" directory
    try:
        index_raw_data = split_path.index(RAW_DATA_DIR_NAME)
    except ValueError:
        index_raw_data = None

    try:
        index_processed_data = split_path.index(PROCESSED_DATA_DIR_NAME)
    except ValueError:
        # if the value is not in the list
        index_processed_data = None
    else:
        if index_raw_data is not None and index_raw_data < index_processed_data:
            return False
    return index_processed_data is not None

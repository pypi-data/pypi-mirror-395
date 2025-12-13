from __future__ import annotations

import os
from enum import Enum
import warnings


class ProcessDataOutputDirMode(Enum):
    IN_SCAN_FOLDER = "same folder as scan"
    PROCESSED_DATA_FOLDER = "PROCESSED_DATA folder"
    OTHER = "other"

    @classmethod
    def from_value(cls, value):
        # ensure backward compatibility
        if value == "near input":
            return cls.IN_SCAN_FOLDER
        elif value == "processed data dir":
            return cls.PROCESSED_DATA_FOLDER
        elif value == "raw data dir":
            # Deprecation logic
            warnings.warn(
                "'RAW_DATA output' is deprecated since writing to 'RAW_DATA' folder is forbidden."
                "Redirecting to 'PROCESSED_DATA_FOLDER'.",
                DeprecationWarning,
                stacklevel=2,
            )
            return cls.PROCESSED_DATA_FOLDER
        return ProcessDataOutputDirMode(value)


class NabuOutputFileFormat(Enum):
    TIFF = "tiff"
    TIFF_3D = "tiff3d"
    HDF5 = "hdf5"
    JP2K = "jp2"
    EDF = "edf"
    RAW = "vol"

    @classmethod
    def from_value(cls, value):
        if isinstance(value, str):
            value = value.lstrip(".")
        return NabuOutputFileFormat(value)


def get_file_format(file_str):
    extension = os.path.splitext(file_str.lower())[-1]
    extension = extension.lstrip(".")
    if extension in ("tiff", "tif"):
        return NabuOutputFileFormat.TIFF
    elif extension in ("hdf5", "hdf", "h5"):
        return NabuOutputFileFormat.HDF5
    elif extension in ("jp2", "jp2k", "jpg2k"):
        return NabuOutputFileFormat.JP2K
    elif extension in ("edf",):
        return NabuOutputFileFormat.EDF
    elif extension in ("vol", "raw"):
        return NabuOutputFileFormat.RAW
    else:
        raise ValueError(f"Unrecognized file extension {extension} from {file_str}")

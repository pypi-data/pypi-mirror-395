from enum import Enum as _Enum


class ScanType(_Enum):
    BLISS = "bliss-hdf5"
    SPEC = "spec-edf"
    NX_TOMO = "NXtomo"

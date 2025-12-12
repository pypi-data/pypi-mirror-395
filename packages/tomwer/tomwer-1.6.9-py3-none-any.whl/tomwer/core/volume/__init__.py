"""contains volumes classes and function. Abstraction layer for scans, based on tomoscan volumes.
See https://gitlab.esrf.fr/tomotools/tomoscan
"""

from .edfvolume import EDFVolume  # noqa F401
from .hdf5volume import HDF5Volume  # noqa F401
from .jp2kvolume import JP2KVolume  # noqa F401
from .rawvolume import RawVolume  # noqa F401
from .tiffvolume import MultiTIFFVolume, TIFFVolume  # noqa F401

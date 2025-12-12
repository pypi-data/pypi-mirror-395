# coding: utf-8
"""
Applications and library for tomography processing.
Provides ewoks tasks, several GUI for nabu as several utils.
"""

from __future__ import absolute_import, division, print_function

from tomwer.core.log import processlog  # noqa F401
from tomwer.version import version as __version  # noqa F401

try:
    # try to first load hdf5plugin before h5py
    import hdf5plugin  # noqa F401
except ImportError:
    pass


__version__ = __version

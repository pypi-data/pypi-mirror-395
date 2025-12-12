from __future__ import annotations


import logging
from urllib.parse import urlparse

from tomoscan import identifier as _identifier_mod
from tomoscan.esrf.identifier.url_utils import split_path
from tomoscan.factory import Factory as _oVolumeFactory
from tomoscan.identifier import BaseIdentifier, ScanIdentifier, VolumeIdentifier

from tomwer.core.scan.edfscan import EDFTomoScan, EDFTomoScanIdentifier
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume import (
    EDFVolume,
    HDF5Volume,
    JP2KVolume,
    MultiTIFFVolume,
    RawVolume,
    TIFFVolume,
)
from tomwer.core.volume.edfvolume import EDFVolumeIdentifier
from tomwer.core.volume.hdf5volume import HDF5VolumeIdentifier
from tomwer.core.volume.jp2kvolume import JP2KVolumeIdentifier
from tomwer.core.volume.rawvolume import RawVolumeIdentifier
from tomwer.core.volume.tiffvolume import (
    MultiTiffVolumeIdentifier,
    TIFFVolumeIdentifier,
)
from tomwer.utils import docstring

_logger = logging.getLogger(__name__)


class VolumeFactory(_oVolumeFactory):
    @staticmethod
    def from_identifier_to_vol_urls(identifier) -> tuple | None:
        """
        convert an identifier to a volume
        and return all the existing url of this volume
        """
        try:
            vol = VolumeFactory.create_tomo_object_from_identifier(
                identifier=identifier
            )
        except Exception as e:
            _logger.error(e)
            return None
        else:
            return tuple(vol.browse_data_urls())

    @docstring(_oVolumeFactory.create_tomo_object_from_identifier)
    @staticmethod
    def create_tomo_object_from_identifier(
        identifier: str | BaseIdentifier,
    ) -> TomwerVolumeBase:
        """

        :param scan_path: path to the scan directory or file
        :param entry: entry on the file. Requested for hdf5 files
        :param accept_bliss_scan: if True the factory can return some BlissScan
                                  But this is only compatible with the
                                  Tomomill processing.
        :return: TomwerScanBase instance fitting the scan folder or scan path
        :raises: ValueError if scan_path is not containing a scan
        """
        if isinstance(identifier, BaseIdentifier):
            identifier = identifier.to_str()
        elif not isinstance(identifier, str):
            raise TypeError(
                f"identifier is expected to be a str or an instance of {BaseIdentifier} not {type(identifier)}"
            )

        # step 1: convert identifier to an instance of BaseIdentifier if necessary
        if isinstance(identifier, str):
            info = urlparse(identifier)
            paths = split_path(info.path)
            scheme = info.scheme
            if len(paths) == 1:
                # insure backward compatibility. Originally (until 0.8) there was only one type which was scan
                tomo_type = ScanIdentifier.TOMO_TYPE
            elif len(paths) == 2:
                tomo_type, _ = paths
            else:
                raise ValueError("Failed to parse path string:", info.path)

            if tomo_type == _identifier_mod.VolumeIdentifier.TOMO_TYPE:
                if scheme == "edf":
                    identifier = EDFVolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "hdf5":
                    identifier = HDF5VolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "tiff":
                    identifier = TIFFVolumeIdentifier.from_str(identifier=identifier)
                elif scheme == "tiff3d":
                    identifier = MultiTiffVolumeIdentifier.from_str(
                        identifier=identifier
                    )
                elif scheme == "jp2k":
                    identifier = JP2KVolumeIdentifier.from_str(identifier=identifier)
                elif scheme in ("raw", "vol"):
                    identifier = RawVolumeIdentifier.from_str(identifier=identifier)
                else:
                    raise ValueError(f"Scheme {scheme} is not recognized")

            elif tomo_type == _identifier_mod.ScanIdentifier.TOMO_TYPE:
                # otherwise consider this is a scan. Insure backward compatibility
                if scheme == "edf":
                    identifier = EDFTomoScanIdentifier.from_str(identifier=identifier)
                elif scheme == "hdf5":
                    identifier = HDF5VolumeIdentifier.from_str(identifier=identifier)
                else:
                    raise ValueError(f"Scheme {scheme} not recognized")
            else:
                raise ValueError(f"{tomo_type} is not an handled tomo type")

        # step 2: convert identifier to a TomoBaseObject
        assert isinstance(identifier, BaseIdentifier)
        scheme = identifier.scheme
        tomo_type = identifier.tomo_type

        if scheme == "edf":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return EDFVolume.from_identifier(identifier=identifier)
            elif tomo_type == ScanIdentifier.TOMO_TYPE:
                return EDFTomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        elif scheme == "hdf5":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return HDF5Volume.from_identifier(identifier=identifier)
            elif tomo_type == ScanIdentifier.TOMO_TYPE:
                return NXtomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        elif scheme == "jp2k":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return JP2KVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme == "tiff":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return TIFFVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme == "tiff3d":
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return MultiTIFFVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        elif scheme in ("raw", "vol"):
            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                return RawVolume.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError
        else:
            raise ValueError(f"Scheme {scheme} not recognized")

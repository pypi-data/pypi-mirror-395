from __future__ import annotations

import glob
import logging
import os
from urllib.parse import urlparse

import h5py
from tomoscan.esrf.identifier.url_utils import split_path
from tomoscan.factory import Factory as _oScanFactory
from tomoscan.identifier import BaseIdentifier, ScanIdentifier, VolumeIdentifier
from tomoscan.scanbase import TomoScanBase
from tomoscan.tomoobject import TomoObject
from nxtomo.application.nxtomo import NXtomo

from tomwer.utils import docstring

from .blissscan import BlissScan
from .edfscan import EDFTomoScan, EDFTomoScanIdentifier
from .hdf5scan import NXtomoScan, NXtomoScanIdentifier

_logger = logging.getLogger(__name__)


@docstring(_oScanFactory)
class ScanFactory(object):
    @docstring(_oScanFactory.create_scan_object)
    @staticmethod
    def create_tomo_object_from_identifier(
        identifier: str | BaseIdentifier,
    ) -> TomoObject:
        """
        Create an instance of TomoScanBase from his identifier if possible

        :param identifier: identifier of the TomoScanBase
        :raises: TypeError if identifier is not a str
        :raises: ValueError if identifier cannot be converted back to an instance of TomoScanBase
        """
        from tomoscan.identifier import BaseIdentifier as _TomoScanIdentifier

        if not isinstance(identifier, (str, BaseIdentifier, _TomoScanIdentifier)):
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

            if tomo_type == VolumeIdentifier.TOMO_TYPE:
                raise ValueError("This factory creates scan object and not volumes")

            elif tomo_type == ScanIdentifier.TOMO_TYPE:
                # otherwise consider this is a scan. Insure backward compatibility
                if scheme == "edf":
                    identifier = EDFTomoScanIdentifier.from_str(identifier=identifier)
                elif scheme == "hdf5":
                    identifier = NXtomoScanIdentifier.from_str(identifier=identifier)
                else:
                    raise ValueError(f"Scheme {scheme} not recognized")
            else:
                raise ValueError(f"{tomo_type} is not an handled tomo type")

        # step 2: convert identifier to a TomoBaseObject
        assert isinstance(identifier, BaseIdentifier)
        scheme = identifier.scheme
        tomo_type = identifier.tomo_type

        if scheme == "edf":
            if tomo_type == ScanIdentifier.TOMO_TYPE:
                return EDFTomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        elif scheme == "hdf5":
            if tomo_type == ScanIdentifier.TOMO_TYPE:
                return NXtomoScan.from_identifier(identifier=identifier)
            else:
                raise NotImplementedError()
        else:
            raise ValueError(f"Scheme {scheme} not recognized")

    @staticmethod
    def create_scan_object(
        scan_path: str, entry: str | None = None, accept_bliss_scan: bool = False
    ) -> TomoScanBase:
        """

        :param scan_path: path to the scan directory or file
        :param entry: entry on the file. Requested for hdf5 files
        :param accept_bliss_scan: if True the factory can return some BlissScan
                                  But this is only compatible with the
                                  Tomomill processing.
        :return: TomwerScanBase instance fitting the scan folder or scan path
        :raises: ValueError if scan_path is not containing a scan
        """
        if scan_path is None:
            raise ValueError("'scan_path' should be provided")
        if entry is not None and not entry.startswith("/"):
            entry = "/" + entry
        if os.path.isfile(scan_path) and ScanFactory.is_hdf5_tomo(scan_path):
            valid_entries = NXtomo.get_valid_entries(scan_path)
            if entry is None:
                if len(valid_entries) > 1:
                    _logger.warning(
                        "more than one entry found for %s."
                        "Pick the last entry" % scan_path
                    )
                entry = valid_entries[-1]
            elif entry not in valid_entries:
                raise ValueError(
                    f"entry {entry} is invalid. Does it exists ? Is the "
                    f"file NXTomo compliant ?. Valid entry are {valid_entries}"
                )
            return NXtomoScan(scan=scan_path, entry=entry)
        elif ScanFactory.is_edf_tomo(scan_path):
            return EDFTomoScan(scan=scan_path)
        elif accept_bliss_scan and BlissScan.is_bliss_file(scan_path):
            if entry is None:
                valid_entries = BlissScan.get_valid_entries(scan_path)
                if len(valid_entries) > 1:
                    _logger.warning(
                        f"more than one entry found for {scan_path}. Pick the last entry"
                    )
                entry = valid_entries[-1]
            return BlissScan(master_file=scan_path, entry=entry, proposal_file=None)

        raise ValueError(f"Unable to generate a scan object from {scan_path}")

    @docstring(_oScanFactory.create_scan_objects)
    @staticmethod
    def create_scan_objects(scan_path, accept_bliss_scan=True) -> tuple:
        scan_path = scan_path.rstrip(os.path.sep)
        if EDFTomoScan.is_tomoscan_dir(scan_path):
            return (EDFTomoScan(scan=scan_path),)
        elif NXtomoScan.is_tomoscan_dir(scan_path):
            scans = []
            master_file = NXtomoScan.get_master_file(scan_path=scan_path)
            entries = NXtomo.get_valid_entries(master_file)
            for entry in entries:
                scans.append(NXtomoScan(scan=scan_path, entry=entry, index=None))
            return tuple(scans)
        elif accept_bliss_scan and BlissScan.is_bliss_file(scan_path):
            scans = []
            for entry in BlissScan.get_valid_entries(scan_path):
                scans.append(
                    BlissScan(master_file=scan_path, entry=entry, proposal_file=None)
                )
            return tuple(scans)
        return tuple()

    @staticmethod
    def mock_scan(type_="edf"):
        """Mock a scan structure which is not associated to any real acquistion"""
        if type_ == "edf":
            return EDFTomoScan(scan=None)
        else:
            raise NotImplementedError("Other TomoScan are not defined yet")

    @staticmethod
    def create_scan_object_frm_dict(_dict):
        if TomoScanBase.DICT_TYPE_KEY not in _dict:
            raise ValueError(
                f"given dict is not recognized. Cannot find {TomoScanBase.DICT_TYPE_KEY}"
            )
        elif _dict[TomoScanBase.DICT_TYPE_KEY] == EDFTomoScan._TYPE:
            return EDFTomoScan(scan=None).load_from_dict(_dict)
        elif _dict[TomoScanBase.DICT_TYPE_KEY] == NXtomoScan._TYPE:
            return NXtomoScan.from_dict(_dict)
        else:
            raise ValueError(
                f"Scan type {_dict[TomoScanBase.DICT_TYPE_KEY]} is not managed"
            )

    @staticmethod
    def is_tomo_scandir(scan_path: str) -> bool:
        """

        :param scan_path: path to the scan directory or file
        :return: True if the given path / file is a tomo_scandir. For now yes by
                 default
        """
        return True

    @staticmethod
    def is_edf_tomo(scan_path: str) -> bool:
        """

        :param scan_path: path to the scan directory or file
        :return: True if given path define a tomo scan based on .edf file
        """
        if scan_path and os.path.isdir(scan_path):
            file_basename = os.path.basename(scan_path)
            has_info_file = (
                len(glob.glob(os.path.join(scan_path, file_basename + "*.info"))) > 0
            )
            not_lbs_scan_path = scan_path.replace("lbsram", "", 1)
            has_notlbsram_info_file = (
                len(
                    glob.glob(os.path.join(not_lbs_scan_path, file_basename + "*.info"))
                )
                > 0
            )
            if has_info_file or has_notlbsram_info_file:
                return True
        return False

    @staticmethod
    def is_hdf5_tomo(scan_path):
        """

        :param scan_path:
        :return:
        """
        if os.path.isfile(scan_path):
            return h5py.is_hdf5(scan_path)
        else:
            return NXtomoScan.directory_contains_scan(scan_path)

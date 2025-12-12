"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""

from __future__ import annotations

import logging
import os
import h5py
import tempfile

from silx.io.dictdump import dicttoh5, h5todict
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5
from tomoscan.esrf.scan.utils import (
    copy_h5_dict_darks_to,
    copy_h5_dict_flats_to,
    cwd_context,
)
from tomoscan.framereducer.target import REDUCER_TARGET
from tomoscan.io import HDF5File

from tomwer.core.process.reconstruction.darkref.darkrefs import DarkRefsTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import data_identifier_to_scan

logger = logging.getLogger(__name__)


class DarkRefsCopy(DarkRefsTask):
    """
    Reimplement Dark ref to deal with copy when there is no median/mean files
    """

    DEFAULT_SRCURRENT = 200.0  # mA

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        super().__init__(
            process_id=process_id,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        if inputs is None:
            inputs = {}

        self._mode_auto = inputs.get("mode_auto", True)
        if "savedir" in inputs:
            raise KeyError("savedir is not a valid key. Use save_dir")
        self._savedir = inputs.get("save_dir", tempfile.mkdtemp())
        self._save_file = self.get_save_file(self._savedir)
        self._darks_url = self.get_darks_url(self._savedir)
        self._flats_url = self.get_flats_url(self._savedir)
        logger.info(f"Flats and darks will be stored in {self._save_file}")

        self._processOnlyCopy = inputs.get("process_only_copy", False)
        self._processOnlyDkRf = inputs.get("process_only_dkrf", False)
        init_ref_scan = inputs.get("init_dkrf_from", None)
        if init_ref_scan:
            if not isinstance(init_ref_scan, TomwerScanBase):
                raise TypeError(
                    f"init_ref_scan is expected to be an instance of TomwerScanBase. Not {type(init_ref_scan)}"
                )
            else:
                self.set_darks_and_flats_from_scan(init_ref_scan)

    @staticmethod
    def get_save_file(save_dir):
        return os.path.join(save_dir, "darks_and_flats.h5")

    @staticmethod
    def get_flats_url(save_dir):
        return DataUrl(
            file_path=DarkRefsCopy.get_save_file(save_dir),
            data_path="/flats",
            scheme="silx",
        )

    @staticmethod
    def get_darks_url(save_dir):
        return DataUrl(
            file_path=DarkRefsCopy.get_save_file(save_dir),
            data_path="/darks",
            scheme="silx",
        )

    def set_process_only_dkRf(self, value: bool) -> None:
        self._processOnlyDkRf = value
        self._processOnlyCopy = False

    def set_process_only_copy(self, value: bool) -> None:
        self._processOnlyDkRf = False
        self._processOnlyCopy = value

    @staticmethod
    def get_reduced_frame_data(
        url: DataUrl, reduced_target: REDUCER_TARGET, check_for_reduced_key: bool = True
    ) -> tuple:
        """
        :param url: url expected to contain the dict with one key per serie of reduced frame
        :param reduced_target: what we are looking for (used when check_for_reduced_key is set to True)
        :param check_for_reduced_key: if True then if the dict contains the given key then return the value of this key instead
                                           of the loaded dict. Used as a user friendly feature to be able to load dict when upper data path
                                           is provided instead of the 'darks' or 'flats' one.
        :return: tuple as (data, metadata)
        """
        reduced_target = REDUCER_TARGET(reduced_target)

        with cwd_context(url.file_path()):
            try:
                reduced_info_dict = h5todict(
                    h5file=url.file_path(),
                    path=url.data_path(),
                )
            except Exception as e:
                logger.error(e)
                return None
            else:
                if check_for_reduced_key and reduced_target.value in reduced_info_dict:
                    return reduced_info_dict[reduced_target.value]
                else:
                    return reduced_info_dict

    @staticmethod
    def save_flats_to_be_copied(save_dir, data: DataUrl | dict):
        if isinstance(data, DataUrl):
            data = DarkRefsCopy.get_reduced_frame_data(url=data, reduced_target="flats")
        if data is None:
            return
        flat_url = DarkRefsCopy.get_flats_url(save_dir)
        # remove group if already exists: else can end up by copying several dark / flat from different datasets
        with HDF5File(flat_url.file_path(), mode="a") as h5f:
            if flat_url.data_path() in h5f:
                del h5f[flat_url.data_path()]
        dicttoh5(
            data,
            h5file=flat_url.file_path(),
            h5path=flat_url.data_path(),
            mode="a",
            update_mode="replace",
        )

    @staticmethod
    def save_darks_to_be_copied(save_dir, data: DataUrl | dict):
        if isinstance(data, DataUrl):
            data = DarkRefsCopy.get_reduced_frame_data(url=data, reduced_target="darks")
        if data is None:
            return
        dark_url = DarkRefsCopy.get_darks_url(save_dir)
        # remove group if already exists: else can end up by copying several dark / flat from different datasets
        with HDF5File(dark_url.file_path(), mode="a") as h5f:
            if dark_url.data_path() in h5f:
                del h5f[dark_url.data_path()]
        dicttoh5(
            data,
            h5file=dark_url.file_path(),
            h5path=dark_url.data_path(),
            mode="a",
            update_mode="replace",
        )

    def clear_cache(self):
        """
        remove the file used to cache the reduced darks / flats.
        This can be used in the case it contain unrelevant data. Like frame with another shape...
        """
        cache_file = DarkRefsCopy.get_save_file(self._savedir)
        if os.path.exists(cache_file):
            os.remove(cache_file)

    def _clear_cache_data_path(self, file_path: str, data_path: str):
        if not os.path.exists(file_path):
            return
        with h5py.File(file_path, mode="a") as h5f:
            if data_path in h5f:
                del h5f[data_path]

    def set_darks_and_flats_from_scan(self, scan: TomwerScanBase) -> bool:
        has_flats = scan.reduced_flats not in (None, {})
        has_darks = scan.reduced_darks not in (None, {})
        if has_flats and has_darks:
            # if the scan has darks and flats remove directly the cache file
            # else in append mode HDF5 is not removing the dataset and
            # the cache size will continue to increase
            self.clear_cache()
        if not has_flats:
            logger.warning(f"No flat found for {scan}. Unable to copy them")
        else:
            self._clear_cache_data_path(
                file_path=self._flats_url.file_path(),
                data_path=self._flats_url.data_path(),
            )
            dicttoh5(
                scan.reduced_flats,
                h5file=self._flats_url.file_path(),
                h5path=self._flats_url.data_path(),
                mode="a",
                update_mode="replace",
            )
        if not has_darks:
            logger.warning(f"No dark found for {scan}. Unable to copy them")
        else:
            self._clear_cache_data_path(
                file_path=self._darks_url.file_path(),
                data_path=self._darks_url.data_path(),
            )
            dicttoh5(
                scan.reduced_darks,
                h5file=self._darks_url.file_path(),
                h5path=self._darks_url.data_path(),
                mode="a",
                update_mode="replace",
            )
        self._ref_has_been_set(scan=scan)

    def _ref_has_been_set(self, scan):
        pass

    def _copy_to(self, scan):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"{scan} is expected to be an instance of {TomwerScanBase} and not {type(scan)}"
            )

        if self.has_dark_stored():
            copy_h5_dict_darks_to(
                scan=scan,
                darks_url=self._darks_url,
                save=True,
                raise_error_if_url_empty=True,
                overwrite=True,
            )
        if self.has_flat_stored():
            copy_h5_dict_flats_to(
                scan=scan,
                flats_url=self._flats_url,
                save=True,
                raise_error_if_url_empty=True,
                overwrite=True,
            )

    def run(self):
        """
        This is function triggered when a new scan / data is received.
        As explained in issue #184 the behavior is the following:

        * if the scan has already ref files files won't be overwrite
        * if the mode is in `auto` will register last ref file met
        * if the scan has no ref files and refCopy has some register. Will
          create a copy of those, normalized from srCurrent (for flat field)
        """
        scan = data_identifier_to_scan(self.inputs.data)
        if not isinstance(scan, (type(None), TomwerScanBase, dict)):
            raise TypeError(
                f"self.inputs.data is expected to be an instance "
                f"of None, TomwerScanBase or dict. Not {type(scan)}"
            )
        if scan is None or scan.path is None:
            return
        # process dark and ref calculation
        if not self._processOnlyCopy:
            super().run()
        # then copy if necessary
        if not self._processOnlyDkRf:
            if self.contains_dark_or_ref(scan):
                if self.is_on_mode_auto:
                    self.set_darks_and_flats_from_scan(scan)
            if self.has_missing_dark_or_ref(scan):
                self._copy_to(scan)

    def has_flat_or_dark_stored(self) -> bool:
        """

        :return: True if the process has at least registered one flat or one
                 dark
        """
        return self.has_flat_stored() or self.has_dark_stored()

    def has_flat_stored(self) -> bool:
        """

        :return: True if the process has registered at least one ref
        """
        if not os.path.exists(self._save_file):
            return False
        else:
            with open_hdf5(self._save_file) as h5f:
                return self._flats_url.data_path() in h5f

    def has_dark_stored(self) -> bool:
        """

        :return: True if the process has registered at least one dark
        """
        if not os.path.exists(self._save_file):
            return False
        else:
            with open_hdf5(self._save_file) as h5f:
                return self._darks_url.data_path() in h5f

    def contains_dark(self, scan: TomwerScanBase) -> bool:
        """Return True if the scan has already some dark processed"""
        if not isinstance(scan, TomwerScanBase):
            return TypeError(
                f"scan is expected to be an instance of {TomwerScanBase} and not {type(scan)}"
            )
        else:
            return scan.reduced_darks or scan.load_reduced_darks()

    def contains_flat(self, scan: TomwerScanBase):
        """Return True if the scan has already some dark processed"""
        if not isinstance(scan, TomwerScanBase):
            return TypeError(
                f"scan is expected to be an instance of {TomwerScanBase} and not {type(scan)}"
            )
        else:
            return scan.reduced_flats or scan.load_reduced_flats()

    def contains_dark_or_ref(self, scan):
        return self.contains_dark(scan=scan) or self.contains_flat(scan=scan)

    def has_missing_dark_or_ref(self, scan: TomwerScanBase) -> bool:
        """return True if the scan has no ref or no dark registered"""
        assert isinstance(scan, TomwerScanBase)
        return not self.contains_dark(scan) or not self.contains_flat(scan)

    def _signal_done(self, scan):
        assert isinstance(scan, TomwerScanBase)
        raise NotImplementedError("Abstract class")

    def set_mode_auto(self, b):
        self._mode_auto = b

    @property
    def is_on_mode_auto(self):
        return self._mode_auto

    @property
    def refHST_prefix(self):
        return self._refHstPrefix

    @property
    def darkHST_prefix(self):
        return self._darkHstPrefix

    def set_refHST_prefix(self, prefix):
        self._refHstPrefix = prefix

    def set_darkHST_prefix(self, prefix):
        self._darkHstPrefix = prefix

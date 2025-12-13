from __future__ import annotations

import logging
import os

import h5py
from nxtomomill.settings import Tomo
from silx.io.utils import h5py_read_dataset
from silx.io.utils import open as open_hdf5

H5_INIT_TITLES = Tomo.H5.INIT_TITLES

H5_ZSERIE_INIT_TITLES = Tomo.H5.ZSERIE_INIT_TITLES

H5_PCOTOMO_INIT_TITLES = Tomo.H5.PCOTOMO_INIT_TITLES

H5_BACK_AND_FORTH_INIT_TITLES = Tomo.H5.BACK_AND_FORTH_INIT_TITLES


_logger = logging.getLogger(__name__)


class BlissScan:
    """Simple class to define a Bliss sequence aka as Bliss scan inside tomwer.

    :warning: BlissScan is not compatible with tomwer treatment. This is
        why it does not inherit from TomwerScanBase. This is a utility class.
    """

    _TYPE = "bliss_hdf5"

    def __init__(
        self, master_file, entry, proposal_file, scan_numbers=None, saving_file=None
    ):
        self._master_file = master_file
        if isinstance(entry, str) and not entry.startswith("/"):
            self._entry = "/" + entry
        else:
            self._entry = entry
        self._proposal_file = proposal_file
        self._scan_numbers = scan_numbers or []
        self._saving_file = saving_file
        self._tomo_n = None
        self._n_acquired = None
        self._dir_path = os.path.dirname(self.master_file)

    @property
    def tomo_n(self):
        """total number of projections"""
        return self._tomo_n

    @property
    def proposal_file(self):
        return self._proposal_file

    @property
    def saving_file(self):
        return self._saving_file

    @tomo_n.setter
    def tomo_n(self, n):
        self._tomo_n = n

    @property
    def n_acquired(self):
        """
        number of frame acquired until now. Does not take into account
        dark, flats or alignment"""
        return self._n_acquired

    @n_acquired.setter
    def n_acquired(self, n):
        self._n_acquired = n

    @property
    def master_file(self):
        return self._master_file

    @property
    def entry(self):
        return self._entry

    @property
    def path(self):
        return self._dir_path

    @property
    def scan_numbers(self):
        return self._scan_numbers

    def add_scan_number(self, scan_number):
        self._scan_numbers.append(scan_number)

    def __str__(self):
        return self.get_id_name(master_file=self.master_file, entry=self.entry)

    @staticmethod
    def get_id_name(master_file, entry):
        return "@".join((str(entry), master_file))

    def _deduce_transfert_scan(self, output_dir):
        new_master_file = os.path.join(
            output_dir,
            os.path.basename(os.path.dirname(self.master_file)),
            os.path.basename(self.master_file),
        )
        new_proposal_file = os.path.join(
            output_dir, os.path.basename(self.proposal_file)
        )
        return BlissScan(
            master_file=new_master_file,
            proposal_file=new_proposal_file,
            entry=self.entry,
        )

    @staticmethod
    def is_bliss_file(file_path):
        return len(BlissScan.get_valid_entries(file_path)) > 0

    def is_abort(self, *args, **kwargs):
        # for now there is not real way to know if a scan is abort or not
        return False

    def scan_dir_name(self) -> str | None:
        """for 'this/is/my/acquisition' returns 'acquisition'"""
        if self.path is not None:
            return self.path.split(os.sep)[-1]
        else:
            return None

    def scan_basename(self) -> str | None:
        """for 'this/is/my/acquisition' returns 'acquisition'"""
        if self.path is not None:
            return self.path
        else:
            return None

    def scan_parent_dir_basename(self) -> str | None:
        if self.path is not None:
            try:
                return os.path.dirname(self.path)
            except Exception:
                return None
        else:
            return None

    @staticmethod
    def is_bliss_valid_entry(file_path: str, entry: str):
        def is_pcotmo_tomo(current_title: str):
            for title in H5_PCOTOMO_INIT_TITLES:
                if current_title.startswith(title):
                    return True
            return False

        def is_standard_tomo(current_title: str):
            for title in H5_INIT_TITLES:
                if current_title.startswith(title):
                    return True
            return False

        def is_zseries_tomo(current_title: str):
            for title in H5_ZSERIE_INIT_TITLES:
                if current_title.startswith(title):
                    return True
            return False

        def is_back_and_forth_tomo(current_title: str):
            for title in H5_BACK_AND_FORTH_INIT_TITLES:
                if current_title.startswith(title):
                    return True
                return False

        with open_hdf5(file_path) as h5s:
            if not isinstance(h5s, h5py.Group) or not isinstance(
                h5s[entry], h5py.Group
            ):
                return False
            if "title" in h5s[entry]:
                title = h5py_read_dataset(h5s[entry]["title"])
                try:
                    return (
                        is_standard_tomo(title)
                        or is_zseries_tomo(title)
                        or is_pcotmo_tomo(title)
                        or is_back_and_forth_tomo(title)
                    )
                except Exception:
                    pass
            return False

    @staticmethod
    def get_valid_entries(file_path) -> tuple:
        if not h5py.is_hdf5(file_path):
            _logger.warning("Provided file %s is not a hdf5 file" % file_path)
            return tuple()
        else:
            res = []
            with open_hdf5(file_path) as h5s:
                for entry in h5s:
                    if BlissScan.is_bliss_valid_entry(file_path=file_path, entry=entry):
                        res.append(entry)
            return tuple(res)

    def to_dict(self):
        return {
            "DICT_TYPE_KEY": self._TYPE,
            "master_file": self.master_file,
            "entry": self.entry,
            "proposal_file": self.proposal_file,
            "scan_numbers": self.scan_numbers,
        }

    @staticmethod
    def from_dict(ddict):
        master_file = ddict["master_file"]
        entry = ddict["entry"]
        return BlissScan(
            master_file=master_file, entry=entry, proposal_file=None
        ).load_frm_dict(ddict=ddict)

    def load_frm_dict(self, ddict):
        if "master_file" in ddict:
            self._master_file = ddict["master_file"]
        if "entry" in ddict:
            self._entry = ddict["entry"]
        if "proposal_file" in ddict:
            self._proposal_file = ddict["proposal_file"]
        if "scan_numbers" in ddict:
            self._scan_numbers = ddict["scan_numbers"]
        return self

# coding: utf-8
"""
Utils to mock scans
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any

import h5py
import numpy
from silx.io.utils import h5py_read_dataset
from tomoscan.esrf.scan.mock import MockEDF as _MockEDF
from tomoscan.esrf.scan.mock import MockNXtomo as _MockNXtomo
from tomoscan.io import HDF5File
from tomoscan.tests.utils import MockContext

from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.scanfactory import ScanFactory

_logger = logging.getLogger(__name__)


class MockNXtomo(_MockNXtomo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scan = NXtomoScan(scan=self.scan_master_file, entry="entry")


class MockEDF(_MockEDF):
    @staticmethod
    def mockScan(
        scanID,
        nRadio=5,
        nRecons=1,
        nPagRecons=0,
        dim=10,
        scan_range=360,
        n_extra_radio=0,
        start_dark=False,
        end_dark=False,
        start_flat=False,
        end_flat=False,
        start_dark_data=None,
        end_dark_data=None,
        start_flat_data=None,
        end_flat_data=None,
    ):
        """
        Create some random radios and reconstruction in the folder

        :param scanID: the folder where to save the radios and scans
        :param nRadio: The number of radios to create
        :param nRecons: the number of reconstruction to mock
        :param nRecons: the number of paganin reconstruction to mock
        :param dim: dimension of the files (nb row/columns)
        :param scan_range: scan range, usually 180 or 360
        :param n_extra_radio: number of radio run after the full range is made
                                  usually used to observe any sample movement
                                  during acquisition
        :param start_dark: do we want to create dark serie at start
        :param end_dark: do we want to create dark serie at end
        :param start_flat: do we want to create flat serie at start
        :param end_flat: do we want to create flat serie at end
        :param start_dark_data: if start_dark set to True Optional value for the dark serie. Else will generate some random values
        :param end_dark_data: if end_dark set to True Optional value for the dark serie. Else will generate some random values
        :param start_flat_data: if start_flat set to True Optional value for the flat serie. Else will generate some random values
        :param end_flat_data: if end_flat set to True Optional value for the flat serie. Else will generate some random values
        """
        assert type(scanID) is str
        assert type(nRadio) is int
        assert type(nRecons) is int
        assert type(dim) is int

        _MockEDF.fastMockAcquisition(
            folder=scanID,
            n_radio=nRadio,
            scan_range=scan_range,
            n_extra_radio=n_extra_radio,
        )
        _MockEDF.mockReconstruction(
            folder=scanID, nRecons=nRecons, nPagRecons=nPagRecons
        )

        if start_dark:
            _MockEDF.add_dark_series(
                scan_path=scanID, n_elmt=4, index=0, dim=dim, data=start_dark_data
            )
        if start_flat:
            _MockEDF.add_flat_series(
                scan_path=scanID, n_elmt=4, index=0, dim=dim, data=start_flat_data
            )
        if end_dark:
            _MockEDF.add_dark_series(
                scan_path=scanID,
                n_elmt=4,
                index=nRadio - 1,
                dim=dim,
                data=end_dark_data,
            )
        if end_flat:
            _MockEDF.add_flat_series(
                scan_path=scanID,
                n_elmt=4,
                index=nRadio - 1,
                dim=dim,
                data=end_flat_data,
            )
        return ScanFactory.create_scan_object(scanID)


class _BlissSample:
    """
    Simple mock of a bliss sample. For now we onyl create the hierarchy of
    files.
    """

    def __init__(
        self,
        sample_dir,
        sample_file,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        with_nx,
        detector_name="pcolinux",
    ):
        self.__sample_dir = sample_dir
        self.__sample_file = sample_file
        self.__n_sequence = n_sequence
        self.__n_scan_per_seq = n_scan_per_sequence
        self.__n_darks = n_darks
        self.__n_flats = n_flats
        self.__scan_folders = []
        self._index = 1
        self.__with_nx = with_nx
        self.__detector_name = detector_name
        self.__det_width = 256
        self.__det_height = 256
        self.__n_frame_per_scan = 100
        self.__energy = 19.0
        for _ in range(n_sequence):
            self.add_sequence()

    def get_next_free_index(self):
        idx = self._index
        self._index += 1
        return idx

    @staticmethod
    def get_title(scan_type):
        if scan_type == "dark":
            return "dark images"
        elif scan_type == "flat":
            return "reference images 1"
        elif scan_type == "projection":
            return "projections 1 - 2000"
        else:
            raise ValueError("Not implemented")

    def add_sequence(self):
        # reserve the index for the 'initialization' sequence. No scan folder
        # will be created for this one.
        seq_ini_index = self.get_next_free_index()

        # add sequence init information
        with h5py.File(self.sample_file, mode="a") as h5f:
            seq_node = h5f.require_group(str(seq_ini_index) + ".1")
            seq_node.attrs["NX_class"] = "NXentry"
            seq_node["title"] = "tomo:fullturn"
            # write energy
            seq_node["technique/scan/energy"] = self.__energy

        def register_scan_in_parent_seq(parent_index, scan_index):
            with h5py.File(self.sample_file, mode="a") as h5f:
                # write scan numbers
                seq_node = h5f.require_group(str(parent_index) + ".1")
                if "measurement/scan_numbers" in seq_node:
                    scan_numbers = h5py_read_dataset(
                        seq_node["measurement/scan_numbers"]
                    )
                    res = list(scan_numbers)
                    del seq_node["measurement/scan_numbers"]
                else:
                    res = []
                res.append(scan_index)
                seq_node["measurement/scan_numbers"] = numpy.asarray(res)

        def add_scan(scan_type):
            scan_idx = self.get_next_free_index()
            scan_name = str(scan_idx).zfill(4)
            scan_path = os.path.join(self.path, scan_name)
            self.__scan_folders.append(
                _BlissScan(folder=scan_path, scan_type=scan_type)
            )
            register_scan_in_parent_seq(parent_index=seq_ini_index, scan_index=scan_idx)
            # register the scan information
            with h5py.File(self.sample_file, mode="a") as h5f:
                seq_node = h5f.require_group(str(scan_idx) + ".1")
                # write title
                title = self.get_title(scan_type=scan_type)
                seq_node["title"] = title
                # write data
                data = (
                    numpy.random.random(
                        self.__det_height * self.__det_width * self.__n_frame_per_scan
                    )
                    * 256
                )
                data = data.reshape(
                    self.__n_frame_per_scan, self.__det_height, self.__det_width
                )
                data = data.astype(numpy.uint16)
                det_path_1 = "/".join(("instrument", self.__detector_name))
                det_grp = seq_node.require_group(det_path_1)
                det_grp["data"] = data
                det_grp.attrs["NX_class"] = "NXdetector"
                acq_grp = det_grp.require_group("acq_parameters")
                acq_grp["acq_expo_time"] = 4
                det_path_2 = "/".join(("technique", "scan", self.__detector_name))
                seq_node[det_path_2] = data
                seq_node.attrs["NX_class"] = "NXentry"
                # write rotation angle value and translations
                hrsrot_pos = seq_node.require_group(
                    "/".join(("instrument", "positioners"))
                )
                hrsrot_pos["hrsrot"] = numpy.random.randint(
                    low=0.0, high=360, size=self.__n_frame_per_scan
                )
                hrsrot_pos["sx"] = numpy.array(
                    numpy.random.random(size=self.__n_frame_per_scan)
                )
                hrsrot_pos["sy"] = numpy.random.random(size=self.__n_frame_per_scan)
                hrsrot_pos["sz"] = numpy.random.random(size=self.__n_frame_per_scan)

        if self.n_darks > 0:
            add_scan(scan_type="dark")

        if self.__n_flats > 0:
            add_scan(scan_type="flat")

        for i_proj_seq in range(self.__n_scan_per_seq):
            add_scan(scan_type="projection")

        # write end time
        with HDF5File(self.sample_file, mode="a") as h5f:
            h5f["/".join((str(seq_ini_index) + ".1", "end_time"))] = str(time.ctime())

        if self.__with_nx:
            nx_file = f"sample_{seq_ini_index:04}.nx"
            nx_file = os.path.join(self.path, nx_file)
            with h5py.File(nx_file, "a") as h5f:
                pass

    @property
    def path(self):
        return self.__sample_dir

    @property
    def sample_directory(self):
        return self.__sample_dir

    @property
    def sample_file(self):
        return self.__sample_file

    def scans_folders(self):
        return self.__scan_folders

    @property
    def n_darks(self):
        return self.__n_darks


class _BlissScan:
    """
    mock of a bliss scan
    """

    def __init__(self, folder, scan_type: str):
        assert scan_type in ("dark", "flat", "projection")
        self.__path = folder

    def path(self):
        return self.__path


class MockBlissAcquisition:
    """

    :param n_sequence: number of sequence to create
    :param n_scan_per_sequence: number of scans (projection series) per sequence
    :param n_projections_per_scan: number of projection frame in a scan
    :param n_darks: number of dark frame in the serie. Only one series at the
                    beginning
    :param n_flats: number of flats to create. In this case will only
                        create one series of n flats after dark if any
    :param output_dir: will contain the proposal file and one folder per
                           sequence.
    """

    def __init__(
        self,
        n_sample,
        n_sequence,
        n_scan_per_sequence,
        n_darks,
        n_flats,
        output_dir,
        with_nx=False,
    ):
        self.__folder = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.__proposal_file = os.path.join(self.__folder, "ihproposal_file.h5")

        # create sample
        self.__samples = []
        for sample_i in range(n_sample):
            dir_name = "_".join(("sample", str(sample_i)))
            sample_dir = os.path.join(self.path, dir_name)
            os.makedirs(sample_dir)
            sample_file = os.path.join(sample_dir, dir_name + ".h5")
            self.__samples.append(
                _BlissSample(
                    sample_dir=sample_dir,
                    sample_file=sample_file,
                    n_sequence=n_sequence,
                    n_scan_per_sequence=n_scan_per_sequence,
                    n_darks=n_darks,
                    n_flats=n_flats,
                    with_nx=with_nx,
                )
            )

    @property
    def samples(self):
        return self.__samples

    @property
    def proposal_file(self):
        # for now a simple file
        return self.__proposal_file

    @property
    def path(self):
        return self.__folder

    def create_bliss_scan(self):
        master_file = self.samples[0].sample_file
        assert os.path.exists(master_file)
        return BlissScan(
            master_file=master_file, entry="/1.1", proposal_file=self.__proposal_file
        )


class HDF5MockContext(MockContext, mock_class=MockNXtomo):
    """
    Util class to provide a context with a new Mock HDF5 file
    """

    def __init__(self, scan_path, n_proj, **kwargs):
        super().__init__(output_folder=os.path.dirname(scan_path))
        self._n_proj = n_proj
        self._mocks_params = kwargs
        self._scan_path = scan_path

    def __enter__(self):
        return MockNXtomo(
            scan_path=self._scan_path, n_proj=self._n_proj, **self._mocks_params
        ).scan


def data_identifier_to_scan(data_identifier: Any):
    """
    from a identifier (as str) try to create a scan.
    Mostly used when 'data' parameter is set from ewoks. In this case we expect it to be a (string) identifier
    """
    if isinstance(data_identifier, str):
        return ScanFactory.create_tomo_object_from_identifier(data_identifier)
    elif isinstance(data_identifier, dict):
        return ScanFactory.create_scan_object_frm_dict(data_identifier)
    else:
        return data_identifier


def format_output_location(location: str, scan):
    """
    format possible keys from the location like {scan_dir} or {scan_path}

    :param location:
    :param scan:
    :return:
    """
    if scan is None:
        _logger.warning("scan is !none, enable to format the nabu output location")

    keywords = {
        "scan_dir_name": scan.scan_dir_name(),
        "scan_basename": scan.scan_basename(),
        "scan_parent_dir_basename": scan.scan_parent_dir_basename(),
    }
    if isinstance(scan, NXtomoScan):
        keywords.update(
            {
                "scan_file_name": (
                    os.path.splitext(os.path.basename(scan.master_file))[0]
                    if scan.master_file is not None
                    else ""
                ),
                "scan_entry": (
                    scan.entry.replace("/", "_") if scan.entry is not None else ""
                ),
            }
        )
    elif isinstance(scan, EDFTomoScan):
        keywords.update(
            {
                "scan_file_name": "",
                "scan_entry": "",
            }
        )

    # filter necessary keywords
    def get_necessary_keywords():
        import string

        formatter = string.Formatter()
        return [field for _, field, _, _ in formatter.parse(location) if field]

    requested_keywords = get_necessary_keywords()

    def keyword_needed(pair):
        keyword, _ = pair
        return keyword in requested_keywords

    keywords = dict(filter(keyword_needed, keywords.items()))
    location = os.path.abspath(location.format(**keywords))
    return location

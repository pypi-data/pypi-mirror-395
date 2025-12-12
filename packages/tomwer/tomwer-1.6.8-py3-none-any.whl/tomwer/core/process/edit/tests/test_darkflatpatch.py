# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile
import unittest

import h5py
import numpy
from silx.io.url import DataUrl
from silx.io.utils import h5py_read_dataset
from tomoscan.esrf.scan.mock import MockNXtomo

from tomwer.core.process.edit.darkflatpatch import DarkFlatPatchTask
from tomwer.core.scan.nxtomoscan import NXtomoScan


class BaseTestAddDarkAndFlats(unittest.TestCase):
    """
    Unit test on nxtomomill.utils.add_dark_flat_nx_file function
    """

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp()
        simple_nx_path = os.path.join(self.tmpdir, "simple_case")
        self.dim = 55
        self.nproj = 20
        self._simple_nx = MockNXtomo(
            scan_path=simple_nx_path,
            n_proj=self.nproj,
            n_ini_proj=self.nproj,
            create_ini_dark=False,
            create_ini_flat=False,
            create_final_flat=False,
            dim=self.dim,
        ).scan
        with h5py.File(self._simple_nx.master_file, mode="r") as h5s:
            data_path = "/".join(
                (self._simple_nx.entry, "instrument", "detector", "data")
            )
            self._raw_data = h5py_read_dataset(h5s[data_path])
        nx_with_vds_path = os.path.join(self.tmpdir, "case_with_vds")
        self._nx_with_virtual_dataset = MockNXtomo(
            scan_path=nx_with_vds_path,
            n_proj=0,
            n_ini_proj=0,
            create_ini_dark=False,
            create_ini_flat=False,
            create_final_flat=False,
            dim=self.dim,
        ).scan
        self._create_vds(
            source_file=self._simple_nx.master_file,
            source_data_path=self._simple_nx.entry,
            target_file=self._nx_with_virtual_dataset.master_file,
            target_data_path=self._nx_with_virtual_dataset.entry,
            copy_other_data=True,
        )
        self._patch_nxtomo_flags(self._nx_with_virtual_dataset)

        nx_with_vds_path_and_links = os.path.join(
            self.tmpdir, "case_with_vds_and_links"
        )
        self._nx_with_virtual_dataset_with_link = MockNXtomo(
            scan_path=nx_with_vds_path_and_links,
            n_proj=0,
            n_ini_proj=0,
            create_ini_dark=False,
            create_ini_flat=False,
            create_final_flat=False,
            dim=self.dim,
        ).scan
        self._create_vds(
            source_file=self._simple_nx.master_file,
            source_data_path=self._simple_nx.entry,
            target_file=self._nx_with_virtual_dataset_with_link.master_file,
            target_data_path=self._nx_with_virtual_dataset_with_link.entry,
            copy_other_data=True,
        )
        self._patch_nxtomo_flags(self._nx_with_virtual_dataset_with_link)

        # create dark
        self.start_dark = (
            numpy.random.random((self.dim * self.dim))
            .reshape(1, self.dim, self.dim)
            .astype("f")
        )
        self.start_dark_file = os.path.join(self.tmpdir, "dark.hdf5")
        self.start_dark_entry = "data"
        self.start_dark_url = self._save_raw(
            data=self.start_dark,
            entry=self.start_dark_entry,
            file_path=self.start_dark_file,
        )

        self.end_dark = (
            numpy.random.random((self.dim * self.dim * 2))
            .reshape(2, self.dim, self.dim)
            .astype("f")
        )
        self.end_dark_file = os.path.join(self.tmpdir, "dark.hdf5")
        self.end_dark_entry = "data2"
        self.end_dark_url = self._save_raw(
            data=self.end_dark, entry=self.end_dark_entry, file_path=self.end_dark_file
        )

        # create flats
        self.start_flat = (
            numpy.random.random((self.dim * self.dim * 3))
            .reshape(3, self.dim, self.dim)
            .astype("f")
        )
        self.start_flat_file = os.path.join(self.tmpdir, "start_flat.hdf5")
        self.start_flat_entry = "/root/flat"
        self.start_flat_url = self._save_raw(
            data=self.start_flat,
            entry=self.start_flat_entry,
            file_path=self.start_flat_file,
        )

        self.end_flat = (
            numpy.random.random((self.dim * self.dim))
            .reshape(1, self.dim, self.dim)
            .astype("f")
        )
        # save the end flat in the simple case file to insure all cases are
        # consider
        self.end_flat_file = self._simple_nx.master_file
        self.end_flat_entry = "flat"
        self.end_flat_url = self._save_raw(
            data=self.end_flat, entry=self.end_flat_entry, file_path=self.end_flat_file
        )

    def _save_raw(self, data, entry, file_path) -> DataUrl:
        with h5py.File(file_path, mode="a") as h5s:
            h5s[entry] = data
        return DataUrl(file_path=file_path, data_path=entry, scheme="silx")

    def _create_vds(
        self,
        source_file: str,
        source_data_path: str,
        target_file: str,
        target_data_path: str,
        copy_other_data: bool,
    ):
        """Create virtual dataset and links from source to target

        :param source_file:
        :param source_data_path:
        :param target_file:
        :param target_data_path:
        :param copy_other_data: we want to create two cases: one copying
                                     datasets 'image_key'... and the other
                                     one linking them. Might have a difference
                                     of behavior when overwriting for example
        """
        assert source_file != target_file, "file should be different"
        # link data
        n_frames = 0
        # for now we only consider the original data
        with h5py.File(source_file, mode="r") as o_h5s:
            old_path = os.path.join(source_data_path, "instrument", "detector", "data")
            n_frames += o_h5s[old_path].shape[0]
            shape = o_h5s[old_path].shape
            data_type = o_h5s[old_path].dtype

            layout = h5py.VirtualLayout(shape=shape, dtype=data_type)
            assert os.path.exists(source_file)
            with h5py.File(source_file, mode="r") as ppp:
                assert source_data_path in ppp
            layout[:] = h5py.VirtualSource(path_or_dataset=o_h5s[old_path])

            det_path = os.path.join(target_data_path, "instrument", "detector")
            with h5py.File(target_file, mode="a") as h5s:
                detector_node = h5s.require_group(det_path)
                detector_node.create_virtual_dataset("data", layout, fillvalue=-5)

        for path in (
            os.path.join("instrument", "detector", "image_key"),
            os.path.join("instrument", "detector", "image_key_control"),
            os.path.join("instrument", "detector", "count_time"),
            os.path.join("sample", "rotation_angle"),
        ):
            old_path = os.path.join(source_data_path, path)
            new_path = os.path.join(target_data_path, path)
            with h5py.File(target_file, mode="a") as h5s:
                if copy_other_data:
                    with h5py.File(source_file, mode="r") as o_h5s:
                        if new_path in h5s:
                            del h5s[new_path]
                        h5s[new_path] = h5py_read_dataset(o_h5s[old_path])
                elif source_file == target_file:
                    h5s[new_path] = h5py.SoftLink(old_path)
                else:
                    relpath = os.path.relpath(source_file, os.path.dirname(target_file))
                    h5s[new_path] = h5py.ExternalLink(relpath, old_path)

    def _patch_nxtomo_flags(self, scan):
        """Insure necessary flags are here"""
        with h5py.File(scan.master_file, mode="a") as h5s:
            instrument_path = os.path.join(scan.entry, "instrument")
            instrument_node = h5s.require_group(instrument_path)
            if "NX_class" not in instrument_node.attrs:
                instrument_node.attrs["NX_class"] = "NXinstrument"
            detector_node = instrument_node.require_group("detector")
            if "NX_class" not in detector_node.attrs:
                detector_node.attrs["NX_class"] = "NXdetector"
            if "data" in instrument_node:
                if "interpretation" not in instrument_node.attrs:
                    instrument_node["data"].attrs["interpretation"] = "image"

            sample_path = os.path.join(scan.entry, "sample")
            sample_node = h5s.require_group(sample_path)
            if "NX_class" not in sample_node:
                sample_node.attrs["NX_class"] = "NXsample"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir)


class TestDaarkFlatPatch(BaseTestAddDarkAndFlats):
    def test(self):
        scan = NXtomoScan(
            self._nx_with_virtual_dataset_with_link.master_file,
            self._nx_with_virtual_dataset_with_link.entry,
        )
        process = DarkFlatPatchTask(
            inputs={
                "data": scan,
                "serialize_output_data": False,
                "configuration": {
                    "darks_start": self.start_dark_url,
                },
            },
        )
        process.definition()
        process.program_version()
        process.program_name()
        # TODO: properties should be part of inputs
        process.run()

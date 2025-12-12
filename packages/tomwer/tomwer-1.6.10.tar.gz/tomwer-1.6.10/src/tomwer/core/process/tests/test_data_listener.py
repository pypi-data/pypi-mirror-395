# coding: utf-8
from __future__ import annotations


import os
import shutil
import tempfile
import unittest

import h5py

from tomwer.core.process.control.datalistener.rpcserver import _BaseDataListenerThread


class JSONRPCClient:
    """Simulate call from bliss"""

    def scan_started(self, scan_number):
        return {
            "method": "scan_started",
            "params": [scan_number],
            "jsonrpc": "2.0",
            "id": 0,
        }

    def scan_ended(self, scan_number):
        return {
            "method": "scan_ended",
            "params": [scan_number],
            "jsonrpc": "2.0",
            "id": 1,
        }

    def sequence_started(
        self, saving_file, scan_title, sequence_scan_number, proposal_file, sample_file
    ):
        params = [
            saving_file,
            scan_title,
            sequence_scan_number,
            proposal_file,
            sample_file,
        ]
        return {
            "method": "sequence_started",
            "params": params,
            "jsonrpc": "2.0",
            "id": 2,
        }

    def sequence_ended(self, saving_file, sequence_scan_number, success):
        return {
            "method": "sequence_ended",
            "params": [saving_file, sequence_scan_number, success],
            "jsonrpc": "2.0",
            "id": 3,
        }


class TestJsonRPCServer(unittest.TestCase):
    """test the json rpc server"""

    def setUp(self):
        self.input_dir = tempfile.mkdtemp()
        sample_dir = os.path.join(self.input_dir, "sample")
        os.makedirs(sample_dir)
        self._proposal_file = os.path.join(sample_dir, "ihpayno_sample.h5")
        with h5py.File(self._proposal_file, mode="w") as h5f:
            h5f["test"] = "toto"

        os.makedirs(os.path.join(sample_dir, "sample_29042021"))
        self._sample_file = os.path.join(
            sample_dir, "sample_29042021", "sample_29042021.h5"
        )
        self._sample_file_entry = "1.1"

        with h5py.File(self._sample_file, mode="w") as h5f:
            h5f[self._sample_file_entry] = "tata"

        self.data_listener = _BaseDataListenerThread(host="localhost", port=4000)

    def tearDown(self):
        shutil.rmtree(self.input_dir)
        self.data_listener.stop()

    def testStartStop(self):
        self.data_listener.start()
        self.data_listener.stop()

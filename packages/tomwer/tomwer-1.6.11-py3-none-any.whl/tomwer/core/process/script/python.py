# coding: utf-8
from __future__ import annotations


import code
import logging

import tomwer.version
from tomwer.core.process.task import Task
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.core.utils.volumeutils import volume_identifier_to_volume

_logger = logging.getLogger(__name__)


class PythonScript(
    Task,
    optional_input_names=("data", "volume", "serialize_output_data"),
    output_names=("data", "volume"),
):
    def run(self):
        # load data
        scan = data_identifier_to_scan(self.inputs.data)
        if isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        elif isinstance(scan, (TomwerScanBase, type(None))):
            scan = scan
        else:
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")
        # load volume
        volume = volume_identifier_to_volume(self.inputs.volume)

        cfg = self.get_configuration()
        interpreter = code.InteractiveConsole(locals={"in_data": scan})
        interpreter = code.InteractiveConsole(locals={"in_volume": volume})
        interpreter.runcode(cfg["scriptText"])
        out_data = data_identifier_to_scan(interpreter.locals.get("out_data"))
        out_volume = data_identifier_to_scan(interpreter.locals.get("out_volume"))

        if out_data is not None and self.get_input_value("serialize_output_data", True):
            self.outputs.data = out_data.to_dict()
        else:
            self.outputs.data = out_data
        self.outputs.volume = out_volume

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "Python script"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Execute some random python code"

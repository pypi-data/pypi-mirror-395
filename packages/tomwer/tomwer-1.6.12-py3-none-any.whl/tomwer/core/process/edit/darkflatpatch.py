# coding: utf-8
from __future__ import annotations


import nxtomomill.version
from nxtomomill.utils import add_dark_flat_nx_file
from silx.io.url import DataUrl
from tomwer.core.utils.deprecation import deprecated_warning, deprecated

from tomwer.core.process.task import Task
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import data_identifier_to_scan


def apply_dark_flat_patch(scan: NXtomoScan, config: dict) -> TomwerScanBase:
    """

    :param scan:
    :param config:
    :return:
    """
    if not isinstance(scan, NXtomoScan):
        raise ValueError(
            f"Dark and flat patch only manage NXtomoScan and not {type(scan)}"
        )
    if config is None:
        return scan
    for param in ("darks_start", "darks_end", "flats_start", "flats_end"):
        if param not in config:
            config[param] = None

    add_dark_flat_nx_file(
        file_path=scan.master_file,
        entry=scan.entry,
        **config,
    )
    return scan


class DarkFlatPatchTask(
    Task,
    input_names=("data", "configuration"),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    Patch an existing NXtomo calling nxtomomill
    """

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            return
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be a dict or an instance of TomwerScanBase. Not {type(scan)}"
            )
        if not isinstance(scan, NXtomoScan):
            raise ValueError(f"input type of {scan}: {type(scan)} is not managed")

        config = self.inputs.configuration
        if not isinstance(config, dict):
            raise TypeError(f"config is expected to be a dict. {type(config)} provided")
        apply_dark_flat_patch(scan=scan, config=config)
        keys = config.keys()
        for key in keys:
            value = config[key]
            if isinstance(value, DataUrl):
                config[key] = value.path()

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    @staticmethod
    def program_name():
        return "nxtomomill.utils.change_image_key_control"

    @staticmethod
    def program_version():
        return nxtomomill.version.version

    @staticmethod
    def definition():
        return "Apply patch for dark and references on a scan (TomwerScanBase)"

    @deprecated(
        since_version="1.2",
        replacement="DarkFlatPatchTask.inputs.configuration",
        reason="ewoksification",
    )
    def get_configuration(self):
        """

        :return: configuration of the process
        """
        return self.inputs.configuration

    @deprecated(
        since_version="1.2",
        replacement="DarkFlatPatchTask.inputs.configuration",
        reason="ewoksification",
    )
    def set_configuration(self, configuration: dict) -> None:
        self.inputs.configuration = configuration


class DarkFlatPatch(DarkFlatPatchTask):
    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.edit.darkflatpatch.DarkFlatPatch",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="DarkFlatPatchTask",
        )
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)

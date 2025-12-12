# coding: utf-8
from __future__ import annotations

import copy
import logging

import nxtomomill.version
from nxtomomill.utils import change_image_key_control as _change_image_key_control
from nxtomo.nxobject.nxdetector import ImageKey
from tomwer.core.utils.deprecation import deprecated_warning, deprecated

from tomwer.core.process.task import Task
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.utils.scanutils import data_identifier_to_scan

_logger = logging.getLogger(__name__)


IMAGE_KEYS = {
    "projection": ImageKey.PROJECTION,
    "invalid": ImageKey.INVALID,
    "dark": ImageKey.DARK_FIELD,
    "flat": ImageKey.FLAT_FIELD,
}


def change_image_key_control(scan: NXtomoScan, config: dict) -> TomwerScanBase:
    """

    :param scan:
    :param config:
    :raises KeyError: if 'frames_indexes' or 'image_key_control_value' are
                      not in config
    :return:
    """
    if scan is None:
        return
    elif not isinstance(scan, NXtomoScan):
        raise ValueError(
            f"Image key control only handle NXtomoScan and not {type(scan)}"
        )

    if "modifications" not in config:
        raise KeyError("modifications are not provided")
    else:
        modifications = config["modifications"]
        if modifications is None:
            modifications = {}

    image_keys_set = set(modifications.values())
    image_keys_set = set([ImageKey(image_key) for image_key in image_keys_set])
    for image_key_type in image_keys_set:
        frame_indexes_dict = dict(
            filter(lambda item: item[1] is image_key_type, modifications.items())
        )
        frame_indexes = tuple(frame_indexes_dict.keys())
        _logger.info(f"will modify {frame_indexes} to {image_key_type}")
        _change_image_key_control(
            file_path=scan.master_file,
            entry=scan.entry,
            frames_indexes=frame_indexes,
            image_key_control_value=image_key_type.value,
            logger=_logger,
        )
    scan.clear_frames_cache()
    return scan


class ImageKeyEditorTask(
    Task,
    input_names=("data", "configuration"),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    task to edit `image_key` field of a NXtomo ('data' input)
    """

    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        super().__init__(
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            return
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be a dict or an instance of TomwerScanBase. Not {type(scan)}"
            )
        if not isinstance(scan, NXtomoScan):
            raise ValueError(f"input type of {scan}: {(type(scan))} is not managed")

        config = self.inputs.configuration
        if not isinstance(config, dict):
            raise TypeError
        # apply configuration
        change_image_key_control(scan=scan, config=config)
        modif_keys = list(config.get("modifications", {}).keys())
        # dump modifications to the tomwer processes file
        # note: we need to cast image keys to str to save it
        config = copy.deepcopy(config)
        new_modif = {}
        for key in modif_keys:
            value = config["modifications"][key]
            config["modifications"][str(key)] = value
        config["modifications"] = new_modif

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
        return "Modify image keys on a NXtomo"


class ImageKeyUpgraderTask(
    Task,
    input_names=("data", "operations"),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    close to ImageKeyEditor but convert a full "family" of frame type to another
    like all projections to dark field
    """

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if not isinstance(scan, NXtomoScan):
            raise TypeError(f"scan is expected to be an instance of {NXtomoScan}")
        operations = self.inputs.operations
        if not isinstance(operations, dict):
            raise TypeError("operations is expected to be an dict")

        configuration = {}
        for key_image_value_from, key_image_value_to in operations.items():
            configuration.update(
                self.from_operation_to_config(
                    scan=scan,
                    from_image_key=key_image_value_from,
                    to_image_key=key_image_value_to,
                )
            )
        configuration = {
            "modifications": configuration,
        }

        # apply modification using tomoscan
        change_image_key_control(scan=scan, config=configuration)

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    @staticmethod
    def from_operation_to_config(
        scan: TomwerScanBase, from_image_key: ImageKey, to_image_key: ImageKey
    ):
        """
        retrieve frame indices to be updated
        """
        from_image_key = ImageKey(from_image_key)
        to_image_key = ImageKey(to_image_key)

        config = {}
        for i_frame, frame in enumerate(scan.frames):
            if frame.image_key == from_image_key:
                config[i_frame] = to_image_key

        return config

    @staticmethod
    def program_name():
        return "nxtomomill.utils.ImageKeyUpgraderTask"

    @staticmethod
    def program_version():
        return nxtomomill.version.version

    @staticmethod
    def definition():
        return "Modify image keys on a NXtomo"

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


class ImageKeyUpgrader(ImageKeyUpgraderTask):
    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.edit.imagekeyeditor.ImageKeyUpgrader",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="ImageKeyUpgraderTask",
        )
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)

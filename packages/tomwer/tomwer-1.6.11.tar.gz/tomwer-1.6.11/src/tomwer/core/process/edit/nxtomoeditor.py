from __future__ import annotations

import gc
import logging
import h5py
import numpy

from collections import namedtuple
from typing import Any

from silx.io.utils import h5py_read_dataset

from tomoscan.io import HDF5File

from nxtomo.paths.nxtomo import get_paths as get_nexus_paths
from nxtomo.nxobject.nxtransformations import NXtransformations
from nxtomo.utils.transformation import (
    DetXFlipTransformation,
    DetYFlipTransformation,
)

from tomwer.core.process.task import Task
from tomwer.core.scan.nxtomoscan import NXtomoScan

_EditorFieldInfo = namedtuple(
    "_EditorFieldInfo", ["nexus_path", "name", "expected_type", "units", "n_value"]
)

_logger = logging.getLogger(__name__)


class NXtomoEditorKeys:
    """namespace to store all keys used by the nxtomo editor"""

    ENERGY = "instrument.beam.energy"
    DETECTOR_X_PIXEL_SIZE = "instrument.detector.x_pixel_size"
    DETECTOR_Y_PIXEL_SIZE = "instrument.detector.y_pixel_size"
    SAMPLE_DETECTOR_DISTANCE = "instrument.detector.distance"
    SAMPLE_SOURCE_DISTANCE = "instrument.source.distance"
    SAMPLE_X_PIXEL_SIZE = "sample.x_pixel_size"
    SAMPLE_Y_PIXEL_SIZE = "sample.y_pixel_size"
    PROPAGATION_DISTANCE = "sample.propagation_distance"
    FIELD_OF_VIEW = "instrument.detector.field_of_view"
    LR_FLIPPED = "instrument.detector.lr_flipped"
    UD_FLIPPED = "instrument.detector.ud_flipped"
    X_TRANSLATION = "sample.x_translation"
    Y_TRANSLATION = "sample.y_translation"
    Z_TRANSLATION = "sample.z_translation"


class NXtomoEditorTask(
    Task,
    input_names=("data", "configuration"),
    output_names=("data",),
):
    """
    task to edit a couple of field of a NXtomo
    """

    def run(self):
        scan = self.inputs.data
        if scan is None:
            _logger.warning("no scan found to be saved")
            return
        if not isinstance(scan, NXtomoScan):
            raise TypeError(
                f"data is expected to be an instance of {NXtomoScan}. Got {type(scan)}"
            )

        configuration = self.inputs.configuration
        if not isinstance(configuration, dict):
            raise TypeError(
                f"configuration is expected to be an instance of {dict}. Got {type(configuration)}"
            )

        n_frames = len(scan.image_key_control)
        mapping = self.build_mapping(
            nexus_version=scan.nexus_version, n_frames=n_frames
        )

        lr_flip = configuration.pop(NXtomoEditorKeys.LR_FLIPPED, None)
        ud_flip = configuration.pop(NXtomoEditorKeys.UD_FLIPPED, None)

        with HDF5File(scan.master_file, mode="a") as h5f:
            entry = h5f[scan.entry]

            for field, field_value in configuration.items():
                if field not in mapping:
                    raise ValueError(f"field unknown ({field})")
                self.__write_to_file(
                    entry=entry,
                    path=mapping[field].nexus_path,
                    value=field_value,
                    name=mapping[field].name,
                    expected_type=mapping[field].expected_type,
                    units=mapping[field].units,
                    n_value=mapping[field].n_value,
                )

            # solve NXtransformations
            if lr_flip is not None or ud_flip is not None:
                nx_transformations, detector_transformation_path = (
                    self.get_detector_transformations(
                        scan_entry=scan.entry,
                        lr_flip=(
                            lr_flip if lr_flip is not None else scan.detector_is_lr_flip
                        ),
                        ud_flip=(
                            ud_flip if ud_flip is not None else scan.detector_is_ud_flip
                        ),
                        nexus_version=scan.nexus_version,
                    )
                )
            else:
                nx_transformations = detector_transformation_path = None

        # make sure the file has been removed (fix https://gitlab.esrf.fr/tomotools/tomwer/-/merge_requests/874#note_366688).
        gc.collect()
        if nx_transformations is not None:
            nx_transformations.save(
                file_path=scan.master_file,
                data_path=detector_transformation_path,
                nexus_path_version=scan.nexus_version,
                overwrite=True,
            )
        # clear caches to make sure all modifications will be considered
        scan.clear_cache()
        scan.clear_frames_cache()
        self.outputs.data = scan

    @staticmethod
    def get_detector_transformations(
        scan_entry: str, lr_flip: bool, ud_flip: bool, nexus_version: float | None
    ) -> dict:
        nexus_paths = get_nexus_paths(nexus_version)
        if nexus_paths.nx_detector_paths.NX_TRANSFORMATIONS is None:
            # old NXtomo are not handling NX_TRANSFORMATIONS
            _logger.debug(
                "Old version of NXtomo found. No information about transformation will be saved"
            )
            return None, None

        nx_transformations = NXtransformations()
        nx_transformations.add_transformation(DetXFlipTransformation(flip=ud_flip))
        nx_transformations.add_transformation(DetYFlipTransformation(flip=lr_flip))

        detector_transformation_path = "/".join(
            (
                scan_entry,
                nexus_paths.INSTRUMENT_PATH,
                nexus_paths.nx_instrument_paths.DETECTOR_PATH,
                nexus_paths.nx_detector_paths.NX_TRANSFORMATIONS,
            ),
        )
        return nx_transformations, detector_transformation_path

    @staticmethod
    def __write_to_file(
        entry: h5py.Group,
        path: str,
        value: Any,
        name: str,
        expected_type: type,
        n_value: int = 1,
        units=None,
    ) -> None:
        if path is None:
            # if the path does not exists (no handled by this version of nexus for example)
            return

        # try to cast the value
        if isinstance(value, str):
            value = value.replace(" ", "")
            if value.lower() == "none" or "..." in value:
                # if value is not defined or is an array not overwrite by the user (case of the ... )
                return
        elif value is None:
            pass
        else:
            try:
                value = expected_type(value)
            except (ValueError, TypeError) as e:
                _logger.error(f"Fail to overwrite {name} of {entry.name}. Error is {e}")
                return

        if path in entry:
            if not NXtomoEditorTask.isFieldValueDifferent(
                dataset=entry[path], new_value=value, units=units
            ):
                # if no need to overwrite
                return
            else:
                del entry[path]
        if value is None:
            return
        elif n_value == 1:
            entry[path] = value
        else:
            entry[path] = numpy.array([value] * n_value)
        if units is not None:
            entry[path].attrs["units"] = units

    @staticmethod
    def isFieldValueDifferent(dataset: h5py.Dataset, new_value, units) -> bool:
        """
        return False if the given value is the same as the one stored.

        This is a small improvement to avoid rewrite field if we can avoid it.
        The reason behind is that the orange widget will update the field when it receive a scan (of the unlock field).
        But then users can edit any field. As we don't want to bother with complex stuff like for each field keep track if
        It has been modified or not the orange widget will always require to modify all possible field even is not modified.
        """
        current_value = h5py_read_dataset(dataset)
        attrs = dataset.attrs
        current_unit = attrs.get("units", attrs.get("unit", None))
        if units != current_unit:
            # if the unit is not the same, even if the value is the same we will overwrite it
            return True
        else:
            if isinstance(new_value, numpy.ndarray) and isinstance(
                current_value, numpy.ndarray
            ):
                return not numpy.array_equal(new_value, current_value)
            elif numpy.isscalar(current_value) and numpy.isscalar(new_value):
                return current_value != new_value
            else:
                return True

    @staticmethod
    def build_mapping(
        nexus_version: float | None, n_frames: int
    ) -> dict[NXtomoEditorKeys, _EditorFieldInfo]:
        """
        for the different field that can be edited we provide an instance of _EditorFieldInfo
        with all metadata needed to save this particular field.

        Note: X_flip and y_flip are saved differently as the two parameters are coupled we want either to save both or none of it.
        """
        nexus_paths = get_nexus_paths(nexus_version)

        mapping = {
            # energy
            NXtomoEditorKeys.ENERGY: _EditorFieldInfo(
                nexus_path=nexus_paths.ENERGY_PATH,
                expected_type=float,
                units="kev",
                name="energy",
                n_value=1,
            ),
            # sample / detector distance
            NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE: _EditorFieldInfo(
                nexus_path=nexus_paths.SAMPLE_DETECTOR_DISTANCE_PATH,
                expected_type=float,
                units="m",
                name="sample detector distance",
                n_value=1,
            ),
            # sample / source distance
            NXtomoEditorKeys.SAMPLE_SOURCE_DISTANCE: _EditorFieldInfo(
                nexus_path=nexus_paths.SAMPLE_SOURCE_DISTANCE_PATH,
                expected_type=float,
                units="m",
                name="sample detector distance",
                n_value=1,
            ),
            # overwrite FOV
            NXtomoEditorKeys.FIELD_OF_VIEW: _EditorFieldInfo(
                nexus_path=nexus_paths.FOV_PATH,
                expected_type=str,
                units=None,
                name="field of view",
                n_value=1,
            ),
            # x translation
            NXtomoEditorKeys.X_TRANSLATION: _EditorFieldInfo(
                nexus_path=nexus_paths.X_TRANS_PATH,
                expected_type=float,
                units="m",
                name="x translation",
                n_value=n_frames,
            ),
            # y translation
            NXtomoEditorKeys.Y_TRANSLATION: _EditorFieldInfo(
                nexus_path=nexus_paths.Y_TRANS_PATH,
                expected_type=float,
                units="m",
                name="y translation",
                n_value=n_frames,
            ),
            # z translation
            NXtomoEditorKeys.Z_TRANSLATION: _EditorFieldInfo(
                nexus_path=nexus_paths.Z_TRANS_PATH,
                expected_type=float,
                units="m",
                name="z translation",
                n_value=n_frames,
            ),
            # detector x pixel size
            NXtomoEditorKeys.DETECTOR_X_PIXEL_SIZE: _EditorFieldInfo(
                nexus_path=nexus_paths.DETECTOR_X_PIXEL_SIZE_PATH,
                expected_type=float,
                units="m",
                name="detector x pixel size",
                n_value=1,
            ),
            # detector y pixel size
            NXtomoEditorKeys.DETECTOR_Y_PIXEL_SIZE: _EditorFieldInfo(
                nexus_path=nexus_paths.DETECTOR_Y_PIXEL_SIZE_PATH,
                expected_type=float,
                units="m",
                name="detector y pixel size",
                n_value=1,
            ),
            # sample x pixel size
            NXtomoEditorKeys.SAMPLE_X_PIXEL_SIZE: _EditorFieldInfo(
                nexus_path=nexus_paths.SAMPLE_X_PIXEL_SIZE_PATH,
                expected_type=float,
                units="m",
                name="sample x pixel size",
                n_value=1,
            ),
            # sample y pixel size
            NXtomoEditorKeys.SAMPLE_Y_PIXEL_SIZE: _EditorFieldInfo(
                nexus_path=nexus_paths.SAMPLE_Y_PIXEL_SIZE_PATH,
                expected_type=float,
                units="m",
                name="sample y pixel size",
                n_value=1,
            ),
            # propagation distance
            NXtomoEditorKeys.PROPAGATION_DISTANCE: _EditorFieldInfo(
                nexus_path=nexus_paths.PROPAGATION_DISTANCE,
                expected_type=float,
                units="m",
                name="propagation distance",
                n_value=1,
            ),
        }

        return mapping

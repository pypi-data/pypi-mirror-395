# coding: utf-8
from __future__ import annotations

import datetime
import logging
import os
from contextlib import AbstractContextManager

from nabu.pipeline.config import generate_nabu_configfile, parse_nabu_config_file
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from enum import Enum

from tomoscan.identifier import VolumeIdentifier
from tomoscan.volumebase import VolumeBase
import tomwer.version
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.process.output import NabuOutputFileFormat
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.jp2kvolume import JP2KVolume
from tomwer.core.volume.rawvolume import RawVolume
from tomwer.core.volume.tiffvolume import TIFFVolume, MultiTIFFVolume

_logger = logging.getLogger(__name__)


class TomwerInfo(AbstractContextManager):
    """Simple context manager to add tomwer metadata to a dict before
    writing it"""

    def __init__(self, config_dict):
        self.config = config_dict

    def __enter__(self):
        self.config["other"] = {
            "tomwer_version": tomwer.version.version,
            "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.config["other"]["tomwer_version"]
        del self.config["other"]["date"]


def retrieve_lst_of_value_from_str(my_string: str, type_) -> tuple:
    """
    Return a list of value from a string like '12,23' or '(12, 23)',
    '[12;23]', '12;23' or with the pattern from:to:step like '0:10:1'

    :param mystring:
    :return: list of single value
    """
    if not isinstance(my_string, str):
        raise TypeError(
            f"my_string is expected to be a string. {type(my_string)} provided"
        )
    res = []
    my_string = my_string.replace("(", "")
    my_string = my_string.replace(")", "")
    my_string = my_string.replace("[", "")
    my_string = my_string.replace("]", "")
    if my_string.count(":") == 2:
        _from, _to, _step = my_string.split(":")
        _from, _to, _step = float(_from), float(_to), float(_step)
        if _from > _to:
            tmp = _to
            _to = _from
            _from = tmp
        while _from <= _to:
            res.append(_from)
            _from += _step
        return tuple(res)
    else:
        vals = my_string.replace(" ", "")
        vals = vals.replace("_", "")
        vals = vals.replace(";", ",").split(",")
        for val in vals:
            try:
                res.append(type_(val))
            except Exception:
                pass
        return tuple(res)


def get_nabu_about_desc(overwrite: bool) -> dict:
    """
    Create the description for nabu's 'about'

    """
    return {"overwrite_results": str(bool(overwrite))}


def get_recons_volume_identifier(
    file_prefix: str,
    location: str,
    file_format: str | NabuOutputFileFormat,
    scan: TomwerScanBase,
    slice_index: int | None,
    axis: NabuPlane,
) -> tuple[VolumeIdentifier]:
    """
    return tuple of DataUrl for existings slices
    """
    axis = NabuPlane.from_value(axis)
    if isinstance(file_format, NabuOutputFileFormat):
        file_format = file_format.value
    file_format = file_format.lower()
    if file_format in ("hdf5", "h5", "hdf"):
        if slice_index is not None:
            # case of a single hdf5 file
            file_name = "_".join(
                (file_prefix, "plane", axis.value, str(slice_index).zfill(6))
            )
        else:
            file_name = file_prefix
        file_name = ".".join((file_name, file_format))
        file_path = os.path.join(location, file_name)

        if isinstance(scan, NXtomoScan):
            entry = scan.entry
        elif isinstance(scan, EDFTomoScan):
            entry = "entry"
        else:
            raise NotImplementedError(f"unrecognized scan type ({type(scan)})")

        volumes = (
            HDF5Volume(
                file_path=file_path,
                data_path="/".join([entry, "reconstruction"]),
            ),
        )
    elif file_format in ("vol", "raw"):
        if slice_index is not None:
            # case of a single hdf5 file
            file_name = "_".join(
                (file_prefix, "plane", axis.value, str(slice_index).zfill(6))
            )
        else:
            file_name = file_prefix
        file_name = ".".join((file_name, file_format))
        file_path = os.path.join(location, file_name)

        volumes = (RawVolume(file_path=file_path),)
    elif file_format in ("jp2", "jp2k", "edf", "tiff"):
        if file_format in ("jp2k", "jp2"):
            constructor = JP2KVolume
        elif file_format == "edf":
            constructor = EDFVolume
        elif file_format == "tiff":
            constructor = TIFFVolume
        else:
            raise NotImplementedError
        basename = file_prefix
        file_path = location
        volumes = (
            constructor(
                folder=location,
                volume_basename=basename,
            ),
        )
    elif file_format == "tiff3d":
        if slice_index is not None:
            # case of a single hdf5 file
            file_name = "_".join(
                (file_prefix, "plane", axis.value, str(slice_index).zfill(6))
            )
        else:
            file_name = file_prefix
        file_name = ".".join((file_name, "tiff"))
        file_path = os.path.join(location, file_name)

        volumes = (
            MultiTIFFVolume(
                file_path=file_path,
            ),
        )

    else:
        raise ValueError(f"file format not managed: {file_format}")

    return tuple([volume.get_identifier() for volume in volumes])


def get_multi_cor_recons_volume_identifiers(
    scan: TomwerScanBase,
    slice_index: int,
    location: str,
    file_prefix: str,
    cors: tuple,
    file_format: str,
    axis=NabuPlane.XY,
) -> dict:
    """
    util to retrieve Volumes (identifier) reconstructed by nabu-multicor

    :param scan: scam processed by the nabu-multicor
    :param location: location of the files
    :param cors: cors for which we want the reconstructed slices. As this extension is created by nabu
                       the cor reference is in absolute.
    :param file_format: file format of the reconstruction

    :return: a dict with absolute cor value as key and the Volume identifier as value
    """
    _logger.info("Deduce volume identifiers for nabu-multicor")
    if isinstance(slice_index, str):
        slice_index = slice_index_to_int(
            slice_index=slice_index,
            scan=scan,
            axis=axis,  # for now we always expect the multicor to be done along Z
        )
    assert isinstance(
        slice_index, int
    ), "slice_index is expected to be an int or to be converted to it"
    res = {}
    if isinstance(scan, EDFTomoScan):
        entry = "entry"
    else:
        entry = scan.entry

    for cor in cors:
        file_path = os.path.join(
            location,
            f"{file_prefix}_{cor:.3f}_{str(slice_index).zfill(5)}.{file_format}",
        )

        if file_format in ("hdf5", "h5", "hdf"):
            file_path = os.path.join(
                location,
                f"{file_prefix}_{cor:.3f}_{str(slice_index).zfill(5)}.{file_format}",
            )
            volume = HDF5Volume(
                file_path=file_path,
                data_path="/".join([entry, "reconstruction"]),
            )
        elif file_format in ("vol", "raw"):
            volume = (RawVolume(file_path=file_path),)
        elif file_format in ("jp2", "jp2k", "edf", "tiff"):
            if file_format in ("jp2k", "jp2"):
                constructor = JP2KVolume
            elif file_format == "edf":
                constructor = EDFVolume
            elif file_format == "tiff":
                constructor = TIFFVolume
            else:
                raise NotImplementedError
            file_path = location
            volume = constructor(
                folder=os.path.dirname(file_path),
                volume_basename=os.path.basename(file_path),
            )
        else:
            raise ValueError(f"file_format {file_format} is not handled for now")
        res[cor] = volume.get_identifier()
    return res


class _NabuMode(Enum):
    FULL_FIELD = "standard acquisition"
    HALF_ACQ = "half acquisition"
    # HELICAL = "helical acquisition"


class _NabuStages(Enum):
    INI = "initialization"
    PRE = "pre-processing"
    PHASE = "phase"
    PROC = "processing"
    POST = "post-processing"
    VOLUME = "volume"

    @staticmethod
    def getStagesOrder():
        return (
            _NabuStages.INI,
            _NabuStages.PRE,
            _NabuStages.PHASE,
            _NabuStages.PROC,
            _NabuStages.POST,
        )

    @staticmethod
    def getProcessEnum(stage):
        """Return the process Enum associated to the stage"""
        stage = _NabuStages(stage)
        if stage is _NabuStages.INI:
            raise NotImplementedError()
        elif stage is _NabuStages.PRE:
            return _NabuPreprocessing
        elif stage is _NabuStages.PHASE:
            return _NabuPhase
        elif stage is _NabuStages.PROC:
            return _NabuProcessing
        elif stage is _NabuStages.POST:
            return _NabuPostProcessing
        raise NotImplementedError()


class _NabuPreprocessing(Enum):
    """Define all the preprocessing action possible and the order they
    are applied on"""

    FLAT_FIELD_NORMALIZATION = "flat field normalization"
    CCD_FILTER = "hot spot correction"

    @staticmethod
    def getPreProcessOrder():
        return (
            _NabuPreprocessing.FLAT_FIELD_NORMALIZATION,
            _NabuPreprocessing.CCD_FILTER,
        )


class _NabuPhase(Enum):
    """Define all the phase action possible and the order they
    are applied on"""

    PHASE = "phase retrieval"
    UNSHARP_MASK = "unsharp mask"
    LOGARITHM = "logarithm"

    @staticmethod
    def getPreProcessOrder():
        return (_NabuPhase.PHASE, _NabuPhase.UNSHARP_MASK, _NabuPhase.LOGARITHM)


class _NabuProcessing(Enum):
    """Define all the processing action possible"""

    RECONSTRUCTION = "reconstruction"

    @staticmethod
    def getProcessOrder():
        return (_NabuProcessing.RECONSTRUCTION,)


class _NabuPostProcessing(Enum):
    """Define all the post processing action available"""

    SAVE_DATA = "save"

    @staticmethod
    def getProcessOrder():
        return (_NabuPostProcessing.SAVE_DATA,)


class _NabuReconstructionMethods(Enum):
    CONE = "cone"
    FBP = "FBP"
    HBP = "HBP"
    MLEM = "MLEM"


class _NabuPhaseMethod(Enum):
    """
    Nabu phase method
    """

    PAGANIN = "Paganin"
    CTF = "CTF"
    NONE = "None"

    @classmethod
    def from_value(cls, value):
        if value in (None, ""):
            return _NabuPhaseMethod.NONE
        elif isinstance(value, str):
            if value.lower() == "paganin":
                return _NabuPhaseMethod.PAGANIN
            elif value.lower() == "none":
                return _NabuPhaseMethod.NONE
            elif value.lower() == "ctf":
                return _NabuPhaseMethod.CTF
        else:
            return _NabuPhaseMethod(value=value)


class _NabuFBPFilterType(Enum):
    RAMLAK = "ramlak"
    SHEPP_LOGAN = "shepp-logan"
    COSINE = "cosine"
    HAMMING = "hamming"
    HANN = "hann"
    TUKEY = "tukey"
    LANCZOS = "lanczos"
    HILBERT = "hilbert"


class _NabuPaddingType(Enum):
    ZEROS = "zeros"
    EDGES = "edges"


class RingCorrectionMethod(Enum):
    NONE = "None"
    MUNCH = "munch"
    VO = "vo"
    MEAN_SUBTRACTION = "mean-subtraction"
    MEAN_DIVISION = "mean-division"


def nabu_std_err_has_error(errs: bytes | None):
    """
    small util to parse stderr where some warning can exists.
    But I don't think we want to catch all warnings from nabu so this is a (bad) concession
    This will disapear when execution will be done directly from a tomwer thread instead of a subprocess
    """

    def ignore(line) -> bool:
        return (
            "warning" in line
            or "Warning" in line
            or "cupyx.jit.rawkernel" in line
            or "deprecated" in line
            or line.replace(" ", "") == ""
            or "unable to load" in line
            or "deprecated" in line
            or "self.module = SourceModule(self.src, **self.sourcemodule_kwargs)"
            in line
            or "return SourceModule(" in line
            or "CUBLAS" in line
            or "Not supported for EDF"
            in line  # debatable but very disturbing from the gui side... anyway EDF days are coming to an end
            or "PerformanceWarning" in line
            or "jitify._init_module()" in line
            or " unable to import 'siphash24.siphash13" in line
            or "_create_built_program_from_source_cached" in line
            or "prg.build(options_bytes," in line
            or (
                "Performing MLEM" in line and "iterations" in line
            )  # corrct usage of tqdm (goes to stderr)
            or "Remark: The" in line
            or "int x_stop_other = other_x_range.y;" in line
            or "int y_stop_other = other_y_range.y;" in line
        )

    if errs is None:
        return False
    else:
        for line in errs.decode("UTF-8").split("\n"):
            if not ignore(line):
                print("\n\nline is", line)
                return True
    return False


def update_cfg_file_after_transfer(config_file_path, old_path, new_path):
    """
    update nabu configuration file path from /lbsram/data to /data
    """
    if old_path is None or new_path is None:
        return

    # load configucation file
    config_as_dict = parse_nabu_config_file(config_file_path)
    assert isinstance(config_as_dict, dict)

    # update paths
    paths_to_update = (
        ("dataset", "location"),
        ("output", "location"),
        ("pipeline", "steps_file"),
    )
    for section, field in paths_to_update:
        # update dataset location and output location
        if section in config_as_dict:
            location = config_as_dict[section].get(field, None)
            if location is not None:
                config_as_dict[section][field] = location.replace(old_path, new_path, 1)
    # overwrite file
    generate_nabu_configfile(
        fname=config_file_path,
        default_config=nabu_fullfield_default_config,
        config=config_as_dict,
        options_level="advanced",
    )


def slice_index_to_int(
    slice_index: int | str,
    scan: TomwerScanBase,
    axis=NabuPlane.XY,
) -> int:
    """
    cast a slice to an index. The slice can be a string in ['first', 'last', 'middle']
    """
    axis = NabuPlane.from_value(axis)
    if slice_index == "fisrt":
        return 0
    elif slice_index == "last":
        if scan is None:
            # backward compatibility in the case the scan is not provided. Should not happen anymore
            _logger.warning("Scan not provided. Consider the 2048 width detector")
            return 2047
        elif scan.dim_2 is not None:
            return scan.dim_2 - 1
        else:
            # this could happen on some EDF scans. Not expected to happen for HDF5
            _logger.warning("unable to get dim size, guess this is 2048 width")
            # in this
            return 2047
    elif slice_index == "middle":
        if scan is None:
            # backward compatibility in the case the scan is not provided. Should not happen anymore
            _logger.warning("Scan not provided. Consider the 1024 width detector")
            # default middle.
            return 1024
        elif axis is NabuPlane.XY:
            if scan.dim_2 is None:
                _logger.warning("unable to get dim size, guess this is 2048 height")
                return 1024
            else:
                return scan.dim_2 // 2
        elif axis in (NabuPlane.YZ, NabuPlane.XZ):
            if scan.dim_1 is None:
                _logger.warning("unable to get dim size, guess this is 2048 width")
                return 1024
            else:
                return scan.dim_1 // 2
        else:
            raise ValueError(f"axis {axis} is not handled")
    else:
        return int(slice_index)


def get_nabu_multicor_file_prefix(scan):
    if isinstance(scan, EDFTomoScan):
        dataset_path = scan.path
    elif isinstance(scan, NXtomoScan):
        dataset_path = scan.master_file
    else:
        raise TypeError(f"{type(scan)} is not handled")

    if os.path.isfile(dataset_path):  # hdf5
        file_prefix = os.path.basename(dataset_path).split(".")[0]
    elif os.path.isdir(dataset_path):
        file_prefix = os.path.basename(dataset_path)
    else:
        raise ValueError(f"dataset location {scan.path} is neither a file or directory")
    file_prefix += "_rec"  # avoid overwriting dataset
    return file_prefix


def update_nabu_config_for_tiff_3d(config: dict) -> None:
    """
    Adapts the nabu configuration for 3D TIFF file format.

    Nabu currently distinguishes TIFF files as either single-file or multi-file,
    but does not natively support the concept of a 3D TIFF format. This function
    bridges that gap by adjusting the configuration to handle 3D TIFF files
    as a single logical unit.
    """
    file_format = NabuOutputFileFormat(
        config.get("output", {}).get("file_format", "tiff")
    )
    if file_format is NabuOutputFileFormat.TIFF_3D:
        config["output"]["file_format"] = "tiff"
        config["output"]["tiff_single_file"] = "1"
        _logger.debug("Mapping tiff3d -> nabu tiff + tiff_single_file=1")


def from_nabu_config_to_file_format(nabu_config) -> NabuOutputFileFormat:
    """
    Infers the file format from a Nabu configuration dictionary.

    This function is specifically designed to handle the special case of 3D TIFF files. See 'update_nabu_config_for_tiff_3d'
    """
    file_format = NabuOutputFileFormat(nabu_config["output"]["file_format"])
    tiff_single_file = nabu_config["output"].get("tiff_single_file", False)
    if tiff_single_file in (True, 1, "1") and file_format is NabuOutputFileFormat.TIFF:
        return NabuOutputFileFormat.TIFF_3D
    else:
        return file_format


def get_default_output_volume_for_tiff_3d(
    input_volume: TomwerVolumeBase, output_dir: str
) -> TomwerVolumeBase:
    """
    Does what nabu.io.cast_volume.get_default_output_volume does but for for 3d-tiff
    For a given input volume and output type return output volume as an instance of VolumeBase

    :param intput_volume: volume for which we want to get the resulting output volume for a cast
    :param output_dir: output dir to save the cast volume
    """
    if not isinstance(input_volume, VolumeBase):
        raise TypeError(f"input_volume is expected to be an instance of {VolumeBase}")

    if isinstance(input_volume, (EDFVolume, TIFFVolume, JP2KVolume)):
        file_path = os.path.join(
            input_volume.data_url.file_path(),
            output_dir,
            input_volume.get_volume_basename() + ".tiff",
        )
        volume = MultiTIFFVolume(
            file_path=file_path,
        )
        assert (
            volume.get_identifier() is not None
        ), "volume should be able to create an identifier"
        return volume

    elif isinstance(input_volume, (HDF5Volume, MultiTIFFVolume)):
        data_file_parent_path, data_file_name = os.path.split(
            input_volume.data_url.file_path()
        )
        # replace extension:
        data_file_name = ".".join(
            [
                os.path.splitext(data_file_name)[0],
                "tiff",
            ]
        )
        volume = MultiTIFFVolume(
            file_path=os.path.join(data_file_parent_path, output_dir, data_file_name),
        )
        assert (
            volume.get_identifier() is not None
        ), "volume should be able to create an identifier"
        return volume
    else:
        raise NotImplementedError(f"input volume format {input_volume} is not handled")

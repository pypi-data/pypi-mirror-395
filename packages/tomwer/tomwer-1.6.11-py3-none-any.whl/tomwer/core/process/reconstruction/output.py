from __future__ import annotations
import os
import logging
from tomwer.io.utils.raw_and_processed_data import (
    to_processed_data_path,
)
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.process.output import ProcessDataOutputDirMode
from tomwer.core.utils.scanutils import format_output_location
from tomwer.core.process.output import NabuOutputFileFormat

_logger = logging.getLogger(__name__)


PROCESS_FOLDER_RECONSTRUCTED_VOLUMES = "reconstructed_volumes"

PROCESS_FOLDER_RECONSTRUCTED_SLICES = "reconstructed_slices"

PROCESS_FOLDER_CAST_VOLUME = "cast_volume"


def get_output_folder_from_scan(
    mode: ProcessDataOutputDirMode,
    scan: TomwerScanBase,
    nabu_location: str | None,
    file_basename: str,
    file_format: NabuOutputFileFormat,
    processed_data_folder_name: str | None,
) -> tuple[str, str]:
    """

    :param mode: output mode, should save this to raw data, processed data...
    :param scan: scan for which we want to get the output folder
    :param nabu_location: output location provided by user (in case mode is 'other')
    :param file_basename: file basename to take in order to create output files
    :param file_format: output volume format (edf...)
    :param processed_data_folder_name: name of the processed data folder. Like 'reconstructed_volumes' or 'reconstructed_slices'...
    :return: (location, location_cfg_files). Location is the nabu configuration field 'output/location' 'location_cfg_files' is the information on where to save the nabu configuration file

    """
    output_mode = ProcessDataOutputDirMode.from_value(mode)
    file_format = NabuOutputFileFormat.from_value(file_format)

    if output_mode is ProcessDataOutputDirMode.OTHER and nabu_location in ("", None):
        _logger.error(
            "'other' output dir requested but no path provided. Fall back on the output dir to the scan folder"
        )
        # note: this is only an info because we expect to pass by this one for all .ows configuration (before 1.3 version)
        # as there was no different option by the time
        output_mode = ProcessDataOutputDirMode.IN_SCAN_FOLDER

    if output_mode is ProcessDataOutputDirMode.OTHER:
        location = format_output_location(nabu_location, scan=scan)
        location_cfg_files = location
    elif output_mode in (
        ProcessDataOutputDirMode.IN_SCAN_FOLDER,
        ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER,
    ):
        # otherwise default location will be the data root level
        location = os.path.join(scan.path, processed_data_folder_name)
        location_cfg_files = location
        if file_format in (
            NabuOutputFileFormat.EDF,
            NabuOutputFileFormat.TIFF,
            NabuOutputFileFormat.JP2K,
        ):  # if user specify the location
            location = "/".join([location, file_basename])
        if output_mode is ProcessDataOutputDirMode.PROCESSED_DATA_FOLDER:
            location = to_processed_data_path(location)
            location_cfg_files = to_processed_data_path(location_cfg_files)
    else:
        raise NotImplementedError(f"mode {output_mode.value} is not implemented yet")

    return location, location_cfg_files

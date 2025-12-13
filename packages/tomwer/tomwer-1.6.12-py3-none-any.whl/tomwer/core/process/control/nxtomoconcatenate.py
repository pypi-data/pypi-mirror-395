import os
import logging
from tomoscan.series import Series

from ewokscore.missing_data import is_missing_data

from tomwer.core.process.task import TaskWithProgress
from tomwer.core.scan.nxtomoscan import NXtomoScan

from nxtomo.application.nxtomo import NXtomo
from nxtomomill.utils.nexus import concatenate as nx_concatenate

_logger = logging.getLogger(__name__)


class ConcatenateNXtomoTask(
    TaskWithProgress,
    input_names=(
        "series",
        "output_file",
        "output_entry",
        "overwrite",
    ),
    optional_input_names=(
        "progress",
        "serialize_output_data",
    ),
    output_names=("data",),
):
    """
    Task used to concatenate a list of NXtomo (NXtomoScan) into a single NXtomo
    """

    def run(self):
        scans_series = self.inputs.series
        if is_missing_data(scans_series) or len(scans_series) < 1:
            raise ValueError("expected at least one nxtomo to be concatenated")
        elif not isinstance(scans_series, Series):
            raise TypeError(
                f"series is expected to be a Series. Get {type(scans_series)}"
            )

        # format output location if necessary
        output_file = format_output_location(
            file_path=self.inputs.output_file, series=scans_series
        )

        # cast scan from NXtomoScan to NXtomo
        def cast_scan_to_nxtomo(obj: NXtomoScan):
            # convert NXtomoScan to NXtomo as we expect to get NXtomoScan
            if isinstance(obj, NXtomoScan):
                return NXtomo().load(
                    file_path=obj.master_file,
                    data_path=obj.entry,
                )
            else:
                raise TypeError(
                    f"nxtomos are supposed to be instances of {NXtomo} or {NXtomoScan}. Get {type(obj)}"
                )

        scans_series = tuple([cast_scan_to_nxtomo(nxtomo) for nxtomo in scans_series])

        # apply concatenation
        output_nxtomo = nx_concatenate(scans_series)

        # dump result
        output_nxtomo.save(
            file_path=output_file,
            data_path=self.inputs.output_entry,
            overwrite=self.inputs.overwrite,
        )

        # cast back nxtomomill NXtomo to NXtomoScan (reference object for tomwer)
        scan = NXtomoScan(
            scan=output_file,
            entry=self.inputs.output_entry,
        )
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan


def format_output_location(file_path, series: Series):
    """
    format possible keys from the location like {scan_dir} or {scan_path}

    :param:
    :param: series of NXtomoScan
    :return:
    """
    if series is None:
        _logger.warning("scan is !none, enable to format the nabu output location")

    for scan in series:
        if not isinstance(scan, NXtomoScan):
            raise TypeError

    def get_common_path():
        if len(series) == 0:
            return ""
        elif len(series) == 1:
            return os.path.dirname(series[0].master_file)
        else:
            return os.path.commonpath(
                [os.path.dirname(scan.master_file) for scan in series]
            )

    keywords = {
        "common_path": get_common_path(),
    }

    # filter necessary keywords
    def get_necessary_keywords():
        import string

        formatter = string.Formatter()
        return [field for _, field, _, _ in formatter.parse(file_path) if field]

    requested_keywords = get_necessary_keywords()

    def keyword_needed(pair):
        keyword, _ = pair
        return keyword in requested_keywords

    keywords = dict(filter(keyword_needed, keywords.items()))
    file_path = file_path.format(**keywords)
    file_path = os.path.abspath(file_path)
    return file_path

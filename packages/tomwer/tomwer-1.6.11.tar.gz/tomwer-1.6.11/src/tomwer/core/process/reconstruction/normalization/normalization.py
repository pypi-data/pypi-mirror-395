# coding: utf-8

"""
material for radio and sinogram normalization
"""
from __future__ import annotations

import functools
import logging

import numpy
import tomoscan.esrf.scan.utils
from processview.core.dataset import DatasetIdentifier
from processview.core.superviseprocess import SuperviseProcess
from silx.io.url import DataUrl
from tomoscan.esrf.scan.utils import get_data
from tomoscan.normalization import Method as NormMethod

import tomwer.version
from tomwer.core.process.task import Task
from tomwer.core.utils.scanutils import data_identifier_to_scan

from .params import SinoNormalizationParams, _ValueCalculationFct, _ValueSource

_logger = logging.getLogger(__name__)


class SinoNormalizationTask(
    Task,
    SuperviseProcess,
    input_names=("data",),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """
    Task to define the normalization to apply to a sinogram before reconstructing it with nabu
    """

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        SuperviseProcess.__init__(self, process_id=process_id)
        self._dry_run = False
        if "configuration" in inputs:
            self.set_configuration(inputs["configuration"])

    def set_properties(self, properties):
        if isinstance(properties, SinoNormalizationParams):
            self._settings = properties.to_dict()
        else:
            self._settings = properties

    def set_configuration(self, configuration: dict) -> None:
        self.set_properties(configuration)

    def run(self):
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            return
        extra_infos = scan.intensity_normalization.get_extra_infos()
        extra_infos.update(
            {
                "tomwer_processing_res_code": None,
            }
        )
        scan.intensity_normalization.set_extra_infos(extra_infos)
        params = SinoNormalizationParams.from_dict(self._settings)
        # define the method used to the scan
        scan.intensity_normalization.method = params.method
        # after this processing the source
        try:
            if params.method in (NormMethod.NONE, NormMethod.CHEBYSHEV):
                final_norm_info = {}
            elif params.source is _ValueSource.MANUAL_ROI:
                value = self._compute_from_manual_roi(scan)
                # need_conversion_to_tomoscan = True
                # insure this could be hashable (for caches)
                if isinstance(value, numpy.ndarray):
                    value = tuple(value)
                final_norm_info = {
                    "value": value,
                    "source": _ValueSource.MANUAL_SCALAR.value,
                }
            elif params.source is _ValueSource.AUTO_ROI:
                value = self._compute_from_automatic_roi(scan)
                # need_conversion_to_tomoscan = True
                # insure this could be hashable (for caches)
                if isinstance(value, numpy.ndarray):
                    value = tuple(value)
                final_norm_info = {
                    "value": value,
                    "source": _ValueSource.MANUAL_SCALAR.value,
                }
            elif params.source is _ValueSource.DATASET:
                final_norm_info = {
                    "dataset_url": params.extra_infos.get("dataset_url", None),
                    "source": _ValueSource.DATASET.value,
                }
            elif params.source is _ValueSource.MANUAL_SCALAR:
                final_norm_info = {
                    "value": params.extra_infos.get("value", None),
                    "source": _ValueSource.MANUAL_SCALAR.value,
                }
            else:
                raise ValueError(f"method {params.method} is not handled")
        except Exception as e:
            _logger.error(e)
            final_norm_info = {"tomwer_processing_res_code": False}
        else:
            final_norm_info.update({"tomwer_processing_res_code": True})
        scan.intensity_normalization.set_extra_infos(final_norm_info)
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    def _compute_from_manual_roi(self, scan):
        params = SinoNormalizationParams.from_dict(self.get_configuration())
        extra_info = params.extra_infos
        start_x = extra_info.get("start_x", None)
        end_x = extra_info.get("end_x", None)
        start_y = extra_info.get("start_y", None)
        end_y = extra_info.get("end_y", None)

        calc_fct = extra_info.get("calc_fct", None)
        if calc_fct is None:
            raise ValueError("calc_fct should be provided")
        else:
            calc_fct = _ValueCalculationFct(calc_fct)

        try:
            value = self._cache_compute_from_manual_roi(
                dataset_identifier=scan.get_identifier(),
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
            )[calc_fct.value]
        except Exception as e:
            _logger.error(e)
            return None
        else:
            return value

    @staticmethod
    @functools.lru_cache(
        maxsize=6
    )  # maxsize=6 to at most keep info at volume and at frame level for 3 scans
    def _cache_compute_from_manual_roi(
        dataset_identifier: DatasetIdentifier,
        start_x,
        end_x,
        start_y,
        end_y,
    ) -> dict:
        """
        compute mean and median on a volume or a slice.
        To improve io performances compute both mean and median for both
        cases one per frame or one for the entire volume

        :param projections:
        :param start_x:
        :param end_x:
        :param start_y:
        :param end_y:
        :param calc_area:
        :return:
        """
        if start_x is None or end_x is None or start_y is None or end_y is None:
            raise ValueError("min_x, max_x, min_y and max_y should all be provided.")
        else:
            start_x = int(start_x)
            start_y = int(start_y)
            end_x = int(end_x)
            end_y = int(end_y)
        # clamp ROI with 0 border
        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = max(0, end_x)
        end_y = max(0, end_y)
        scan = dataset_identifier.recreate_dataset()
        projections = scan.projections

        roi_area = numpy.zeros(
            (len(projections), int(end_y - start_y), int(end_x - start_x))
        )
        # as dataset can be large we try to split the load of
        # the data
        proj_compacted = tomoscan.esrf.scan.utils.get_compacted_dataslices(
            projections,
            max_grp_size=20,
        )
        proj_indexes = sorted(proj_compacted.keys())
        # small hack to avoid loading several time the same url
        url_treated = set()

        def url_has_been_treated(url: DataUrl):
            return (
                url.file_path(),
                url.data_path(),
                url.data_slice().start,
                url.data_slice().stop,
                url.data_slice().step,
                url.scheme(),
            ) in url_treated

        def append_url(url: DataUrl):
            url_treated.add(
                (
                    url.file_path(),
                    url.data_path(),
                    url.data_slice().start,
                    url.data_slice().stop,
                    url.data_slice().step,
                    url.scheme(),
                )
            )

        current_idx = 0
        url_idxs = {v.path(): k for k, v in scan.projections.items()}
        for proj_index in proj_indexes:
            url = proj_compacted[proj_index]
            if url_has_been_treated(url):
                continue

            append_url(url)
            data = get_data(url)
            if data.ndim < 2:
                raise ValueError("data is expected to be at least 2D")
            # clamp ROI with frame size
            start_x = min(data.shape[-1], start_x)
            start_y = min(data.shape[-2], start_y)
            end_x = min(data.shape[-1], end_x)
            end_y = min(data.shape[-2], end_y)

            def retrieve_data_proj_indexes(url_):
                urls = []
                for data_slice in range(
                    url_.data_slice().start,
                    url_.data_slice().stop,
                    url_.data_slice().step or 1,
                ):
                    urls.append(
                        DataUrl(
                            file_path=url_.file_path(),
                            data_path=url_.data_path(),
                            scheme=url_.scheme(),
                            data_slice=data_slice,
                        )
                    )

                # try to retrieve the index from the projections else
                # keep the slice index as the frame index (should be the
                # case in most case
                res = []
                for my_url in urls:
                    my_url_path = my_url.path()
                    if my_url_path in url_idxs:
                        res.append(url_idxs[my_url_path])
                    else:
                        _logger.warning(
                            f"unable to retrieve frame index from url {my_url_path}. Take the slice index as frame index"
                        )
                return res

            data_indexes = retrieve_data_proj_indexes(url)
            # apply flat field correction
            if data.ndim == 2:
                projs = (data,)
            else:
                projs = list(data)
            data = scan.flat_field_correction(projs=projs, proj_indexes=data_indexes)
            if data is None:
                continue
            data = numpy.asarray(data)
            if data.ndim == 2:
                roi_area[current_idx] = data[start_y:end_y, start_x:end_x]
                current_idx += 1
            elif data.ndim == 3:
                length = data.shape[0]
                roi_area[current_idx : current_idx + length] = data[
                    :, start_y:end_y, start_x:end_x
                ]
                current_idx += length
            else:
                raise ValueError(f"Frame where expected and not a {data.ndim}D object")
        return SinoNormalizationTask.compute_stats(roi_area)

    @staticmethod
    def compute_stats(data):
        results = {}
        for calc_fct in _ValueCalculationFct:
            if data.ndim == 3:
                res = getattr(numpy, calc_fct.value)(data, axis=(-2, -1))
            elif data.ndim == 2:
                res = getattr(numpy, calc_fct.value)(data, axis=(-1))
            elif data.ndim in (0, 1):
                res = data
            else:
                raise ValueError(f"dataset dimension not handled ({data.ndim}D)")
            results[calc_fct.value] = res
        return results

    def _compute_from_automatic_roi(self, scan):
        raise NotImplementedError("Not implemented yet")

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "Intensity normalization"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "Normalize intensity."

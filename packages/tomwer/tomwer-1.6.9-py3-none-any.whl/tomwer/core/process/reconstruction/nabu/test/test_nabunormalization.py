# coding: utf-8
from __future__ import annotations

import configparser
from collections import namedtuple

import numpy
import pytest
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from tomwer.core.process.reconstruction.nabu import settings as nabu_settings
from tomwer.core.process.reconstruction.nabu.nabuslices import NabuSlicesTask
from tomwer.core.process.reconstruction.normalization.normalization import (
    SinoNormalizationTask,
)
from tomwer.core.process.reconstruction.normalization.params import (
    SinoNormalizationParams,
)
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_SLICES,
)

try:
    import nabu
except ImportError:
    has_nabu = False
else:
    has_nabu = True
import os

_norm_setting = namedtuple("_norm_setting", ["method", "source", "extra_infos"])

_nabu_norm_field = namedtuple(
    "_nabu_norm_field",
    ["sino_normalization", "has_sino_normalization_file"],
)


normalization_config_test = (
    # no normalization
    (
        _norm_setting(method="none", source=None, extra_infos=None),
        _nabu_norm_field(
            sino_normalization="",
            has_sino_normalization_file=False,
        ),
    ),
    # chebyshev normalization
    (
        _norm_setting(method="chebyshev", source=None, extra_infos=None),
        _nabu_norm_field(
            sino_normalization="chebyshev",
            has_sino_normalization_file=False,
        ),
    ),
    # divide by a scalar
    (
        _norm_setting(method="division", source="scalar", extra_infos={"value": 12.0}),
        _nabu_norm_field(
            sino_normalization="division",
            has_sino_normalization_file=True,
        ),
    ),
    # substract a roi
    (
        _norm_setting(
            method="subtraction",
            source="manual ROI",
            extra_infos={
                "start_x": 0.0,
                "end_x": 1.0,
                "start_y": 0.0,
                "end_y": 1.0,
                "calc_fct": "mean",
                "calc_area": "volume",
                "calc_method": "scalar",
            },
        ),
        _nabu_norm_field(
            sino_normalization="subtraction",
            has_sino_normalization_file=True,
        ),
    ),
    # substract from a dataset
    (
        _norm_setting(
            method="subtraction",
            source="from dataset",
            extra_infos={
                "dataset_url": DataUrl(
                    file_path="random_dataset.hdf5",
                    data_path="data",
                    scheme="silx",
                ),
                "calc_fct": "median",
                "calc_area": "volume",
                "calc_method": "scalar",
            },
        ),
        _nabu_norm_field(
            sino_normalization="subtraction",
            has_sino_normalization_file=True,
        ),
    ),
)


@pytest.mark.skipif(
    (not has_nabu or nabu.version < "2022.2"),
    reason="nabu not available or the current version doesn't handle sino normlaization yet",
)
@pytest.mark.parametrize(
    "norm_setting, expected_nabu_conf", [item for item in normalization_config_test]
)
def test_normalization(norm_setting, expected_nabu_conf, tmp_path):
    """
    Insure normalization is correctly provided to nabu configuration file
    For this run a normalization process followed by a nabu process.
    """
    scan_dir = tmp_path / "scan"
    scan_dir.mkdir()

    nabu_cfg_folders = os.path.join(scan_dir, nabu_settings.NABU_CFG_FILE_FOLDER)
    os.makedirs(nabu_cfg_folders, exist_ok=True)

    random_dataset_file = os.path.join(nabu_cfg_folders, "random_dataset.hdf5")

    # create a random dataset if necessary
    with HDF5File(random_dataset_file, mode="w") as h5f:
        h5f["data"] = numpy.ones((20, 20))

    mock = MockNXtomo(
        scan_path=scan_dir,
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=20,
    )
    scan = mock.scan

    cfg_folder = os.path.join(
        str(scan_dir), PROCESS_FOLDER_RECONSTRUCTED_SLICES, "nabu_cfg_files"
    )
    cfg_file = os.path.join(cfg_folder, "entry_scan.cfg")
    assert not os.path.exists(cfg_file)
    norm_params = SinoNormalizationParams(
        method=norm_setting.method,
        source=norm_setting.source,
        extra_infos=norm_setting.extra_infos,
    )

    normalization = SinoNormalizationTask(
        inputs={
            "data": scan,
            "configuration": norm_params.to_dict(),
            "serialize_output_data": False,
        },
        varinfo=None,
    )
    normalization.run()

    # insure the method is style valid
    assert scan.intensity_normalization.method.value == norm_setting.method
    assert (
        "tomwer_processing_res_code" in scan.intensity_normalization.get_extra_infos()
    )

    process = NabuSlicesTask(
        inputs={
            "data": scan,
            "dry_run": True,
            "nabu_params": get_default_nabu_config(nabu_fullfield_default_config),
            "serialize_output_data": False,
        },
        varinfo=None,
    )
    process.run()
    assert os.path.exists(cfg_file)

    configuration = configparser.ConfigParser(allow_no_value=True)
    configuration.read(cfg_file)

    preproc_section = configuration["preproc"]
    sino_normalization = preproc_section.get("sino_normalization", "")
    sino_normalization_file = preproc_section.get("sino_normalization_file", "")
    assert sino_normalization == expected_nabu_conf.sino_normalization
    if expected_nabu_conf.has_sino_normalization_file:
        url = DataUrl(path=sino_normalization_file)
        assert url.is_valid()
    else:
        assert sino_normalization_file == ""
    assert (
        "tomwer_processing_res_code" in scan.intensity_normalization.get_extra_infos()
    )

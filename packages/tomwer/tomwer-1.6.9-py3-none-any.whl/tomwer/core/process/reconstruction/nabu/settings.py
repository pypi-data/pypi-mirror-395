# coding: utf-8
from __future__ import annotations

import logging

_logger = logging.getLogger(__name__)


NABU_CONFIG_FILE_EXTENSION = ".cfg"

NABU_CFG_FILE_FOLDER = "nabu_cfg_files"
# foler where nabu configuraiton will be saved

NABU_TOMWER_SERVING_HATCH = "nabu_tomwer_serving_hatch.h5"
# file used to insure some passing from tomwer to nabu like providing normalization values

try:
    import nabu.app.reconstruct  # noqa: F401
except ImportError:
    try:
        import nabu.resources.cli.reconstruct  # noqa: F401
    except ImportError:
        _logger.warning(
            "Fail to get path to nabu reconstruct main path. Take the most recent path"
        )
        NABU_FULL_FIELD_APP_PATH = "nabu.app.reconstruct"
    else:
        NABU_FULL_FIELD_APP_PATH = "nabu.resources.cli.reconstruct"
else:
    NABU_FULL_FIELD_APP_PATH = "nabu.app.reconstruct"


NABU_CAST_APP_PATH = "nabu.app.cast_volume"

NABU_MULTICOR_PATH = "nabu.app.multicor"

# coding: utf-8

import logging
import resource

_logger = logging.getLogger(__name__)


def increase_max_number_file():
    """increase the maximal number of file the software can open within respect of the hard limit"""
    try:
        hard_nofile = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
        resource.setrlimit(resource.RLIMIT_NOFILE, (hard_nofile, hard_nofile))
    except (ValueError, OSError):
        _logger.warning("Failed to retrieve and set the max opened files limit")
    else:
        _logger.debug("Set max opened files to %d", hard_nofile)

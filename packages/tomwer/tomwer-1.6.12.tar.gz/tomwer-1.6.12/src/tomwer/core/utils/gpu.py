# coding: utf-8

import logging

_logger = logging.getLogger(__name__)


def getNumberOfDevice():
    try:
        import pycuda  # noqa F401  pylint: disable=E0401
        from pycuda import compiler  # noqa F401  pylint: disable=E0401
        from pycuda import driver  # pylint: disable=E0401

        driver.init()
        return driver.Device.count()
    except Exception:
        _logger.error("fail to discover the number of gpu")
        return None

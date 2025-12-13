"""
Orange add-on for tomography
"""

import logging

from . import state_summary  # noqa F401

fabio_logger = logging.getLogger("fabio.edfimage")
fabio_logger.setLevel(logging.WARNING)

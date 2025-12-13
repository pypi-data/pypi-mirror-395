#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Application to stitch along z (aka axis 0) a set of scans or reconstructed volumes
"""
from __future__ import annotations

import sys
import logging
from tomwer.app.stitching.common import main as common_main

logging.basicConfig(level=logging.WARNING)

_logger = logging.getLogger(__name__)


def getinputinfo():
    return "tomwer z-stitching [tomo objects]"


def main(argv):
    common_main(argv, stitcher_name="z-stitching", stitching_axis=0, logger=_logger)


if __name__ == "__main__":
    main(sys.argv)

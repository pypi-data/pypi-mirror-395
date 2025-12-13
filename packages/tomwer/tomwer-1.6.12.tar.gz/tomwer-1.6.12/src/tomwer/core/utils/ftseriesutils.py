# coding: utf-8
from __future__ import annotations

import logging
import operator
import os

logger = logging.getLogger(__name__)


def get_vol_file_shape(file_path):
    ddict = {}
    f = open(file_path, "r")
    lines = f.readlines()
    for line in lines:
        if "=" not in line:
            continue
        line_str = line.rstrip().replace(" ", "")
        line_str = line_str.split("#")[0]
        key, value = line_str.split("=")
        ddict[key.lower()] = value

    dimX = None
    dimY = None
    dimZ = None

    if "num_z" in ddict:
        dimZ = int(ddict["num_z"])
    if "num_y" in ddict:
        dimY = int(ddict["num_y"])
    if "num_x" in ddict:
        dimX = int(ddict["num_x"])

    return (dimZ, dimY, dimX)


def orderFileByLastLastModification(folder, fileList):
    """Return the list of files sorted by time of last modification.
    From the oldest to the newest modify"""
    res = {}
    for f in fileList:
        res[os.path.getmtime(os.path.join(folder, f))] = f

    return sorted(res.items(), key=operator.itemgetter(0))

# coding: utf-8
from __future__ import annotations


# TODO: change this for enum

OBSERVATION_STATUS = {
    "not processing": 0,  # data watcher is not doing anything
    "parsing": 1,  # data watcher is parsing folders
    "none found": 2,  # data watcher haven't found anything
    "starting": 3,  # data watcher have found an acquisition starting
    "started": 4,  # data watcher have found an acquisition started
    "waiting for acquisition ending": 5,  # data watcher is waiting for all .edf file to be copied
    "acquisition ended": 6,  # data watcher have found an acquisition completed
    "acquisition canceled": 7,  # data watcher have found an acquisition canceled
    "failure": -1,  # data watcher have encountered an issue. Should be associated with an info describing it
    "aborted": -2,  # if aborted by acquisition
}

DICT_OBS_STATUS = {}
for name, value in OBSERVATION_STATUS.items():
    DICT_OBS_STATUS[value] = name

" Possible status of a data watcher observation"

DET_END_XML = "[scan].xml"
"""DET_END for detection end.
In this case we are looking for the scan.xml file. On it is here then the
acquisition is considered ended
"""

PARSE_INFO_FILE = "[scan].info"
"""
In this case we will end for the .info to be here and then parse it to know how
many .edf file we are waiting for and wait for all of them to be recorded.
"""

DET_END_USER_ENTRY = "from file pattern"
"""DET_END for detection end.
In this case the user specify the pattern we are looking for
"""

DET_END_METHODS = (DET_END_XML, PARSE_INFO_FILE, DET_END_USER_ENTRY)
"""List of option that can notice the end of the acquisition"""


BLISS_SCAN_END = "bliss scan - end_time dataset"


NXtomo_END = "already converted NXtomo"

EDF_SCAN_END = "Any EDF scan"

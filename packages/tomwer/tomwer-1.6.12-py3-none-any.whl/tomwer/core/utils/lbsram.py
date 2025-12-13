import os
import psutil
from tomwer.core import settings

MOCK_LOW_MEM = False  # if True will simulate the case the computer run into low memory

IGNORE_LOW_MEM = False


def is_low_on_memory(path=""):
    """

    :return: True if the RAM usage is more than MAX_MEM_USED (or low memory
       is simulated)
    """
    if IGNORE_LOW_MEM is True:
        return False
    if path == settings.get_dest_path():
        if settings.MOCK_LBSRAM is True:
            return MOCK_LOW_MEM
        else:
            assert os.path.isdir(path)
            return psutil.disk_usage(path).percent > settings.MAX_MEM_USED
    else:
        return (MOCK_LOW_MEM is True) or (
            os.path.exists(path)
            and (psutil.disk_usage(path).percent > settings.MAX_MEM_USED)
        )


def mock_low_memory(b=True):
    """Mock the case the computer is running into low memory"""
    global MOCK_LOW_MEM
    MOCK_LOW_MEM = b
    return psutil.virtual_memory().percent > settings.MAX_MEM_USED

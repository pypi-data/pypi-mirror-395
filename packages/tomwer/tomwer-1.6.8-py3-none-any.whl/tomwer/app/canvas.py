"""Application to define a tomography workflow (also as know as 'ewoks-canvas' or 'orange canvas')"""

import logging
import platform
import sys

import psutil

from tomwer.app.canvas_launcher.mainwindow import OMain as QMain
from tomwer.app.canvas_launcher.utils import get_tomotools_stack_versions
from tomwer.core.utils.resource import increase_max_number_file

_logger = logging.getLogger(__name__)


def print_versions():
    """Prints the Tomotools packages versions"""
    print(
        "\n - ".join(
            [
                "Tomotools packages versions:",
            ]
            + list(
                [
                    f"{soft_name: <11}: {version}"
                    for soft_name, version in get_tomotools_stack_versions().items()
                ]
            )
        )
    )


def check_free_space():
    """Check if enough space exists. Else could bring issues on processing"""
    if platform.system() == "Linux":
        try:
            free_home_space = psutil.disk_usage("/home").free
        except OSError:
            pass
        else:
            if free_home_space < 100 * 1024 * 1024:
                # if no space Qt might fail to create the display and log file not be created
                _logger.warning(
                    f"only {free_home_space / 1024} ko available. Display might fail"
                )


def main(argv=None):
    print_versions()
    check_free_space()
    increase_max_number_file()
    return QMain().run(argv)


if __name__ == "__main__":
    sys.exit(main())

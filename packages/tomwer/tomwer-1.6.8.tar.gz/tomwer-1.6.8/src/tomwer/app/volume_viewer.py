#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application to browse a given scan"""

import numpy
import argparse
import logging
import signal
import sys

import silx
from silx.gui import qt

from tomwer.tasks.visualization.volume_viewer import VolumeViewerTask
from tomwer.core.volume.volumefactory import VolumeFactory
from tomoscan.esrf.volume.utils import guess_volumes
from tomwer.core.utils.resource import increase_max_number_file
from tomwer.gui import icons
from tomwer.gui.utils.splashscreen import getMainSplashScreen
from tomwer.gui.visualization.volume_viewer.VolumeViewerWindow import (
    VolumeViewerWindow,
)

logging.basicConfig(level=logging.WARNING)
_logger = logging.getLogger(__name__)


class VolumeSummaryTaskThread(qt.QThread):
    def __init__(self, parent, inputs):
        super().__init__(parent)
        self._inputs = inputs

    def run(self):
        self._task = VolumeViewerTask(inputs=self._inputs)
        self._task.execute()

    def result(self):
        return {
            "slices": self._task.outputs.slices,
            "metadata": self._task.outputs.volume_metadata,
            "volume_shape": self._task.outputs.volume_shape,
        }

    def get_loaded_volume_data(self) -> numpy.array:
        return self._task.outputs.loaded_volume


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "volume",
        help="Volume identifier or location of the volume to display",
    )
    parser.add_argument(
        "--load-volume",
        help="Load the full volume in memory. Allows fast browsing along the three axis.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--use-opengl-plot",
        help="Use OpenGL for plots (instead of matplotlib)",
        action="store_true",
        default=False,
    )

    options = parser.parse_args(argv[1:])

    try:
        volumes = VolumeFactory.create_tomo_object_from_identifier(options.volume)
    except Exception:
        volumes = []

    if len(volumes) == 0:
        volumes = guess_volumes(
            options.volume,
        )

    if len(volumes) == 0:
        raise ValueError(f"No volume found in {options.volume}")
    if len(volumes) > 1:
        _logger.warning(
            f"More than one volume found in {options.volume}. Pick the first one."
        )

    volume = VolumeFactory.create_tomo_object_from_identifier(
        volumes[0].get_identifier().to_str()
    )

    if options.use_opengl_plot:
        silx.config.DEFAULT_PLOT_BACKEND = "gl"
    else:
        silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    increase_max_number_file()

    global app  # QApplication must be global to avoid seg fault on quit

    app = qt.QApplication.instance() or qt.QApplication(["tomwer"])
    splash = getMainSplashScreen()
    qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor)
    qt.QApplication.processEvents()

    qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
    qt.QLocale.setDefault(qt.QLocale.c())
    signal.signal(signal.SIGINT, sigintHandler)
    sys.excepthook = qt.exceptionHandler

    timer = qt.QTimer()
    timer.start(500)
    # Application have to wake up Python interpreter, else SIGINT is not
    # catch
    timer.timeout.connect(lambda: None)

    window = VolumeViewerWindow(parent=None)
    # there is options from the CLI to load or not the volume at start. This option has no sense
    # in the CLI tool.
    window.setLoadingVolumeOptionVisible(False)
    window.setWindowTitle("tomwer: volume-viewer")
    window.setWindowIcon(icons.getQIcon("tomwer"))

    if options.load_volume:
        loading_message = "Loading volume."
    else:
        loading_message = "Loading slices."
    window.initVolumePreview(volume, message=loading_message)
    splash.finish(window)
    window.show()

    taskThread = VolumeSummaryTaskThread(
        parent=window,
        inputs={
            "volume": volume,
            "load_volume": options.load_volume,
        },
    )
    taskThread.finished.connect(
        lambda: window.setSlicesAndMetadata(**taskThread.result())
    )
    if options.load_volume:
        taskThread.finished.connect(
            lambda: window.setVolume(taskThread.get_loaded_volume_data())
        )
    taskThread.finished.connect(lambda: window.setLoading(False))
    taskThread.start()

    qt.QApplication.restoreOverrideCursor()
    app.aboutToQuit.connect(window.close)
    exit(app.exec())


def getinputinfo():
    return "tomwer volume-viewer [file_path] [[file_entry]]"


def sigintHandler(*args):
    """Handler for the SIGINT signal."""
    qt.QApplication.closeAllWindows()  # needed because get a waiting thread behind
    qt.QApplication.quit()


if __name__ == "__main__":
    main(sys.argv)

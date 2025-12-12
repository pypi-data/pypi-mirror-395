from __future__ import annotations


import logging
import os

import numpy.lib.npyio
from silx.gui import qt

import tomwer.resources
from tomwer.io.utils import get_slice_data

logger = logging.getLogger(__name__)


class ImageLoaderThread(qt.QThread):
    """Thread used to load an image"""

    IMG_NOT_FOUND = numpy.load(
        tomwer.resources._resource_filename(
            "%s.%s" % ("imageNotFound", "npy"),
            default_directory=os.path.join("gui", "icons"),
        )
    )

    def __init__(self, url, *args, **kwargs):
        """

        :param index: index of the image on the stackplot
        :param filePath: filePath is the file to load on stackplot reference.
                         It can be an .edf file or a .vol file. If this is a
                         vol file then the name is given with the slice z index
                         to be loaded.
        """
        super().__init__(*args, **kwargs)
        self.data = None
        self.url = url

    def getData(self):
        if hasattr(self, "data"):
            return self.data
        else:
            return None

    def run(self):
        if os.path.exists(self.url.file_path()) and os.path.isfile(
            self.url.file_path()
        ):
            self.data = get_slice_data(self.url)
        else:
            logger.warning("file %s not longer exists or is empty" % self.url)
            self.data = self.IMG_NOT_FOUND

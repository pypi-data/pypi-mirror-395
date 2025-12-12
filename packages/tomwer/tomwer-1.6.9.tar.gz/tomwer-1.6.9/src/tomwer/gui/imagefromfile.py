"""Utils to load images from file"""

from __future__ import annotations


import functools
import logging

from silx.gui import qt
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.synctools.imageloaderthread import ImageLoaderThread

logger = logging.getLogger(__name__)


class _Image(qt.QObject):
    def __init__(self, data):
        qt.QObject.__init__(self)
        self.data = data


class ImageFromFile(_Image):
    """
    Define an Image with a status
    """

    LOADING_STATUS = {"loading": 0, "loaded": 1, "not loaded": 2}
    sigLoaded = qt.Signal(str)
    """Signal emitted when the file is loaded. Parameter is the file url"""

    def __init__(self, _file=None, index=None, data=None, _load=False, url=None):
        _Image.__init__(self, data)
        if url is not None:
            assert _file is None and index is None
            self.url = url
        else:
            assert isinstance(_file, str)
            data_path = None
            if _file.lower().endswith(".edf"):
                scheme = "fabio"
            else:

                def get_nabu_entry():
                    try:
                        with open_hdf5(_file) as h5s:
                            for node in h5s:
                                if "reconstruction" in h5s[node]:
                                    return "/".join(
                                        (node, "reconstruction", "results", "data")
                                    )
                    except Exception as e:
                        logger.error(e)

                data_path = get_nabu_entry() or None
                scheme = "silx"

            if index is not None:
                data_slice = (index,)
            else:
                data_slice = None
            self.url = DataUrl(
                file_path=_file,
                data_slice=data_slice,
                scheme=scheme,
                data_path=data_path,
            )

        self._status = "not loaded" if data is None else "loaded"
        self.url_path = self.url.path()
        if _load is True:
            self.load()

    def load(self, sync=False):
        """
        Load the data contained in the url.

        :param sync: if True: then wait for the image to be loaded for giving
            back hand
        """
        if self._status == "loaded" and self.data is not None:
            self.sigLoaded.emit(self.url.path())
        elif self._status == "loading":
            logger.debug("%s is already loading" % self.url.path())
        else:
            self._status = "loading"
            self.loaderThread = ImageLoaderThread(url=self.url)

            callback = functools.partial(
                self._setData, self.url_path, self.loaderThread.getData
            )
            self.loaderThread.finished.connect(callback)
            self.loaderThread.start()
            if sync is False:
                self.loaderThread.wait()

    def _setData(self, url_path, dataGetter):
        self.data = dataGetter()
        if self.data is not None:
            if self.data.ndim != 2:
                if self.data.shape[0] == 1:
                    self.data = self.data.reshape(self.data.shape[1:])
                elif self.data.shape[-1] == 1:
                    self.data = self.data.reshape(self.data.shape[0:-1])

        self._status = "loaded"
        self.sigLoaded.emit(url_path)

    def isLoaded(self):
        return self._status == "loaded"


class FileWithImage(object):
    """Definition of file which can contain multiple images"""

    def __init__(self, _file):
        self.file = _file

    def getImages(self, _load):
        """

        :param _load: if True then launch the load of the image
        :return: the list of images contained in the given file.
        """
        if self.file.lower().endswith(TomwerScanBase.VALID_RECONS_EXTENSION):
            return [ImageFromFile(self.file)]
        else:
            logger.error("only deal with .edf and .vol extension")
            return []

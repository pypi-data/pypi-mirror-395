"""Contains the QImageFileStackPlot. Widget to display a set of files with metadata (either scan or volume metadata)"""

from __future__ import annotations

import logging
import os
import time

from silx.gui import qt
from tomwer.gui.visualization.imagestack import ImageStack


from . import utils

logger = logging.getLogger(__name__)


class QImageFileStackPlot(ImageStack):
    """
    Widget based on ImageStack and adding some widget to display metadata associated with urls.
    Like Paganin delta / beta values...
    """

    def __init__(self, parent, show_overview=True, backend=None):
        """
        Constructor

        :param parent: the Qt parent widget
        """
        super().__init__(parent, show_overview=show_overview)

        self._plot.setBackend(backend=backend)

        self._imagejThreads = []

        # dock widget: qslider
        self._plot.layout()
        self._fileInfoDockWidget = qt.QDockWidget(parent=self)
        self._fileInfoWidget = self.__buildFileInfo()
        self._fileInfoDockWidget.setWidget(self._fileInfoWidget)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._fileInfoDockWidget)
        self._fileInfoDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)

        # connect signal / slot
        self._openWithImjButton.released.connect(self._openCurrentInImagej)
        self.sigCurrentUrlChanged.connect(self._updateUrlInfos)

    def __buildFileInfo(self):
        self._fileInfoWidget = qt.QWidget(parent=self)
        layout = qt.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self._fileInfoWidget.setLayout(layout)

        # file name label
        layout.addWidget(qt.QLabel("file :", self._fileInfoWidget), 0, 0, 1, 1)
        self._qlFileName = qt.QLabel("", parent=self._fileInfoWidget)
        layout.addWidget(self._qlFileName, 0, 1, 1, 2)

        # open in image j button
        style = qt.QApplication.style()
        open_icon = style.standardIcon(qt.QStyle.SP_FileLinkIcon)
        self._openWithImjButton = qt.QPushButton(
            open_icon, "open with ImageJ", parent=self
        )
        self._openWithImjButton.setSizePolicy(
            qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum
        )
        layout.addWidget(self._openWithImjButton, 0, 3, 1, 1)

        # date last modification
        layout.addWidget(
            qt.QLabel("last modification :", self._fileInfoWidget), 1, 0, 1, 1
        )
        self._qlLastModifications = qt.QLabel("", parent=self._fileInfoWidget)
        layout.addWidget(self._qlLastModifications, 1, 1, 1, 2)

        return self._fileInfoWidget

    def _openCurrentInImagej(self):
        current_url = self.getCurrentUrl()
        if current_url is None:
            logger.warning("No active image defined")
        else:
            try:
                self._imagejThreads.append(utils.open_url_with_image_j(current_url))
            except OSError as e:
                msg = qt.QMessageBox(self)
                msg.setIcon(qt.QMessageBox.Warning)
                msg.setWindowTitle("Unable to open image in imagej")
                msg.setText(str(e))
                msg.exec()

    def _updateUrlInfos(self):
        url = self.getCurrentUrl()
        name = url.file_path().split(os.path.sep)[-1]

        self._qlFileName.setText(name)
        self._qlFileName.setToolTip(url.path())
        try:
            last_mod = time.ctime(os.path.getmtime(url.file_path()))
        except Exception:
            last_mod = ""
        self._qlLastModifications.setText(last_mod)

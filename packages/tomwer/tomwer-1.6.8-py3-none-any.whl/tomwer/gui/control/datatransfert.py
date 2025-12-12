# coding: utf-8
from __future__ import annotations

import logging
import os

from silx.gui import qt

from tomwer.io.utils import get_default_directory

_logger = logging.getLogger(__file__)


class DataTransfertSelector(qt.QWidget):
    """
    Simple GUI for selecting the datatransfert root folder
    """

    sigSelectionChanged = qt.Signal(str)
    """If None: default mode, send it to rnice, else send it to the given root
    folder"""

    def __init__(self, parent, rnice_option, default_root_folder):
        qt.QWidget.__init__(self, parent)
        assert type(default_root_folder) is str
        assert type(rnice_option) is bool
        self.setLayout(qt.QVBoxLayout(self))
        self.layout().setSpacing(0)

        self._buttonGrp = qt.QButtonGroup(self)
        self._buttonGrp.setExclusive(True)

        # rnice option
        if rnice_option is True:
            self._rniceOpt = qt.QRadioButton("to rnice", self)
            self._rniceOpt.setChecked(True)
            self._buttonGrp.addButton(self._rniceOpt)
        else:
            self._rniceOpt = None
        self.layout().addWidget(self._rniceOpt)

        # folder option
        self._rootFolderOpt = qt.QWidget(parent=self)
        self._rootFolderOpt.setLayout(qt.QHBoxLayout())
        self._rootFolderOpt.layout().setContentsMargins(0, 0, 0, 0)
        self._folderOpt = qt.QRadioButton("to root folder", self._rootFolderOpt)
        self._buttonGrp.addButton(self._folderOpt)
        self._folderOpt.setChecked(not rnice_option)
        self._rootFolderOpt.layout().addWidget(self._folderOpt)

        self._folderSelection = qt.QLineEdit(
            default_root_folder or get_default_directory(), self._rootFolderOpt
        )
        self._rootFolderOpt.layout().addWidget(self._folderSelection)

        self._folderSelPB = qt.QPushButton("select folder", self._folderSelection)
        self._folderSelPB.setAutoDefault(True)
        self._rootFolderOpt.layout().addWidget(self._folderSelPB)
        self.layout().addWidget(self._rootFolderOpt)

        # default visibility values
        self._updateFolderVisibility(not rnice_option)

        # connect signal / SLOT
        self._folderOpt.toggled.connect(self._updateFolderVisibility)
        if self._rniceOpt:
            self._rniceOpt.toggled.connect(self._updateRniceAction)

        self._folderSelPB.clicked.connect(self._changeFolder)
        self._folderSelection.textChanged.connect(self.__updateFolder)

    def __updateFolder(self, folder_path):
        """Inform connected QObject that the selection just changed"""
        assert folder_path is None or type(folder_path) is str
        self.sigSelectionChanged.emit(folder_path)

    def _updateFolderVisibility(self, b):
        """Deal with the select folder widget visibility"""
        self._folderSelection.setEnabled(b)
        self._folderSelPB.setEnabled(b)
        if b is True:
            self.__updateFolder(self._folderSelection.text())

    def _updateRniceAction(self, b):
        """if necessary connect with rnice radio button with __updateFolder"""
        if b is True:
            self.__updateFolder(None)

    def _changeFolder(self):  # pragma: no cover
        """Callback when folder selection is choose"""
        defaultDirectory = self._folderSelection.text()
        if os.path.isdir(defaultDirectory):
            defaultDirectory = get_default_directory()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec():
            dialog.close()
            return

        self._folderSelection.setText(dialog.selectedFiles()[0])

    def setFolder(self, folder_path):
        """
        Define the root folder to move scan

        :param folder_path: root folder for received scan
        """
        assert type(folder_path) is str or folder_path is None
        if folder_path is None:
            if self._rniceOpt is None:
                _logger.warning("rnice option is not available")
            else:
                self._rniceOpt.setChecked(True)
        else:
            self._folderOpt.setChecked(True)
            self._folderSelection.setText(folder_path)

    def getFolder(self):
        if self._rniceOpt.isChecked():
            return None
        else:
            return self._folderSelection.text()

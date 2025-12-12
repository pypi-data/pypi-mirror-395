"""contains dialogs to select a Scan (aka Data)"""

from __future__ import annotations

import logging
import os

from silx.gui import qt


_logger = logging.getLogger()


class QDataDialog(qt.QFileDialog):
    """dialog to select a scans (aka data)"""

    def __init__(self, parent, multiSelection=False):
        qt.QFileDialog.__init__(self, parent)
        self.setNameFilters(
            [
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
                "Any files (*)",
            ]
        )
        self._selected_files = []
        self.setFileMode(qt.QFileDialog.ExistingFiles)

        # self.QDialogButtonBox
        self.multiSelection = multiSelection
        # check if 'TOMWER_DEFAULT_INPUT_DIR' has been set
        if os.environ.get("TOMWER_DEFAULT_INPUT_DIR", None) and os.path.exists(
            os.environ["TOMWER_DEFAULT_INPUT_DIR"]
        ):
            self.setDirectory(os.environ["TOMWER_DEFAULT_INPUT_DIR"])
        elif self.directory() != os.getcwd() or str(self.directory()).startswith(
            "/data"
        ):
            # if the directory as already been set by the user. Avoid redefining it
            pass
        elif os.path.isdir("/data"):
            self.setDirectory("/data")

        btns = self.findChildren(qt.QPushButton)
        if len(btns) == 0:
            _logger.error(
                "Cannot retrieve open button. switch to none " "native QFileDialog"
            )
            self.setOption(qt.QFileDialog.DontUseNativeDialog)
            btns = self.findChildren(qt.QPushButton)

        if self.multiSelection is True:
            # to make it possible to select multiple directories:
            self.file_view = self.findChild(qt.QListView, "listView")
            if self.file_view:
                self.file_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                self.file_view.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

            self.f_tree_view = self.findChild(qt.QTreeView)
            if self.f_tree_view:
                self.f_tree_view.setSelectionMode(qt.QAbstractItemView.MultiSelection)
                self.f_tree_view.setSelectionMode(
                    qt.QAbstractItemView.ExtendedSelection
                )

            if len(btns) > 0:
                self.openBtn = [x for x in btns if "open" in str(x.text()).lower()][0]
                self.openBtn.clicked.disconnect()
                self.openBtn.hide()
                parent = self.openBtn.parent()
                self.openBtn = qt.QPushButton("Select", parent=parent)
                self.openBtn.clicked.connect(self.openClicked)
                parent.layout().insertWidget(0, self.openBtn)

    def openClicked(self):
        inds = self.f_tree_view.selectionModel().selectedIndexes()
        for i in inds:
            if i.column() == 0:
                self._selected_files.append(
                    os.path.join(str(self.directory().absolutePath()), str(i.data()))
                )
        self.accept()
        self.done(1)

    def files_selected(self):
        for file_ in self.selectedFiles():
            self._selected_files.append(file_)
        return self._selected_files

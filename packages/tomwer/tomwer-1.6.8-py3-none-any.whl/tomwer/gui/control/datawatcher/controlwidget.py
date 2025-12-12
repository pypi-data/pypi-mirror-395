import os
from tomwer.gui.qlefilesystem import QLFileSystem
from silx.gui import qt, icons as silxicons
from tomwer.io.utils import get_default_directory


class ControlWidget(qt.QWidget):
    _TXT_STOP_OBS = "Stop observation"
    _TXT_START_OBS = "Start observation"

    def __init__(self, parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.setLayout(qt.QVBoxLayout())
        layout = self.layout()

        self.mystatusBar = qt.QStatusBar(parent=self)
        self._qlInfo = qt.QLabel(parent=self)

        layout.addWidget(self._getFolderSelection())
        layout.addWidget(self._qlInfo)
        layout.addWidget(self._buildFilterWidget())
        layout.addWidget(self._buildStartStopButton())
        layout.addWidget(self.mystatusBar)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        layout.addWidget(spacer)

    def _getFolderSelection(self):
        """
        Return the widget used for the folder selection
        """
        widget = qt.QWidget(self)
        layout = qt.QHBoxLayout()

        self._qtbSelectFolder = qt.QPushButton("Select folder", parent=widget)
        self._qtbSelectFolder.setAutoDefault(True)
        self._qtbSelectFolder.clicked.connect(self._setFolderPath)

        self._qteFolderSelected = QLFileSystem("", parent=widget)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._qteFolderSelected)
        layout.addWidget(self._qtbSelectFolder)

        self.animated_icon = silxicons.getWaitIcon()
        self._stateLabel = qt.QLabel(parent=widget)
        self.animated_icon.register(self._stateLabel)

        self._stateLabel.setFixedWidth(30)
        layout.addWidget(self._stateLabel)

        widget.setLayout(layout)
        return widget

    def _buildFilterWidget(self):
        widget = qt.QWidget(self)
        layout = qt.QHBoxLayout()
        widget.setLayout(layout)
        widget.layout().addWidget(qt.QLabel("filter"))
        self._filterQLE = qt.QLineEdit("", self)
        self._filterQLE.setToolTip(
            "You can provide a Linux Regular Expression that will insure only file fitting the expression will be discovered"
        )
        self._filterQLE.setPlaceholderText("*file_pattern*")
        widget.layout().addWidget(self._filterQLE)

        return widget

    def _buildStartStopButton(self):
        """
        Build the start/stop button in a QHLayout with one spacer on the left
        and one on the right
        """
        widget = qt.QWidget(self)
        layout = qt.QHBoxLayout()
        widget.setLayout(layout)

        # left spacer
        spacerL = qt.QWidget(widget)
        spacerL.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(spacerL)

        # button
        self._qpbstartstop = qt.QPushButton(self._TXT_START_OBS)
        self._qpbstartstop.setAutoDefault(True)
        layout.addWidget(self._qpbstartstop)

        # right spacer
        spacerR = qt.QWidget(widget)
        spacerR.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(spacerR)

        return widget

    def _setFolderPath(self):  # pragma: no cover
        """
        Ask the user the path to the folder to observe
        """
        defaultDirectory = self._qteFolderSelected.text()
        if defaultDirectory is None or not os.path.isdir(defaultDirectory):
            if defaultDirectory is None:
                defaultDirectory = get_default_directory()

        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)

        if not dialog.exec():
            dialog.close()
            return

        self._qteFolderSelected.setText(dialog.selectedFiles()[0])

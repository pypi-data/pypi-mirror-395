from __future__ import annotations

from silx.gui import qt

from tomwer.core.scan.scantype import ScanType
from tomwer.gui.control import datareacheractions
from tomwer.gui.control.datawatcher.controlwidget import ControlWidget


class ScanDiscoveryConfigWidget(qt.QGroupBox):
    sigScanTypeChanged = qt.Signal()
    """emit when scan typo change"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLayout(qt.QVBoxLayout())
        self._nxtomoQRB = qt.QRadioButton(ScanType.NX_TOMO.value, parent=self)
        self.layout().addWidget(self._nxtomoQRB)

        self._blissQRB = qt.QRadioButton(ScanType.BLISS.value, parent=self)
        self.layout().addWidget(self._blissQRB)

        self._specQRB = qt.QRadioButton(ScanType.SPEC.value, parent=self)
        self.layout().addWidget(self._specQRB)

        # set up
        self._nxtomoQRB.setChecked(True)
        # connect signal / slot
        self._nxtomoQRB.toggled.connect(self._configChanged)
        self._blissQRB.toggled.connect(self._configChanged)
        self._specQRB.toggled.connect(self._configChanged)

    def _configChanged(self, *args, **kwargs):
        self.sigScanTypeChanged.emit()

    def getScanType(self) -> ScanType:
        if self._specQRB.isChecked():
            return ScanType.SPEC
        elif self._blissQRB.isChecked():
            return ScanType.BLISS
        elif self._nxtomoQRB.isChecked():
            return ScanType.NX_TOMO
        else:
            raise NotImplementedError

    def setScanType(self, mode: ScanType):
        mode = ScanType(mode)
        if mode is ScanType.SPEC:
            self._specQRB.setChecked(True)
        elif mode is ScanType.BLISS:
            self._blissQRB.setChecked(True)
        elif mode is ScanType.NX_TOMO:
            self._nxtomoQRB.setChecked(True)
        else:
            raise NotImplementedError


class _MainWidget(qt.QWidget):
    sigStart = qt.Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())
        self.controlWidget = ControlWidget()
        self.layout().addWidget(self.controlWidget)
        self.configWidget = ScanDiscoveryConfigWidget(parent=self)
        self.layout().addWidget(self.configWidget)

        # set up
        self.configWidget.setVisible(False)
        self.controlWidget.setVisible(False)
        self.controlWidget._qpbstartstop.setText("start discovery")
        # connect signal / slot
        self.controlWidget._qpbstartstop.released.connect(self._startDiscovery)
        # expose api
        self.sigScanTypeChanged = self.configWidget.sigScanTypeChanged

    def getConfigWindow(self):
        return self.configWidget

    def _startDiscovery(self):
        self.sigStart.emit()

    def getFolderObserved(self):
        return self.controlWidget._qteFolderSelected.text()

    def setFolderObserved(self, dir_):
        return self.controlWidget._qteFolderSelected.setText(dir_)

    def getLinuxFilePattern(self) -> str | None:
        text = self.controlWidget._filterQLE.text()
        if text.replace(" ", "") == "":
            return None
        else:
            return text

    def setLinuxFilePattern(self, pattern: str | None):
        if pattern is None:
            pattern = ""
        self.controlWidget._filterQLE.setText(pattern)

    def setSearchScanType(self, scan_type):
        self.configWidget.setScanType(scan_type)

    def getSearchScqnType(self):
        return self.configWidget.getScanType()


class DataDiscoveryWidget(qt.QMainWindow):
    sigTMStatusChanged = qt.Signal(str)
    """Signal emitted when the state changed"""
    sigScanReady = qt.Signal(object)
    """Signal emitted when a scan is considered as ready"""
    sigFolderObservedChanged = qt.Signal()
    """Signal emitted when the user change the observed folder"""
    sigObservationStart = qt.Signal()
    """Signal emitted when the observation starts"""
    sigObservationEnd = qt.Signal()
    """Signal emitted when the observation end"""
    sigFilterFileNamePatternChanged = qt.Signal(str)
    """Signal emut when the filter pattern change"""

    def __init__(self, parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.setWindowFlags(qt.Qt.Widget)
        self._mainWidget = _MainWidget(parent=self)
        self.setCentralWidget(self.widget)
        # create toolbar
        toolbar = qt.QToolBar("", parent=self)
        toolbar.setIconSize(qt.QSize(32, 32))
        self._controlAction = datareacheractions.ControlAction(parent=self)
        self._configurationAction = datareacheractions.ConfigurationAction(parent=self)
        toolbar.addAction(self._controlAction)
        toolbar.addAction(self._configurationAction)

        self._actionGroup = qt.QActionGroup(self)
        self._actionGroup.addAction(self._controlAction)
        self._actionGroup.addAction(self._configurationAction)

        self.addToolBar(qt.Qt.LeftToolBarArea, toolbar)
        toolbar.setMovable(False)
        # connect signal / slot
        self._controlAction.toggled[bool].connect(
            self._mainWidget.controlWidget.setVisible
        )
        self._configurationAction.toggled[bool].connect(
            self._mainWidget.configWidget.setVisible
        )
        self._controlAction.setChecked(True)

    def getConfiguration(self) -> dict:
        return {
            "start_folder": self.widget.getFolderObserved(),
            "file_filter": self.widget.getLinuxFilePattern(),
            "scan_type_searched": self.widget.getConfigWindow().getScanType().value,
        }

    def setConfiguration(self, config: dict):
        if "start_folder" in config:
            self.widget.setFolderObserved(config["start_folder"])
        if "file_filter" in config:
            self.widget.setLinuxFilePattern(config["file_filter"])
        type_searched = config.get("scan_type_searched", None)
        if type_searched is not None:
            self.widget.getConfigWindow().setScanType(type_searched)

    @property
    def widget(self) -> qt.QWidget:
        return self._mainWidget

# coding: utf-8
from __future__ import annotations


import os
import socket
import logging

from silx.gui import qt

from tomwer.core import settings
from tomwer.core.process.utils import LastReceivedScansDict
from tomwer.core.scan.blissscan import BlissScan
from tomwer.gui import icons as tomwericons
from tomwer.gui.control import datareacheractions as actions
from tomwer.gui.control.history import ScanHistory
from tomwer.gui.control.observations import ScanObservation
from tomwer.gui.utils.inputwidget import (
    HDF5ConfigFileSelector,
    NXTomomillOutputDirSelector,
)
from tomwer.gui.utils.host_editor import HostEditor
from tomwer.synctools.rsyncmanager import BlissSequenceRSyncWorker

from ._host import Host


_logger = logging.getLogger(__name__)


class DataListenerWidget(qt.QMainWindow):
    """
    Widget to display the bliss acquisition on going and finished
    """

    NB_STORED_LAST_FOUND = 20

    sigActivate = qt.Signal()
    """Signal emitted when the listening start"""
    sigDeactivate = qt.Signal()
    """Signal emitted when the listening end"""
    sigConfigurationChanged = qt.Signal()
    """Signal emitted when the configuration for the bliss client is updated"""
    sigAcquisitionEnded = qt.Signal(tuple)
    """Signal emitted when an acquisition is ended without errors.
    Tuple contains (master_file, entry, proposal_file)"""
    sigServerStopped = qt.Signal()
    """Signal emitted when the server is stopped by a sigkill or sigterm"""
    sigCFGFileChanged = qt.Signal(str)
    """Signal emitted when path to the nxtomomill configuration file change"""
    sigMechanicalFlipsChanged = qt.Signal()
    """Signal emitted when the mechanical flips have been changed"""

    def __init__(self, parent=None, host_discovery=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._listener = None
        self.lastFoundScans = LastReceivedScansDict(self.NB_STORED_LAST_FOUND)
        self._blissScans = {}
        # keep a trace of the bliss scans. key is bliss scan strings
        # (used as id), value is BlissScan instance
        self._syncWorkers = {}
        # associate scan path (directory) to the RSyncWorker

        # create widgets
        self._centralWidget = qt.QWidget(parent=self)
        self._centralWidget.setLayout(qt.QVBoxLayout())

        self._controlWidget = DataListenerControl(parent=self)
        """Widget containing the 'control' of the datalistener: start of stop
        the listener"""
        self._centralWidget.layout().addWidget(self._controlWidget)

        self._historyWindow = ScanHistory(parent=self)
        """Widget containing the latest valid scan found by the listener"""
        self._centralWidget.layout().addWidget(self._historyWindow)

        self._configWindow = ConfigurationWidget(
            parent=self, host_discovery=host_discovery
        )
        """Widget containing the configuration to communicate with bliss"""
        self._centralWidget.layout().addWidget(self._configWindow)

        self._observationWidget = ScanObservation(parent=self)
        """Widget containing the current observed directory by the listener"""
        self._centralWidget.layout().addWidget(self._observationWidget)

        # create toolbar
        toolbar = qt.QToolBar("")
        toolbar.setIconSize(qt.QSize(32, 32))

        self._controlAction = actions.ControlAction(parent=self)
        self._observationsAction = actions.ObservationAction(parent=self)
        self._configurationAction = actions.ConfigurationAction(parent=self)
        self._historyAction = actions.HistoryAction(parent=self)
        toolbar.addAction(self._controlAction)
        toolbar.addAction(self._observationsAction)
        toolbar.addAction(self._configurationAction)
        toolbar.addAction(self._historyAction)

        self._actionGroup = qt.QActionGroup(self)
        self._actionGroup.addAction(self._controlAction)
        self._actionGroup.addAction(self._observationsAction)
        self._actionGroup.addAction(self._configurationAction)
        self._actionGroup.addAction(self._historyAction)

        self.addToolBar(qt.Qt.LeftToolBarArea, toolbar)
        toolbar.setMovable(False)

        # signal / slot connection
        self._actionGroup.triggered.connect(self._updateCentralWidget)
        self._controlWidget.sigActivated.connect(self.sigActivate)
        self._controlWidget.sigDeactivated.connect(self.sigDeactivate)
        self._configWindow.sigConfigurationChanged.connect(self.sigConfigurationChanged)
        self._configWindow.sigCFGFileChanged.connect(self.sigCFGFileChanged)
        self._configWindow.sigMechanicalFlipsChanged.connect(
            self.sigMechanicalFlipsChanged
        )
        self._configWindow.sigRestart.connect(self._restartListener)

        # expose api
        self.activate = self._controlWidget.activate
        self.getCFGFilePath = self._configWindow.getCFGFilePath
        self.getOutputFolder = self._configWindow.getOutputFolder

        # set up
        self.setCentralWidget(self._centralWidget)
        self._controlAction.setChecked(True)
        self._updateCentralWidget(self._controlAction)

    def setHostAndPortToolTip(self, tooltip: str):
        self._configWindow._hostQLE.setToolTip(tooltip)
        self._configWindow._hostLabel.setToolTip(tooltip)
        self._configWindow._portLabel.setToolTip(tooltip)
        self._configWindow._portSpinBox.setToolTip(tooltip)

    def _updateCentralWidget(self, action_triggered):
        action_to_widget = {
            self._controlAction: self._controlWidget,
            self._historyAction: self._historyWindow,
            self._observationsAction: self._observationWidget,
            self._configurationAction: self._configWindow,
        }
        for action, widget in action_to_widget.items():
            widget.setVisible(action is action_triggered)

    def _serverStopped(self):
        self.sigServerStopped.emit()

    def _acquisitionStarted(self, arg: tuple):
        master_file, entry, proposal_file, saving_file = arg
        scan = self._getBlissScan(
            master_file=master_file, entry=entry, proposal_file=proposal_file
        )
        if settings.isOnLbsram(scan.path):
            self._attachRSyncWorker(scan.path, proposal_file, saving_file)
        self.addAcquisitionObserve(scan=scan)

    def _acquisitionEnded(self, arg: tuple):
        master_file, entry, proposal_file, saving_file, succeed = arg
        scan = self._getBlissScan(
            master_file=master_file, entry=entry, proposal_file=proposal_file
        )
        self.setAcquisitionEnded(scan=scan, success=succeed)
        if self._hasRSyncWorkerAttach(scan.path):
            self._detachRSyncWorker(scan.path)
        self.sigAcquisitionEnded.emit(
            (master_file, entry, proposal_file, saving_file, succeed)
        )

    def _acquisitionUpdated(self, arg: tuple):
        master_file, entry, proposal_file, saving_file, scan_number = arg
        scan = self._getBlissScan(
            master_file=master_file, entry=entry, proposal_file=proposal_file
        )
        scan.add_scan_number(scan_number)
        if settings.isOnLbsram(scan.path):
            if not self._hasRSyncWorkerAttach(scan.path):
                self._attachRSyncWorker(
                    scan.path, proposal_file=proposal_file, saving_file=saving_file
                )

        self.updateAcquisitionObserve(scan=scan)

    def _getBlissScan(self, master_file, entry, proposal_file):
        scan_id = BlissScan.get_id_name(master_file=master_file, entry=entry)
        if scan_id in self._blissScans:
            return self._blissScans[scan_id]
        else:
            bliss_scan = BlissScan(
                master_file=master_file, entry=entry, proposal_file=proposal_file
            )
            self._blissScans[str(bliss_scan)] = bliss_scan
            return bliss_scan

    def addAcquisitionObserve(self, scan):
        self._observationWidget.addObservation(scan)
        self._observationWidget.update(scan, "on going")

    def setAcquisitionEnded(self, scan, success):
        if success is False:
            self._observationWidget.update(scan, "failed")
        else:
            self._observationWidget.removeObservation(scan)
            self.lastFoundScans.add(scan)
            self._historyWindow.update(list(self.lastFoundScans.items()))

    def updateAcquisitionObserve(self, scan):
        self._observationWidget.update(scan, "on going")

    def sizeHint(self):
        return qt.QSize(600, 400)

    def _restartListener(self, host_name, host_port):
        # At the moment we still pass by the `BEACON_HOST` environment variable
        # Because the interface is still the same for the old data listener and the new one.
        # This is the most straightforward.
        os.environ["BEACON_HOST"] = f"{host_name}:{host_port}"
        self.activate(False)
        self.activate(True)

    def _attachRSyncWorker(self, scan_path, proposal_file, saving_file):
        dest_dir = scan_path.replace(
            settings.get_lbsram_path(), settings.get_dest_path()
        )
        dest_dir = os.path.dirname(dest_dir)
        if proposal_file is not None:
            dest_proposal_file = proposal_file.replace(
                settings.get_lbsram_path(), settings.get_dest_path()
            )
        else:
            dest_proposal_file = None
        if saving_file is not None:
            dest_saving_file = saving_file.replace(
                settings.get_lbsram_path(), settings.get_dest_path()
            )
        else:
            dest_saving_file = None
        worker = BlissSequenceRSyncWorker(
            src_dir=scan_path,
            dst_dir=dest_dir,
            delta_time=1,
            src_proposal_file=proposal_file,
            dst_proposal_file=dest_proposal_file,
            src_sample_file=saving_file,
            dst_sample_file=dest_saving_file,
        )
        self._syncWorkers[scan_path] = worker
        worker.start()

    def _detachRSyncWorker(self, scan_path):
        if self._hasRSyncWorkerAttach(scan_path=scan_path):
            worker = self._syncWorkers[scan_path]
            worker.stop()
            del self._syncWorkers[scan_path]

    def _hasRSyncWorkerAttach(self, scan_path):
        return scan_path in self._syncWorkers

    # expose API
    def getHost(self) -> str:
        """Return server host"""
        return self._configWindow.getHost()

    def getPort(self) -> int:
        """Return server port"""
        return self._configWindow.getPort()

    def getBlissServerConfiguration(self) -> dict:
        return self._configWindow.getConfiguration()

    def setBlissServerConfiguration(self, config):
        self._configWindow.setConfiguration(config=config)

    def setCFGFilePath(self, cfg_file):
        self._configWindow.setCFGFilePath(cfg_file)

    def setOutputFolder(self, output_dir):
        self._configWindow.setOutputFolder(output_dir)

    def setMechanicalFlips(self, left_right_flip: bool, up_down_flip: bool) -> None:
        self._configWindow.setMechanicalFlips(
            left_right_flip=left_right_flip, up_down_flip=up_down_flip
        )

    def getMechanicalFlips(self) -> tuple[bool, bool]:
        return self._configWindow.getMechanicalFlips()


class DataListenerControl(qt.QWidget):
    """Interface to control the activation of the datalistener"""

    sigActivated = qt.Signal()
    """signal emitted when the datalistener is start"""
    sigDeactivated = qt.Signal()
    """signal emitted when the datalistener is stop"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QGridLayout())

        # add left spacer
        lspacer = qt.QWidget(self)
        lspacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(lspacer, 0, 0, 1, 1)

        # add start / stop icon frame
        self._iconLabel = qt.QLabel(parent=self)
        self._iconLabel.setMinimumSize(qt.QSize(55, 55))
        self.layout().addWidget(self._iconLabel, 0, 1, 1, 1)

        # add button
        self._button = qt.QPushButton(self)
        self.layout().addWidget(self._button, 1, 1, 1, 1)

        # add right spacer
        rspacer = qt.QWidget(self)
        rspacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(rspacer, 0, 2, 1, 1)

        # bottom spacer
        bspacer = qt.QWidget(self)
        bspacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(bspacer, 2, 1, 1, 1)

        # set up
        self._updateIconAndText(activate=False)

        # connect signal / slot
        self._button.released.connect(self._buttonCallback)

    def _buttonCallback(self):
        self.activate(not self.isActivate())

    def isActivate(self):
        return self._button.text() == "stop"

    def activate(self, activate=True, *args, **kwargs):
        self._updateIconAndText(activate=activate)
        if activate is True:
            self.sigActivated.emit()
        else:
            self.sigDeactivated.emit()

    def _updateIconAndText(self, activate):
        if activate:
            icon = tomwericons.getQIcon("datalistener_activate")
        else:
            icon = tomwericons.getQIcon("datalistener_deactivate")

        text = "stop" if activate else "start"
        self._button.setText(text)
        self._iconLabel.setPixmap(icon.pixmap(80, 80))


class ConfigurationWidget(qt.QTabWidget):
    """Widget for data listener configuration"""

    sigConfigurationChanged = qt.Signal()
    """Signal emitted when the configuration change"""
    sigCFGFileChanged = qt.Signal(str)

    sigMechanicalFlipsChanged = qt.Signal()
    """Signal emitted when the mechanical flip has been changed"""

    sigRestart = qt.Signal(str, int)
    """Emit when use ask for a restart of the data listener. This can happen when the host / port are changed"""

    DEFAULT_PORT = 25_000

    def __init__(
        self,
        parent=None,
        host_discovery: str | None = None,
        enable_host_pinging: bool = True,
    ):
        """
        :param host_discovery: define a policy regarding host discovery when creating the widget. If None no discovery will be made.
            If 'BEACON_HOST' given then will try to discover the host name and port using the environment variable BEACON_HOST.
        """

        super().__init__(parent)

        # host tab
        self._hostWidget = qt.QDialog()
        self._hostWidget.setLayout(qt.QGridLayout())

        self._currentHost = self._getHost(host_discovery)
        """
        Current address listen by bliss data. As host, port.
        setPort and setHost will update this value.
        Else it will be updated when users are asking for a restart of the bliss-data listener.
        Used to handle the '_restartButton' and '_resetButton'
        """
        # host
        self._hostLabel = qt.QLabel("host name", self)
        self._hostWidget.layout().addWidget(self._hostLabel, 0, 0, 1, 1)
        self._hostQLE = HostEditor(
            parent=self,
            name=self._currentHost.name,
            port=self._currentHost.port,
            enable_host_pinging=enable_host_pinging,
        )
        self._hostQLE.setEnabled(self._hostEditable)
        self._hostWidget.layout().addWidget(self._hostQLE, 0, 1, 1, 2)

        # port
        self._portLabel = qt.QLabel("host port", self)
        self._hostWidget.layout().addWidget(self._portLabel, 1, 0, 1, 1)
        self._portSpinBox = qt.QSpinBox(self)
        self._portSpinBox.setRange(0, 100000)
        self._portSpinBox.setValue(self._currentHost.port)
        self._portSpinBox.setEnabled(self._hostEditable)
        self._hostWidget.layout().addWidget(self._portSpinBox, 1, 1, 1, 2)

        # restart & reset buttons
        self._buttons = qt.QDialogButtonBox(parent=self)
        style = qt.QApplication.style()
        icon = style.standardIcon(qt.QStyle.SP_MediaPlay)
        self._restartButton = qt.QPushButton(icon, "restart bliss-data listener")
        self._buttons.addButton(self._restartButton, qt.QDialogButtonBox.ActionRole)

        icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self._resetButton = qt.QPushButton(icon, "reset host")
        self._buttons.addButton(self._resetButton, qt.QDialogButtonBox.ActionRole)

        self._hostWidget.layout().addWidget(self._buttons, 2, 2, 1, 2)

        # spacer
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._hostWidget.layout().addWidget(spacer, 90, 0, 1, 1)

        # h52nx tab
        self._h52nxConfigWidget = qt.QWidget()
        self._h52nxConfigWidget.setLayout(qt.QGridLayout())

        # configuration file to use
        self._cfgLabel = qt.QLabel("config file")
        self._h52nxConfigWidget.layout().addWidget(self._cfgLabel, 11, 0, 1, 1)
        self._cfgWidget = HDF5ConfigFileSelector(self)
        self._cfgWidget.setContentsMargins(0, 0, 0, 0)
        self._cfgWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._h52nxConfigWidget.layout().addWidget(self._cfgWidget, 11, 1, 1, 2)
        tooltip = (
            "You can provide a configuration file to tune conversion "
            "done by nxtomomill. If None is provided then the default "
            "parameters will be used."
        )
        self._cfgLabel.setToolTip(tooltip)
        self._cfgWidget.setToolTip(tooltip)

        # mechanical flip
        self._lrMechanicalFlipLabel = qt.QLabel("left-right mechanical flip")
        lr_icon = tomwericons.getQIcon("lr_mirroring")
        self._h52nxConfigWidget.layout().addWidget(
            self._lrMechanicalFlipLabel, 12, 0, 1, 1
        )
        self._lrMechanicalFlip = qt.QCheckBox()
        self._lrMechanicalFlip.setIcon(lr_icon)
        self._lrMechanicalFlip.setToolTip(
            "Detector image is flipped **left-right** for mechanical reasons that are not propagated with bliss-tomo hdf5 metadata (mirror,..)."
        )
        self._h52nxConfigWidget.layout().addWidget(self._lrMechanicalFlip, 12, 1, 1, 2)

        self._udMechanicalFlipLabel = qt.QLabel("up-down mechanical flip")
        ud_icon = tomwericons.getQIcon("ud_mirroring")
        self._h52nxConfigWidget.layout().addWidget(
            self._udMechanicalFlipLabel, 13, 0, 1, 1
        )
        self._udMechanicalFlip = qt.QCheckBox()
        self._udMechanicalFlip.setIcon(ud_icon)
        self._udMechanicalFlip.setToolTip(
            "Detector image is flipped **up-down** for mechanical reasons that are not propagated with bliss-tomo hdf5 metadata (mirror,..)."
        )
        self._h52nxConfigWidget.layout().addWidget(self._udMechanicalFlip, 13, 1, 1, 2)

        # vline 2
        self._vLine2 = qt.QFrame()
        self._vLine2.setFrameShape(qt.QFrame.Shape.HLine)
        self._vLine2.setFrameShadow(qt.QFrame.Shadow.Sunken)
        self._h52nxConfigWidget.layout().addWidget(self._vLine2, 20, 0, 1, 3)

        # output folder
        self._outputFolderLabel = qt.QLabel("nexus file output dir")
        self._h52nxConfigWidget.layout().addWidget(self._outputFolderLabel, 21, 0, 1, 1)
        self._nxTomomillOutputWidget = NXTomomillOutputDirSelector(self)
        self._nxTomomillOutputWidget.setContentsMargins(0, 0, 0, 0)
        self._nxTomomillOutputWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._h52nxConfigWidget.layout().addWidget(
            self._nxTomomillOutputWidget, 21, 1, 1, 2
        )

        # buttons
        types = qt.QDialogButtonBox.Apply
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self._buttons.button(qt.QDialogButtonBox.Apply).setToolTip(
            "Once apply if a listening is on going"
            "then it will stop the current listening and"
            "restart it with the new parameters"
        )
        self._h52nxConfigWidget.layout().addWidget(self._buttons, 21, 0, 1, 3)

        # height spacer
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._h52nxConfigWidget.layout().addWidget(spacer, 90, 0, 1, 1)

        # connect signal / slot
        self._cfgWidget.sigConfigFileChanged.connect(self.sigCFGFileChanged)
        self._buttons.button(qt.QDialogButtonBox.Apply).clicked.connect(self.validate)
        self._nxTomomillOutputWidget.sigChanged.connect(self.validate)
        self._lrMechanicalFlip.toggled.connect(self.sigMechanicalFlipsChanged)
        self._udMechanicalFlip.toggled.connect(self.sigMechanicalFlipsChanged)
        self._portSpinBox.valueChanged.connect(self._updateRestartAndResetAvailability)
        self._portSpinBox.editingFinished.connect(self._portHasChanged)
        self._hostQLE.currentTextChanged.connect(
            self._updateRestartAndResetAvailability
        )
        self._restartButton.released.connect(self._restartBlissData)
        self._resetButton.released.connect(self._resetHostAndPortValues)

        # set up
        self._buttons.hide()

        # update host name and port in case one was none at start up.
        self._currentHost.name = self.getHost()
        self._currentHost.port = self.getPort()
        self._updateRestartAndResetAvailability()

        self.addTab(self._hostWidget, "host")
        self.addTab(self._h52nxConfigWidget, "h52nx")

    def _getHost(self, host_discovery) -> Host:
        if settings.JSON_RPC_HOST is not None:
            # use case settings.JSON_RPC_HOST is defined
            # if defined in the settings file take it
            self._hostEditable = False
            return Host(settings.JSON_RPC_HOST, settings.JSON_RPC_PORT)

        if host_discovery is None:
            # use case settings.JSON_RPC_HOST is not defined but 'host_discovery' is None (requires JSON-RPC)
            self._hostEditable = False
            return Host(
                socket.gethostname(),
                settings.JSON_RPC_PORT,
            )

        # default use case - using bliss-data and BEACON_HOST
        self._hostEditable = True
        err_beacon_host = "Unable to determine host name and host port from 'BEACON_HOST'. Please export it as host_name:host_port. For example 'export BEACON_HOST=icc:0000'"
        beacon_host = os.environ.get("BEACON_HOST")
        if beacon_host is None:
            _logger.warning(err_beacon_host)
            return Host(None, self.DEFAULT_PORT)
        try:
            host_name, host_port = beacon_host.split(":")
            try:
                host_port = int(host_port)
            except ValueError:
                host_port = self.DEFAULT_PORT
        except ValueError:
            _logger.error(err_beacon_host)
            return Host(None, self.DEFAULT_PORT)
        else:
            return Host(host_name, host_port)

    def _restartBlissData(self):
        self._currentHost.name = self.getHost()
        self._currentHost.port = self.getPort()
        self.sigRestart.emit(self._currentHost.name, self._currentHost.port)
        self._updateRestartAndResetAvailability()

    def _resetHostAndPortValues(self):
        self.setHost(self._currentHost.name)
        self.setPort(self._currentHost.port)

    def _updateRestartAndResetAvailability(self):
        host_name_or_port_has_changed = (
            self._currentHost.name != self.getHost()
            or self._currentHost.port != self.getPort()
        )
        self._resetButton.setEnabled(host_name_or_port_has_changed)
        self._restartButton.setEnabled(host_name_or_port_has_changed)

    def _portHasChanged(self):
        # update port to the host (so it can update the icons). This requires a bit of processing so
        # we do this when edition is finished only.
        self._hostQLE.setPort(self.getPort())

    def getCFGFilePath(self):
        return self._cfgWidget.getCFGFilePath()

    def setCFGFilePath(self, cfg_file):
        self._cfgWidget.setCFGFilePath(cfg_file)

    def getOutputFolder(self):
        return self._nxTomomillOutputWidget.getOutputFolder()

    def setOutputFolder(self, output_dir):
        self._nxTomomillOutputWidget.setOutputFolder(output_dir)

    def addBlissSession(self, session: str) -> None:
        if self._blissSession.findText(session) >= 0:
            return
        else:
            self._blissSession.addItem(session)

    def getConfiguration(self) -> dict:
        return {"host": self.getHost(), "port": self.getPort()}

    def setConfiguration(self, config: dict):
        if "host" in config:
            self.setHost(config["host"])
        if "port" in config:
            self.setPort(config["port"])

    def getHost(self) -> str:
        return self._hostQLE.currentText()

    def setHost(self, name: str):
        self._hostQLE.setCurrentText(name)
        self._currentHost.name = name

    def getPort(self) -> int:
        return self._portSpinBox.value()

    def setPort(self, port: int) -> None:
        assert isinstance(port, int)
        self._portSpinBox.setValue(port)
        self._currentHost.port = port

    def getMechanicalFlips(self) -> tuple[bool, bool]:
        """
        :return: left-right flip, up-down flip
        """
        return self._lrMechanicalFlip.isChecked(), self._udMechanicalFlip.isChecked()

    def setMechanicalFlips(self, left_right_flip: bool, up_down_flip: bool) -> None:
        self._lrMechanicalFlip.setChecked(left_right_flip)
        self._udMechanicalFlip.setChecked(up_down_flip)

    def validate(self):
        self.sigConfigurationChanged.emit()

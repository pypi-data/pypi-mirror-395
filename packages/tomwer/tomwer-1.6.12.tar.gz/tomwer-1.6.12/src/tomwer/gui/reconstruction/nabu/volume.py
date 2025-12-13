# coding: utf-8
from __future__ import annotations

from asyncio.log import logger

from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuStages,
)
from tomwer.core.utils.dictutils import concatenate_dict
from tomwer.gui import icons
from tomwer.gui.configuration.action import (
    BasicConfigurationAction,
    ExpertConfigurationAction,
    MinimalisticConfigurationAction,
)
from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.gui.reconstruction.nabu.nabuconfig.output import (
    NabuOutputLocationWidget,
    QNabuFileFormatComboBox,
)
from tomwer.gui.reconstruction.nabu.platform import NabuPlatformSettings
from tomwer.gui.settings import (
    TAB_LABEL_RECONSTRUCTION_SETTINGS,
    TAB_LABEL_PLATFORM_SETTINGS,
)


class SliceSelector(qt.QWidget):
    """
    Widget to select a value for defining a ROI to reconstruction (start or
    end)
    """

    valueChanged = qt.Signal()
    """emit when the slice value change"""

    def __init__(
        self, label, auto_alias, is_end, grid_layout, index_layout, parent=None
    ):
        qt.QWidget.__init__(self, parent=parent)
        self._label = qt.QLabel(label, parent=self)
        grid_layout.addWidget(self._label, index_layout, 0, 1, 1)
        self._qcb = qt.QCheckBox(auto_alias)
        grid_layout.addWidget(self._qcb, index_layout, 1, 1, 1)
        grid_layout.addWidget(qt.QLabel("or", self), index_layout, 2, 1, 1)
        self._qle = qt.QLineEdit("0", self)
        self._validator = qt.QIntValidator()
        self._qle.setValidator(self._validator)
        grid_layout.addWidget(self._qle, index_layout, 3, 1, 1)
        self._is_end = is_end
        if is_end is True:
            self._qle.setToolTip("-1 will be the last slice")
            self._validator.setBottom(-1)
        else:
            self._validator.setBottom(0)

        # set up
        self._qcb.setChecked(True)
        self._qle.setEnabled(False)
        if is_end:
            self._qle.setText("-1")

        # connect signal / slot
        self._qcb.toggled.connect(self._qle.setDisabled)
        self._qcb.toggled.connect(self._triggerValueChanged)
        self._qle.editingFinished.connect(self._triggerValueChanged)

    def _triggerValueChanged(self, *args, **kwargs):
        self.valueChanged.emit()

    def setMaximum(self, maximum):
        self._validator.setTop(maximum)

    def value(self):
        if self._qcb.isChecked():
            return -1 if self._is_end else 0
        else:
            return int(self._qle.text())

    def setValue(self, value):
        self._qle.setText(str(value))
        if self._is_end:
            self._qcb.setChecked(value == -1)
        else:
            self._qcb.setChecked(value == 0)


class NabuVolumeWidget(_NabuStageConfigBase, qt.QWidget):
    """
    Widget dedicated to manage the volume reconstruction from nabu
    """

    sigConfigChanged = qt.Signal()
    """Signal emitted when the configuration change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent=parent)
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.VOLUME)
        self.setLayout(qt.QGridLayout())

        # warning about requires parameters from a nabu slice reconstruction
        self._warning_widget = qt.QWidget(parent=self)
        self._warning_widget.setLayout(qt.QHBoxLayout())
        self._warningIconL = qt.QLabel("", parent=self)
        self._warningIconL.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self._warningIconL.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self._warningIconR = qt.QLabel("", parent=self)
        self._warningIconR.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self._warningIconR.setAlignment(qt.Qt.AlignLeft | qt.Qt.AlignVCenter)
        warning_icon = icons.getQIcon("warning")
        self._warningIconL.setPixmap(warning_icon.pixmap(20, 20))
        self._warningIconR.setPixmap(warning_icon.pixmap(20, 20))
        self._warning_widget.layout().addWidget(self._warningIconL)

        self._labelWarning = qt.QLabel(
            "Requires parameters from nabu slice reconstruction.", parent=self
        )
        self._labelWarning.setToolTip(
            'This mean that a "nabu slice '
            'reconstruction" widget should exist upstream'
        )
        self._warning_widget.layout().addWidget(self._labelWarning)
        self._warning_widget.layout().addWidget(self._warningIconR)
        self.layout().addWidget(self._warning_widget, 0, 0, 1, 2)

        # volume from and to option
        self._groupBox = qt.QGroupBox("volume to reconstruct", parent=self)
        self._groupBox.setLayout(qt.QGridLayout())
        self.layout().addWidget(self._groupBox, 2, 0, 1, 2)

        self._fromSlice = SliceSelector(
            label="from slice",
            auto_alias="start",
            is_end=False,
            parent=self,
            grid_layout=self._groupBox.layout(),
            index_layout=0,
        )
        self._groupBox.layout().addWidget(self._fromSlice)
        self.registerWidget(self._groupBox, "required")

        self._toSlice = SliceSelector(
            label="to slice",
            auto_alias="end",
            is_end=True,
            parent=self,
            grid_layout=self._groupBox.layout(),
            index_layout=1,
        )
        self._groupBox.layout().addWidget(self._toSlice)

        # option to compute histogram
        self._histogramCB = qt.QCheckBox("compute volume histogram of values", self)
        self.layout().addWidget(self._histogramCB, 3, 0, 1, 2)
        self.registerWidget(self._histogramCB, "required")

        # output format can be redefined
        self._redefineNabuFileFormat = qt.QGroupBox(
            "change received file format from 'nabu slice'", self
        )
        self._redefineNabuFileFormat.setCheckable(True)
        self._redefineNabuFileFormat.setLayout(qt.QVBoxLayout())
        self._fileFormatCB = QNabuFileFormatComboBox(self._redefineNabuFileFormat)
        self._redefineNabuFileFormat.layout().addWidget(self._fileFormatCB)
        self.layout().addWidget(self._redefineNabuFileFormat, 4, 0, 1, 2)
        self.registerWidget(self._fileFormatCB, "advanced")
        self.registerWidget(self._redefineNabuFileFormat, "advanced")

        # redefine output location
        self._redefineNabuOutputLocation = qt.QGroupBox(
            "change received reconstruction output location from 'nabu slice'", self
        )
        self._redefineNabuOutputLocation.setCheckable(True)
        self._redefineNabuOutputLocation.setLayout(qt.QVBoxLayout())
        self._outputLocationWidget = NabuOutputLocationWidget(parent=self)
        self._redefineNabuOutputLocation.layout().addWidget(self._outputLocationWidget)
        self.layout().addWidget(self._redefineNabuOutputLocation, 5, 0, 1, 2)
        self.registerWidget(self._redefineNabuOutputLocation, "advanced")
        self.registerWidget(self._outputLocationWidget, "advanced")

        # opt use phase Paganin
        self._usePhaseQCB = qt.QCheckBox("Use phase Paganin")
        self.layout().addWidget(self._usePhaseQCB, 52, 0, 1, 2)
        self.registerWidget(self._usePhaseQCB, "advanced")
        self._usePhaseQCB.setToolTip(
            "Whether to use a margin when " "performing phase retrieval."
        )

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 99, 0, 1, 1)

        # set up
        self._histogramCB.setChecked(True)
        self._usePhaseQCB.setChecked(True)
        self._redefineNabuFileFormat.setChecked(False)
        self._redefineNabuOutputLocation.setChecked(False)
        self.setConfigurationLevel("required")

        # connect signal / slot
        self._fromSlice.valueChanged.connect(self._triggerSigConfChanged)
        self._toSlice.valueChanged.connect(self._triggerSigConfChanged)
        self._usePhaseQCB.toggled.connect(self._triggerSigConfChanged)
        self._outputLocationWidget._outputDirQLE.editingFinished.connect(
            self._triggerSigConfChanged
        )
        self._outputLocationWidget.sigOutputChanged.connect(self._triggerSigConfChanged)
        self._redefineNabuOutputLocation.toggled.connect(self._triggerSigConfChanged)

    def redefineOutputLocation(self):
        return self._redefineNabuOutputLocation.isChecked()

    def setRedefineOutputLocation(self, redefine: bool):
        self._redefineNabuOutputLocation.setChecked(redefine)

    def getNabuOutputLocation(self):
        if self.redefineOutputLocation():
            return self._outputLocationWidget.getOutputDir()
        else:
            return None

    def setNabuOutputLocation(self, location: str | None):
        if location is None:
            self._redefineNabuOutputLocation.setChecked(False)
        else:
            self._redefineNabuOutputLocation.setChecked(True)
            self._outputLocationWidget.setOutputDirMode("other")
            self._outputLocationWidget.setOutputDir(location)

    def redefineNabuFileFormat(self):
        return self._redefineNabuFileFormat.isChecked()

    def getNabuFileFormat(self):
        if self.redefineNabuFileFormat():
            return self._fileFormatCB.currentText()
        else:
            return None

    def setNabuFileFormat(self, file_format: str | None):
        if file_format is None:
            self._redefineNabuFileFormat.setChecked(False)
        else:
            assert isinstance(file_format, str)
            self._redefineNabuFileFormat.setChecked(True)
            idx = self._fileFormatCB.findText(file_format)
            if idx < 0:
                logger.error(f"unable to find file format {file_format}")
            else:
                self._fileFormatCB.setCurrentIndex(idx)

    def _triggerSigConfChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getStartZ(self):
        return self._fromSlice.value()

    def setStartZ(self, value):
        self._fromSlice.setValue(value)

    def getEndZ(self):
        return self._toSlice.value()

    def setEndZ(self, value):
        self._toSlice.setValue(value)

    def phasePaganinRequested(self):
        return self._usePhaseQCB.isChecked()

    def setPhasePaganinRequested(self, checked):
        self._usePhaseQCB.setChecked(checked)

    def setScan(self, scan):
        if len(scan.projections) > 0:
            self._fromSlice.setMaximum(len(scan.projections))
        else:
            self._fromSlice.setMaximum(999999999)

    def isHistogramRequested(self):
        return self._histogramCB.isChecked()

    def setHistogramRequested(self, requested):
        self._histogramCB.setChecked(requested)

    def getConfiguration(self):
        return {
            "start_z": self.getStartZ(),
            "end_z": self.getEndZ(),
            "use_phase_margin": self.phasePaganinRequested(),
            "postproc": {
                "output_histogram": int(self.isHistogramRequested()),
            },
            "new_output_file_format": self.getNabuFileFormat() or "",
            "new_output_location": self.getNabuOutputLocation() or "",
            "output_dir_mode": self._outputLocationWidget.getOutputDirMode().value,
            "overwrite_output_location": self.redefineOutputLocation(),
        }

    def setConfiguration(self, config):
        if "start_z" in config:
            self.setStartZ(config["start_z"])
        if "end_z" in config:
            self.setEndZ(config["end_z"])
        if "use_phase_margin" in config:
            self.setPhasePaganinRequested(config["use_phase_margin"])
        if "postproc" in config:
            self.setPostProcConfiguration(config["postproc"])
        if "new_output_file_format" in config:
            new_output_file_format = config["new_output_file_format"]
            if new_output_file_format == "":
                new_output_file_format = None
            self.setNabuFileFormat(new_output_file_format)
        if "new_output_location" in config:
            new_output_location = config["new_output_location"]
            if new_output_location == "":
                new_output_location = None
            self.setNabuOutputLocation(new_output_location)
        output_dir_mode = config.get("output_dir_mode", None)
        if output_dir_mode is not None:
            self._outputLocationWidget.setOutputDirMode(output_dir_mode)
        overwrite_output_location = config.get("overwrite_output_location", None)
        if overwrite_output_location is not None:
            self.setRedefineOutputLocation(overwrite_output_location)

    def setPostProcConfiguration(self, config):
        if "output_histogram" in config:
            self.setHistogramRequested(requested=bool(config["output_histogram"]))

    def setConfigurationLevel(self, level):
        level = ConfigurationLevel(level)
        _NabuStageConfigBase.setConfigurationLevel(self, level)

    def getConfigurationLevel(self):
        return self._configuration_level


class NabuVolumeTabWidget(qt.QTabWidget):
    """
    Widget that integrate the reconstruction settings and the platform (local) settings
    """

    sigConfigChanged = qt.Signal()

    def __init__(self, parent: qt.QWidget | None = ...) -> None:
        super().__init__(parent)
        self._configurationLevel = ConfigurationLevel.OPTIONAL
        self._nabuSettingsWidget = NabuVolumeWidget(parent=self)
        self.addTab(self._nabuSettingsWidget, TAB_LABEL_RECONSTRUCTION_SETTINGS)

        self._platformSettingsWidget = NabuPlatformSettings(parent=self)
        self.addTab(self._platformSettingsWidget, TAB_LABEL_PLATFORM_SETTINGS)

        # connect signal / slot
        self._nabuSettingsWidget.sigConfigChanged.connect(self.sigConfigChanged)
        self._platformSettingsWidget.sigConfigChanged.connect(self.sigConfigChanged)

    def getConfiguration(self) -> dict:
        return concatenate_dict(
            self._nabuSettingsWidget.getConfiguration(),
            self._platformSettingsWidget.getConfiguration(),
        )

    def setConfiguration(self, config: dict) -> None:
        self._nabuSettingsWidget.setConfiguration(config=config)
        self._platformSettingsWidget.setConfiguration(config=config)

    def setConfigurationLevel(self, level):
        self._configurationLevel = ConfigurationLevel(level)
        self._nabuSettingsWidget.setConfigurationLevel(level=self._configurationLevel)
        self._platformSettingsWidget.setConfigurationLevel(
            level=self._configurationLevel
        )

    def getConfigurationLevel(self):
        return self._configuration_level


class NabuVolumeWindow(qt.QMainWindow):
    """
    Widget to define settings for a volume reconstruction
    """

    sigConfigChanged = qt.Signal()
    """Signal emitted when configuration change"""

    def __init__(self, parent):
        qt.QMainWindow.__init__(self, parent=parent)

        self.setWindowFlags(qt.Qt.Widget)

        self._mainWidget = NabuVolumeTabWidget(parent=self)
        self.setCentralWidget(self._mainWidget)

        # add toolbar
        toolbar = qt.QToolBar(self)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        # add configuration mode
        self.__configurationModesAction = qt.QAction(self)
        self.__configurationModesAction.setCheckable(False)
        menu = qt.QMenu(self)
        self.__configurationModesAction.setMenu(menu)
        toolbar.addAction(self.__configurationModesAction)

        self.__configurationModesGroup = qt.QActionGroup(self)
        self.__configurationModesGroup.setExclusive(True)
        self.__configurationModesGroup.triggered.connect(self._userModeChanged)

        self._minimalisticAction = MinimalisticConfigurationAction(toolbar)
        menu.addAction(self._minimalisticAction)
        self.__configurationModesGroup.addAction(self._minimalisticAction)
        self._basicConfigAction = BasicConfigurationAction(toolbar)
        menu.addAction(self._basicConfigAction)
        self.__configurationModesGroup.addAction(self._basicConfigAction)
        self._expertConfiguration = ExpertConfigurationAction(toolbar)
        menu.addAction(self._expertConfiguration)
        self.__configurationModesGroup.addAction(self._expertConfiguration)

        # set up
        self._userModeChanged(action=self._basicConfigAction)
        self._basicConfigAction.setChecked(True)

        # connect signal / slot
        self._mainWidget.sigConfigChanged.connect(self._triggerSigConfigChanged)

    def _triggerSigConfigChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def _userModeChanged(self, action):
        self.__configurationModesAction.setIcon(action.icon())
        self.__configurationModesAction.setToolTip(action.tooltip())
        if action is self._basicConfigAction:
            level = ConfigurationLevel.OPTIONAL
        elif action is self._expertConfiguration:
            level = ConfigurationLevel.ADVANCED
        else:
            level = ConfigurationLevel.REQUIRED
        self._mainWidget.setConfigurationLevel(level)

    # expose API
    def getConfigurationLevel(self):
        self._mainWidget.getConfigurationLevel()

    def setConfigurationLevel(self, level):
        self._mainWidget.setConfigurationLevel(level=level)

    def getConfiguration(self):
        return self._mainWidget.getConfiguration()

    def setConfiguration(self, config):
        return self._mainWidget.setConfiguration(config=config)

    def setScan(self, scan):
        return self._mainWidget.setScan(scan=scan)

from __future__ import annotations

import os
from nabu.pipeline.config import parse_nabu_config_file
from tomwer.gui.configuration.action import (
    BasicConfigurationAction,
    ExpertConfigurationAction,
    MinimalisticConfigurationAction,
)
from silx.gui import qt
from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)
from tomwer.gui.reconstruction.nabu.slices import NabuWidget
from tomwer.gui.configuration.level import ConfigurationLevel


class NabuWidgetWithToolbar(qt.QMainWindow):
    sigConfigChanged = qt.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(qt.Qt.Widget)

        self._nabuSettings = NabuWidget(parent=self)
        self.setCentralWidget(self._nabuSettings)

        self._createNabuSettingsToolbar()
        # connect signal / slot
        self._nabuSettings.sigConfigChanged.connect(self.sigConfigChanged)

    def _createNabuSettingsToolbar(self):
        style = qt.QApplication.style()

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

        # reset configuration option
        self.__resetAction = qt.QAction(self)
        self.__resetAction.setToolTip("reset nabu configuration")
        reset_icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self.__resetAction.setIcon(reset_icon)
        toolbar.addAction(self.__resetAction)
        self.__resetAction.triggered.connect(self._resetParameters)

        # toolbar spacer
        self.__tSpacer = qt.QWidget(toolbar)
        self.__tSpacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Preferred)
        toolbar.addWidget(self.__tSpacer)

        # connect signal / slot
        self._nabuSettings.sigConfigChanged.connect(self.sigConfigChanged)

        # set up
        self._resetParameters()
        self._basicConfigAction.setChecked(True)
        self._userModeChanged()

    def _resetParameters(self):
        # reset nabu settings
        default_config = get_default_nabu_config(nabu_fullfield_default_config)
        self._nabuSettings._configuration._preProcessingWidget._sinoRingsOpts.resetConfiguration()
        default_config["tomwer_slices"] = "middle"
        default_config["preproc"]["ccd_filter_enabled"] = False
        default_config["preproc"]["double_flatfield"] = False
        default_config["preproc"]["flatfield"] = True
        default_config["preproc"]["take_logarithm"] = True
        self._nabuSettings.setConfiguration(default_config)

    def _userModeChanged(self, *args, **kwargs):
        selectedAction = self.__configurationModesGroup.checkedAction()
        self.__configurationModesAction.setIcon(selectedAction.icon())
        self.__configurationModesAction.setToolTip(selectedAction.tooltip())
        self._nabuSettings.setConfigurationLevel(self.getConfigurationLevel())
        self.sigConfigChanged.emit()

    def _loadParameters(self):
        inputFile = self.askForNabuconfigFile(acceptMode=qt.QFileDialog.AcceptOpen)

        if inputFile and os.path.exists(inputFile):
            config = parse_nabu_config_file(inputFile)
            self._nabuSettings.setConfiguration(config)

    def setConfigurationLevel(self, level):
        level = ConfigurationLevel(level)
        if level == ConfigurationLevel.REQUIRED:
            self._minimalisticAction.setChecked(True)
        elif level == ConfigurationLevel.ADVANCED:
            self._expertConfiguration.setChecked(True)
        elif level == ConfigurationLevel.OPTIONAL:
            self._basicConfigAction.setChecked(True)
        else:
            raise ValueError("Level not recognize")
        self._userModeChanged()

    def getConfigurationLevel(self):
        if self._basicConfigAction.isChecked():
            return ConfigurationLevel.OPTIONAL
        elif self._expertConfiguration.isChecked():
            return ConfigurationLevel.ADVANCED
        elif self._minimalisticAction.isChecked():
            return ConfigurationLevel.REQUIRED
        else:
            raise ValueError("Level not recognize")

    # expose API
    def hideSlicesInterface(self):
        return self._nabuSettings.hideSlicesInterface()

    def hidePaganinInterface(self):
        return self._nabuSettings.hidePaganinInterface()

    def setConfiguration(self, *args, **kwargs):
        self._nabuSettings.setConfiguration(*args, **kwargs)

    def getConfiguration(self):
        return self._nabuSettings.getConfiguration()

    def getMode(self):
        return self._nabuSettings.getMode()

    def setMode(self, *args, **kwargs):
        self._nabuSettings.setMode(*args, **kwargs)

    def setScan(self, scan):
        self._nabuSettings.setScan(scan=scan)

from __future__ import annotations

from silx.gui import qt
from tomwer.gui.configuration.action import (
    ExpertConfigurationAction,
    BasicConfigurationAction,
)
from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.core.scan.scanbase import TomwerScanBase

try:
    from ewoksnotify.gui.icat import PublishProcessedDataWidget
except ImportError:
    has_ewoksnotify = False
else:
    has_ewoksnotify = True


class PublishProcessedDataWindow(qt.QMainWindow):
    def __init__(self, parent: qt.QWidget | None, beamlines: tuple) -> None:
        super().__init__(parent)
        if not has_ewoksnotify:
            raise RuntimeError(
                f"ewoksnotify not installed. Please  install it to instantiate {PublishProcessedDataWindow}"
            )

        # define toolbar
        toolbar = qt.QToolBar(self)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        self.__configurationModesAction = qt.QAction(self)
        self.__configurationModesAction.setCheckable(False)
        menu = qt.QMenu(self)
        self.__configurationModesAction.setMenu(menu)
        toolbar.addAction(self.__configurationModesAction)

        self.__configurationModesGroup = qt.QActionGroup(self)
        self.__configurationModesGroup.setExclusive(True)

        self._basicConfigAction = BasicConfigurationAction(toolbar)
        menu.addAction(self._basicConfigAction)
        self.__configurationModesGroup.addAction(self._basicConfigAction)
        self._expertConfiguration = ExpertConfigurationAction(toolbar)
        menu.addAction(self._expertConfiguration)
        self.__configurationModesGroup.addAction(self._expertConfiguration)

        # define widget
        self._centralWidget = PublishProcessedDataWidget(
            parent=parent,
            beamlines=beamlines,
        )
        # hide the dataset field has defined automatically by tomwer
        self._centralWidget._datasetPLB.setDisabled(True)
        self._centralWidget._datasetQLE.setDisabled(True)
        self._centralWidget._datasetQLE.setToolTip("This field is imposed by tomwer")
        self.setCentralWidget(self._centralWidget)

        # connect signal / slot
        self.__configurationModesGroup.triggered.connect(self._userModeChanged)

        # set up
        # for the time beeing let's hide the toolbar and use the 'expert configuration'
        toolbar.hide()
        self._expertConfiguration.trigger()

    def _userModeChanged(self, action):
        self.__configurationModesAction.setIcon(action.icon())
        self.__configurationModesAction.setToolTip(action.tooltip())
        if action is self._basicConfigAction:
            level = ConfigurationLevel.OPTIONAL
        elif action is self._expertConfiguration:
            level = ConfigurationLevel.ADVANCED
        else:
            raise NotImplementedError
        self.centralWidget().setVisible(ConfigurationLevel.ADVANCED <= level)

    # expose API
    def getConfiguration(self) -> dict:
        return self._centralWidget.getConfiguration()

    def setConfiguration(self, configuration: dict) -> None:
        self._centralWidget.setConfiguration(configuration=configuration)

    def setScan(self, scan: TomwerScanBase):
        if not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"scan is expected to be an instance of {TomwerScanBase}, {type(scan)} provided instead"
            )

        new_config = {}
        if not self._centralWidget._proposalPLB.isChecked():
            new_config["proposal"] = scan.get_proposal_name()
        if not self._centralWidget._beamlinePLB.isChecked():
            new_config["beamline"] = scan.instrument_name

        self.setConfiguration(new_config)

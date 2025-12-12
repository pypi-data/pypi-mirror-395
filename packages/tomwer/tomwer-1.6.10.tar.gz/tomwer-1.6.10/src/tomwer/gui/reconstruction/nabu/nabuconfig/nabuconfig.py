# coding: utf-8
from __future__ import annotations


from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from tomwer.gui.reconstruction.nabu.nabuconfig.output import _NabuOutputConfig
from tomwer.gui.reconstruction.nabu.nabuconfig.phase import _NabuPhaseConfig
from tomwer.gui.reconstruction.nabu.nabuconfig.preprocessing import (
    _NabuPreProcessingConfig,
)
from tomwer.gui.reconstruction.nabu.nabuconfig.reconstruction import (
    _NabuReconstructionConfig,
)


class NabuConfiguration(qt.QWidget):
    """
    Top level widget for defining the nabu configuration
    """

    sigConfChanged = qt.Signal(str, str)
    """Signal emitted when the configuration change. Parameters are
    (stage, index option modified)
    """

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent)
        self._stageHided = []
        # list of hided stage. Not taking into account the filter

        self.setLayout(qt.QVBoxLayout())

        # pre processing options
        self._preProcessingGB = qt.QGroupBox("pre processing", self)
        self._preProcessingGB.setLayout(qt.QVBoxLayout())

        self._preProcessingWidget = _NabuPreProcessingConfig(parent=self)
        self._preProcessingGB.layout().addWidget(self._preProcessingWidget)
        self.layout().addWidget(self._preProcessingGB)

        # phase options
        self._phaseGB = qt.QGroupBox("phase", self)
        self._phaseGB.setLayout(qt.QVBoxLayout())

        self._phaseWidget = _NabuPhaseConfig(parent=self)
        self._phaseGB.layout().addWidget(self._phaseWidget)
        self.layout().addWidget(self._phaseGB)

        # reconstruction opts
        self._reconstructionGB = qt.QGroupBox("reconstruction", self)
        self._reconstructionGB.setLayout(qt.QVBoxLayout())

        self._reconstructionWidget = _NabuReconstructionConfig(parent=self)
        self._reconstructionGB.layout().addWidget(self._reconstructionWidget)
        self.layout().addWidget(self._reconstructionGB)

        # output information
        self._outputGB = qt.QGroupBox("output", self)
        self._outputGB.setLayout(qt.QVBoxLayout())

        self._outputWidget = _NabuOutputConfig(parent=self)
        self._outputGB.layout().addWidget(self._outputWidget)
        self.layout().addWidget(self._outputGB)

        # connect signal / slot
        self._preProcessingWidget.sigConfChanged.connect(
            self._signalConfChangedPreProcessing
        )
        self._phaseWidget.sigConfChanged.connect(self._signalConfChangedPhase)
        self._reconstructionWidget.sigConfChanged.connect(
            self._signalConfChangedReconstruction
        )
        self._outputWidget.sigConfChanged.connect(self._signalConfChangedOutput)

        # expose API
        self.getSlices = self._reconstructionWidget.getSlices
        self.setOutputDir = self._outputWidget.setOutputDir

    def setDeltaBetaValue(self, value):
        self._phaseWidget.setDeltaBetaValue(value)

    def hideSlicesInterface(self):
        self._reconstructionWidget.hideSlicesInterface()

    def hidePaganinInterface(self):
        self._stageHided.append(self._phaseGB)
        self._phaseGB.hide()

    def _signalConfChangedPhase(self, param):
        self.sigConfChanged.emit(self._phaseWidget.getStage().value, param)

    def _signalConfChangedPreProcessing(self, param):
        self.sigConfChanged.emit(self._preProcessingWidget.getStage().value, param)

    def _signalConfChangedReconstruction(self, param):
        self.sigConfChanged.emit(self._reconstructionWidget.getStage().value, param)

    def _signalConfChangedOutput(self, param):
        self.sigConfChanged.emit(self._outputWidget.getStage().value, param)

    def getConfiguration(self):
        config = {
            "preproc": self._preProcessingWidget.getConfiguration(),
            "reconstruction": self._reconstructionWidget.getConfiguration(),
            "dataset": self._reconstructionWidget.getDatasetConfiguration(),
            "tomwer_slices": self._reconstructionWidget.getSlices(),
            "output": self._outputWidget.getConfiguration(),
            "phase": self._phaseWidget.getConfiguration(),
        }
        return config

    def setConfiguration(self, config):
        if "preproc" in config:
            self._preProcessingWidget.setConfiguration(config["preproc"])
        if "phase" in config:
            self._phaseWidget.setConfiguration(config["phase"])
        if "reconstruction" in config:
            self._reconstructionWidget.setConfiguration(config["reconstruction"])
        if "tomwer_slices" in config:
            self._reconstructionWidget.setSlices(config["tomwer_slices"])
        if "dataset" in config:
            self._reconstructionWidget.setDatasetConfiguration(config["dataset"])
        if "output" in config:
            self._outputWidget.setConfiguration(config["output"])

    def applyFilter(self, stage, option):
        if stage is None:
            for widget in (
                self._preProcessingGB,
                self._reconstructionGB,
                self._outputGB,
                self._phaseGB,
            ):
                widget.setVisible(True)
        else:
            stage = _NabuStages(stage)
            self._preProcessingGB.setVisible(stage is _NabuStages.PRE)
            self._reconstructionGB.setVisible(stage is _NabuStages.PROC)
            self._outputGB.setVisible(stage is _NabuStages.POST)
            self._phaseGB.setVisible(stage is _NabuStages.PHASE)

        # handle _stageHided list
        for widget in (
            self._preProcessingGB,
            self._reconstructionGB,
            self._outputGB,
            self._phaseGB,
        ):
            if widget in (self._stageHided):
                self._phaseGB.setVisible(False)

    def setConfigurationLevel(self, level):
        for widget in (
            self._preProcessingWidget,
            self._reconstructionWidget,
            self._outputWidget,
            self._phaseWidget,
        ):
            widget.setConfigurationLevel(level)


class NabuConfigurationTab(qt.QTabWidget):
    """
    Top level widget for defining the nabu configuration.
    Same as NabuConfiguration but inside a tab
    """

    sigConfChanged = qt.Signal(str, str)
    """Signal emitted when the configuration change. Parameters are
    (stage, index option modified)
    """

    def __init__(self, parent):
        qt.QTabWidget.__init__(self, parent=parent)

        # pre processing options
        self._preProcessingWidget = _NabuPreProcessingConfig(parent=self)
        self.addTab(self._preProcessingWidget, "pre processing")

        # phase options
        self._phaseGB = qt.QGroupBox("apply phase", self)
        self._phaseGB.setLayout(qt.QVBoxLayout())

        self._phaseWidget = _NabuPhaseConfig(parent=self)
        self._phaseGB.layout().addWidget(self._phaseWidget)
        self.addTab(self._phaseGB, "phase")

        # reconstruction opts
        self._reconstructionWidget = _NabuReconstructionConfig(parent=self)
        self.addTab(self._reconstructionWidget, "reconstruction")

        # output information
        self._outputWidget = _NabuOutputConfig(parent=self)
        self.addTab(self._outputWidget, "output")

        # connect signal / slot
        self._preProcessingWidget.sigConfChanged.connect(
            self._signalConfChangedPreProcessing
        )
        self._phaseWidget.sigConfChanged.connect(self._signalConfChangedPhase)
        self._reconstructionWidget.sigConfChanged.connect(
            self._signalConfChangedReconstruction
        )

        # expose API
        self.getSlices = self._reconstructionWidget.getSlices
        self.setOutputDir = self._outputWidget.setOutputDir

    def _signalConfChangedPhase(self, param):
        self.sigConfChanged.emit(self._phaseWidget.getStage().value, param)

    def _signalConfChangedPreProcessing(self, param):
        self.sigConfChanged.emit(self._preProcessingWidget.getStage().value, param)

    def _signalConfChangedReconstruction(self, param):
        self.sigConfChanged.emit(self._reconstructionWidget.getStage().value, param)

    def getConfiguration(self):
        config = {
            "preproc": self._preProcessingWidget.getConfiguration(),
            "reconstruction": self._reconstructionWidget.getConfiguration(),
            "tomwer_slices": self.getSlices(),
            "output": self._outputWidget.getConfiguration(),
        }
        config["phase"] = self._phaseWidget.getConfiguration()
        return config

    def setConfiguration(self, config):
        if "preproc" in config:
            self._preProcessingWidget.setConfiguration(config["preproc"])
        if "phase" in config:
            self._phaseWidget.setConfiguration(config["phase"])
        if "reconstruction" in config:
            self._reconstructionWidget.setConfiguration(config["reconstruction"])
        if "tomwer_slices" in config:
            self._reconstructionWidget.setSlices(config["tomwer_slices"])

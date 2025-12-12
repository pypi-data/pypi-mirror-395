# coding: utf-8

"""
contains gui relative to semi-automatic axis calculation
"""

from __future__ import annotations


import logging
from typing import Iterable

import numpy
from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuMode,
    retrieve_lst_of_value_from_str,
)
from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    SADeltaBetaTask,
)
from tomwer.core.process.reconstruction.scores.params import ScoreMethod
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui import icons
from tomwer.gui.reconstruction.nabu.nabuconfig.phase import _NabuPhaseConfig
from tomwer.gui.reconstruction.nabu.platform import NabuPlatformSettings
from tomwer.gui.reconstruction.saaxis.sliceselector import SliceSelector
from tomwer.gui.reconstruction.scores.control import ControlWidget
from tomwer.gui.reconstruction.scores.scoreplot import DelaBetaSelection
from tomwer.gui.reconstruction.scores.scoreplot import ScorePlot as _ScorePlot
from tomwer.gui.utils.buttons import TabBrowsersButtons
from tomwer.gui.utils.scandescription import ScanNameLabelAndShape
from tomwer.gui.settings import TAB_LABEL_PLATFORM_SETTINGS
from tomwer.synctools.sadeltabeta import QSADeltaBetaParams
from tomwer.gui.reconstruction.sacommon import NabuWidgetWithToolbar as NabuWidget

_logger = logging.getLogger(__name__)


class ScorePlot(_ScorePlot, constructor=DelaBetaSelection):
    """Score plot dedicated to center delta / beta values."""

    def _updateScores(self):
        scan = self.__scan() if self.__scan else None
        if scan is not None:
            assert isinstance(scan, TomwerScanBase)
            if scan.sa_delta_beta_params:
                scan.sa_delta_beta_params.score_method = self.getScoreMethod()
                # update autofocus
                SADeltaBetaTask.autofocus(scan)
        self.setVarScores(
            scores=self._scores,
            score_method=self.getScoreMethod(),
            update_only_scores=True,
        )

    def _applyAutofocus(self):
        scan = self.__scan() if self.__scan else None
        if scan is None:
            return
        if scan.sa_delta_beta_params:
            best_db = scan.sa_delta_beta_params.autofocus
            if best_db:
                self._varSlider.setVarValue(best_db)


class _SADeltaBetaTabWidget(qt.QTabWidget):
    sigConfigurationChanged = qt.Signal()
    """Signal emit when the configuration changes"""

    def __init__(self, parent=None, backend=None):
        qt.QTabWidget.__init__(self, parent=parent)

        self._deltaBetaSelectionWidget = DeltaBetaSelectionWidget(self)
        delta_beta_icon = icons.getQIcon("delta_beta")
        self.addTab(
            self._deltaBetaSelectionWidget, delta_beta_icon, "delta beta values"
        )
        # nabu reconstruction parameters
        self._nabuSettings = NabuWidget(self)
        self._nabuSettings.setConfigurationLevel(level="required")
        self._nabuSettings.hidePaganinInterface()
        self._nabuSettings.hideSlicesInterface()
        nabu_icon = icons.getQIcon("nabu")
        self.addTab(self._nabuSettings, nabu_icon, "reconstruction settings")
        # platform settings
        self._localPlatformSettings = NabuPlatformSettings(self)
        settings_icons = icons.getQIcon("parameters")
        self.addTab(
            self._localPlatformSettings, settings_icons, TAB_LABEL_PLATFORM_SETTINGS
        )
        # results
        self._resultsViewer = ScorePlot(self, variable_name="db", backend=backend)
        results_icon = icons.getQIcon("results")
        self.addTab(self._resultsViewer, results_icon, "reconstructed slices")

        # connect signal / slot
        self._nabuSettings.sigConfigChanged.connect(self._configurationChanged)
        self._deltaBetaSelectionWidget.sigConfigurationChanged.connect(
            self._configurationChanged
        )
        self._resultsViewer.sigConfigurationChanged.connect(self._configurationChanged)

        # expose function API
        self.setNabuReconsParams = self._nabuSettings.setConfiguration
        self.getNabuReconsParams = self._nabuSettings.getConfiguration
        self.saveReconstructedSlicesTo = self._resultsViewer.saveReconstructedSlicesTo

    def setDeltaBetaScores(self, *args, **kwargs):
        self._resultsViewer.setVarScores(*args, **kwargs)

    def setCurrentVarValue(self, *args, **kwargs):
        self._resultsViewer.setCurrentVarValue(*args, **kwargs)

    def getCurrentVarValue(self):
        return self._resultsViewer.getCurrentVarValue()

    def showResults(self):
        self.setCurrentWidget(self._resultsViewer)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def lockAutoFocus(self, lock):
        self._resultsViewer.lockAutoFocus(lock=lock)

    def isAutoFocusLock(self):
        return self._resultsViewer.isAutoFocusLock()

    def hideAutoFocusButton(self):
        self._resultsViewer.hideAutoFocusButton()

    def getDeltaBetaValues(self):
        """Return db values to be computed"""
        return self._deltaBetaSelectionWidget.getDeltaBetaValues()

    def setDeltaBetaValues(self, values):
        """set db values to be computed"""
        self._deltaBetaSelectionWidget.setDeltaBetaValues(values)

    def loadPreprocessingParams(self):
        """load reconstruction nabu if tomwer has already process this
        dataset. Not done for now"""
        return False

    def setScan(self, scan):
        self._resultsViewer.setScan(scan)
        self._nabuSettings.setScan(scan)
        if self.loadPreprocessingParams() and scan.axis_params is not None:
            self._nabuSettings.setConfiguration(scan.axis_params)
        self._deltaBetaSelectionWidget.setScan(scan)

    def getConfiguration(self):
        nabu_config = self.getNabuReconsParams()
        enable_ht = int(self._nabuSettings.getMode() is _NabuMode.HALF_ACQ)
        nabu_config["reconstruction"]["enable_halftomo"] = enable_ht
        # update phase option
        nabu_config["phase"][
            "padding_type"
        ] = self._deltaBetaSelectionWidget.getPaddingType().value
        nabu_config["phase"][
            "unsharp_coeff"
        ] = self._deltaBetaSelectionWidget.getUnsharpCoeff()
        nabu_config["phase"][
            "unsharp_sigma"
        ] = self._deltaBetaSelectionWidget.getUnsharpSigma()
        return {
            "slice_index": self.getReconstructionSlice(),
            "nabu_params": nabu_config,
            "score_method": self.getScoreMethod().value,
            "delta_beta_values": self.getDeltaBetaValues(),
            "output_dir": nabu_config.get("output", {}).get("location", None) or None,
        }

    def getReconstructionSlice(self):
        return self._deltaBetaSelectionWidget.getSlice()

    def setReconstructionSlice(self, slice_):
        return self._deltaBetaSelectionWidget.setSlice(slice_=slice_)

    def setConfiguration(self, config):
        if isinstance(config, QSADeltaBetaParams):
            config = config.to_dict()
        if not isinstance(config, dict):
            raise TypeError(
                f"config should be a dictionary or a SAAxisParams. Not {type(config)}"
            )

        db_values = config.get("delta_beta_values", None)
        if db_values is not None:
            self.setDeltaBetaValues(db_values)
        slice_index = config.get("slice_index", None)
        if slice_index is not None:
            self.setReconstructionSlice(slice_index)
        if "nabu_params" in config:
            nabu_params = config["nabu_params"]
            self.setNabuReconsParams(nabu_params)
            # special handling of unsharp coeff, sigma and padding type
            padding_type = nabu_params.get("phase", {}).get("padding_type", None)
            if padding_type is not None:
                self._deltaBetaSelectionWidget.setPaddingType(padding_type=padding_type)

            unsharp_coeff = nabu_params.get("phase", {}).get("unsharp_coeff", None)
            if unsharp_coeff is not None:
                self._deltaBetaSelectionWidget.setUnsharpCoeff(coeff=unsharp_coeff)

            unsharp_sigma = nabu_params.get("phase", {}).get("unsharp_sigma", None)
            if unsharp_sigma is not None:
                self._deltaBetaSelectionWidget.setUnsharpSigma(sigma=unsharp_sigma)

        if "score_method" in config:
            self.setScoreMethod(config["score_method"])

    def getScoreMethod(self):
        return self._resultsViewer.getScoreMethod()

    def setScoreMethod(self, method):
        self._resultsViewer.setScoreMethod(method)

    def close(self):
        self._resultsViewer.close()
        self._resultsViewer = None
        self._deltaBetaSelectionWidget.close()
        self._deltaBetaSelectionWidget = None
        self._nabuSettings.close()
        self._nabuSettings = None
        super().close()

    def setSliceRange(self, min_, max_):
        self._deltaBetaSelectionWidget.setSliceRange(min_, max_)


class SADeltaBetaWindow(qt.QMainWindow):
    """
    Widget used to determine half-automatically the better delta / beta value
    """

    def __init__(self, parent=None, backend=None):
        qt.QMainWindow.__init__(self, parent)
        self._db_values = []
        self._urls = []

        self._scan = None
        self._qdeltabeta_rp = QSADeltaBetaParams()
        self.setWindowFlags(qt.Qt.Widget)
        # central widget
        self._mainWidget = qt.QWidget(self)
        self._mainWidget.setLayout(qt.QVBoxLayout())
        self._scanInfo = ScanNameLabelAndShape(self)
        self._mainWidget.layout().addWidget(self._scanInfo)
        self._tabWidget = _SADeltaBetaTabWidget(self, backend=backend)
        self._mainWidget.layout().addWidget(self._tabWidget)
        self.setCentralWidget(self._mainWidget)
        # next and previous buttons for browsing the tab widget
        self._browserButtons = TabBrowsersButtons(self)
        self._dockWidgetBrwButtons = qt.QDockWidget(self)
        self._dockWidgetBrwButtons.setWidget(self._browserButtons)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetBrwButtons)
        self._dockWidgetBrwButtons.setFeatures(qt.QDockWidget.DockWidgetMovable)
        # control widget (validate, compute, cor positions)
        self._sadbControl = ControlWidget(self)
        self._dockWidgetCtrl = qt.QDockWidget(self)
        self._dockWidgetCtrl.setWidget(self._sadbControl)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetCtrl)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)

        # expose signals
        self.sigConfigurationChanged = self._tabWidget.sigConfigurationChanged

        # connect signal / slot
        self._browserButtons.sigNextReleased.connect(self._showNextPage)
        self._browserButtons.sigPreviousReleased.connect(self._showPreviousPage)
        self._sadbControl.sigComputationRequest.connect(self._launchReconstructions)
        self._sadbControl.sigValidateRequest.connect(self._validate)

    def showResults(self):
        self._tabWidget.showResults()

    def compute(self):
        """force compute of the current scan"""
        """force compute of the current scan"""
        self._sadbControl.sigComputationRequest.emit()

    def getConfiguration(self) -> dict:
        return self._tabWidget.getConfiguration()

    def setConfiguration(self, config: dict):
        self._tabWidget.setConfiguration(config)

    def getQDeltaBetaRP(self):
        return self._qdeltabeta_rp

    def setScan(self, scan):
        self._scan = scan
        self._tabWidget.setScan(scan)
        self._scanInfo.setScan(scan)

    def getScan(self):
        return self._scan

    def lockAutofocus(self, lock):
        self._tabWidget.lockAutoFocus(lock=lock)

    def isAutoFocusLock(self):
        return self._tabWidget.isAutoFocusLock()

    def hideAutoFocusButton(self):
        return self._tabWidget.hideAutoFocusButton()

    def _launchReconstructions(self):
        """callback when we want to launch the reconstruction of the
        slice for n delta/beta value"""
        raise NotImplementedError("Base class")

    def _validate(self):
        raise NotImplementedError("Base class")

    def _showNextPage(self, *args, **kwargs):
        idx = self._tabWidget.currentIndex()
        idx += 1
        if idx < self._tabWidget.count():
            self._tabWidget.setCurrentIndex(idx)

    def _showPreviousPage(self, *args, **kwargs):
        idx = self._tabWidget.currentIndex()
        idx -= 1
        if idx >= 0:
            self._tabWidget.setCurrentIndex(idx)

    def close(self):
        self._tabWidget.close()
        self._tabWidget = None
        super().close()

    def setDBScores(
        self,
        scores: dict,
        score_method: str | ScoreMethod,
        img_width=None,
        update_only_scores=False,
    ):
        """

        :param scores: cor value (float) as key and
                            tuple(url: DataUrl, score: float) as value
        """
        self._tabWidget.setDeltaBetaScores(
            scores=scores,
            score_method=score_method,
            img_width=img_width,
            update_only_scores=update_only_scores,
        )

    def getScoreMethod(self):
        return self._tabWidget.getScoreMethod()

    def setCurrentDeltaBetaValue(self, value):
        self._tabWidget.setCurrentVarValue(value)

    def getCurrentDeltaBetaValue(self):
        return self._tabWidget.getCurrentVarValue()

    def setSlicesRange(self, min_, max_):
        self._tabWidget.setSliceRange(min_, max_)

    def saveReconstructedSlicesTo(self, output_folder):
        self._tabWidget.saveReconstructedSlicesTo(output_folder=output_folder)


class DeltaBetaSelectionWidget(qt.QWidget):
    """Widget used to select the range of delta / beta to use"""

    sigConfigurationChanged = qt.Signal()
    """emit when configuration change"""

    _DEFAULT_VERTICAL_SLICE_MODE = ("middle", "other")

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self.setLayout(qt.QVBoxLayout())

        # slice selection
        self._sliceGB = qt.QGroupBox("slice", self)
        self.layout().addWidget(self._sliceGB)
        self._sliceGB.setLayout(qt.QGridLayout())
        self._label = qt.QLabel("slice", self)
        self._sliceGB.layout().addWidget(self._label, 0, 0, 1, 1)
        sl_spacer = qt.QWidget(self)
        sl_spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._sliceGB.layout().addWidget(sl_spacer, 0, 5, 1, 1)

        self._defaultSlicesCB = qt.QComboBox(self)
        for mode in self._DEFAULT_VERTICAL_SLICE_MODE:
            self._defaultSlicesCB.addItem(mode)
        self._sliceGB.layout().addWidget(self._defaultSlicesCB, 0, 1, 1, 1)

        self._sliceSelectionQSB = SliceSelector(self, insert=False, invert_y_axis=True)
        self._sliceSelectionQSB.addSlice(value=0, name="Slice", color="green")
        self._sliceSelectionQSB.setFixedSize(qt.QSize(250, 250))
        self._sliceGB.layout().addWidget(self._sliceSelectionQSB, 1, 0, 1, 5)

        # paganin main window
        self._paganinGB = qt.QGroupBox("paganin", self)
        self._paganinGB.setLayout(qt.QVBoxLayout())
        self._mainWindow = _NabuPhaseConfig(self)
        self._mainWindow.setConfigurationLevel(ConfigurationLevel.ADVANCED)
        self._mainWindow._ctfOpts.hide()
        self._paganinGB.layout().addWidget(self._mainWindow)
        self._mainWindow._methodCB.hide()
        self._mainWindow._methodLabel.hide()
        self.layout().addWidget(self._paganinGB)

        # spacer
        widget_spacer = qt.QWidget(self)
        widget_spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(widget_spacer)

        # connect signal / slot
        self._sliceSelectionQSB.sigSlicesChanged.connect(self._updated)
        self._mainWindow.sigConfChanged.connect(self._updated)
        self._defaultSlicesCB.currentIndexChanged.connect(self._updated)
        self._defaultSlicesCB.currentIndexChanged.connect(self._updateModeCB)

        self.setSlice("middle")

    def _updated(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def setSlice(self, slice_: str | int):
        if isinstance(slice_, str):
            if slice_ != "middle":
                raise ValueError(f"Slice should be 'middle' or an int. Not {slice_}")
            else:
                self.setMode("middle")
        elif isinstance(slice_, int):
            self.setMode("other")
            self._sliceSelectionQSB.setSliceValue("Slice", slice_)
        elif isinstance(slice_, dict) and "Slice" in slice_:
            self.setMode("other")
            self._sliceSelectionQSB.setSliceValue("Slice", slice_["Slice"])
        else:
            raise TypeError(f"slice should be an int or 'middle'. Not {type(slice_)}")

    def setSliceRange(self, min_, max_):
        self._sliceSelectionQSB.setSlicesRange(min_, max_)

    def getMode(self):
        return self._defaultSlicesCB.currentText()

    def setMode(self, mode):
        if mode not in self._DEFAULT_VERTICAL_SLICE_MODE:
            raise ValueError(
                f"mode should be in {self._DEFAULT_VERTICAL_SLICE_MODE}. Not {mode}."
            )
        idx = self._defaultSlicesCB.findText(mode)
        self._defaultSlicesCB.setCurrentIndex(idx)
        self._updateModeCB()

    def _updateModeCB(self):
        self._sliceSelectionQSB.setVisible(self.getMode() == "other")

    def getSlice(self):
        if self.getSliceMode() == "middle":
            return "middle"
        else:
            return self._sliceSelectionQSB.getSlicesValue()

    def getSliceMode(self):
        return self._defaultSlicesCB.currentText()

    def setScan(self, scan: TomwerScanBase):
        self._sliceSelectionQSB.setSlicesRange(0, scan.dim_2)

    def getDeltaBetaValues(self) -> numpy.array:
        db_values = self._mainWindow._paganinOpts.getDeltaBeta()
        return retrieve_lst_of_value_from_str(db_values, type_=float)

    def setDeltaBetaValues(self, values: numpy.array | Iterable):
        values = numpy.array(values)
        step = None
        if len(values) > 3:
            deltas = values[1:] - values[:-1]
            if deltas.min() == deltas.max():
                step = deltas.min()

        deltaBetaQLE = self._mainWindow._paganinOpts._deltaBetaQLE
        if step is None:
            deltaBetaQLE.setText(",".join([str(value) for value in values]))
        else:
            deltaBetaQLE.setText(
                "{from_}:{to_}:{step_}".format(
                    from_=values.min(), to_=values.max(), step_=step
                )
            )

    def getPaddingType(self):
        return self._mainWindow.getPaddingType()

    def setPaddingType(self, padding_type: str):
        self._mainWindow.setPaddingType(padding_type=padding_type)

    def getUnsharpCoeff(self) -> float:
        return self._mainWindow.getUnsharpCoeff()

    def setUnsharpCoeff(self, coeff) -> float:
        return self._mainWindow.setUnsharpCoeff(coeff=coeff)

    def getUnsharpSigma(self) -> float:
        return self._mainWindow.getUnsharpSigma()

    def setUnsharpSigma(self, sigma):
        self._mainWindow.setUnsharpSigma(sigma=sigma)

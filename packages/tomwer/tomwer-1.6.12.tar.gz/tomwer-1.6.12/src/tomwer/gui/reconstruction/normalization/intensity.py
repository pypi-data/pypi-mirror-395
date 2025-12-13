# coding: utf-8
"""
contains gui relative to intensity normalization
"""

from __future__ import annotations


import weakref

from silx.gui import qt
from silx.gui.dialog.DataFileDialog import DataFileDialog
from silx.gui.plot.items.roi import HorizontalRangeROI, RectangleROI
from silx.gui.plot.tools.roi import RegionOfInterestManager
from silx.io.url import DataUrl
from tomoscan.normalization import Method

from tomwer.core.process.reconstruction.normalization import params as _normParams
from tomwer.core.process.reconstruction.normalization.params import _ValueSource
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.gui.reconstruction.scores.control import ControlWidget
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.visualization.dataviewer import DataViewer
from tomwer.gui.visualization.sinogramviewer import SinogramViewer as _SinogramViewer


class SinoNormWindow(qt.QMainWindow):
    sigConfigurationChanged = qt.Signal()
    """signal emit when the configuration change"""

    def __init__(self, parent, backend=None):
        qt.QMainWindow.__init__(self, parent)
        self._scan = None
        self.setWindowFlags(qt.Qt.Widget)

        # central widget
        self._centralWidget = _Viewer(self, backend=backend)
        self.setCentralWidget(self._centralWidget)

        # control widget (options + ctrl buttons)
        self._dockWidgetWidget = qt.QWidget(self)
        self._dockWidgetWidget.setLayout(qt.QVBoxLayout())
        self._optsWidget = _NormIntensityOptions(self)
        self._dockWidgetWidget.layout().addWidget(self._optsWidget)
        self._spacer = qt.QWidget(self)
        self._spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self._dockWidgetWidget.layout().addWidget(self._spacer)
        self._crtWidget = _NormIntensityControl(self)
        self._dockWidgetWidget.layout().addWidget(self._crtWidget)

        # dock widget
        self._dockWidgetCtrl = qt.QDockWidget(parent=self)
        self._dockWidgetCtrl.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetCtrl.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockWidgetCtrl.setWidget(self._dockWidgetWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockWidgetCtrl)

        # connect signal / slot
        # self._optsWidget.sigModeChanged.connect(self._modeChanged)
        self._optsWidget.sigValueUpdated.connect(self.setResult)
        self._optsWidget.sigConfigurationChanged.connect(self.sigConfigurationChanged)
        self._optsWidget.sigSourceChanged.connect(self._sourceChanged)
        self._crtWidget.sigValidateRequest.connect(self._validated)

        # set up
        self._centralWidget._updateSinogramROI()
        self._modeChanged()

    def _hideLockButton(self):
        self._optsWidget._hideLockButton()

    def _validated(self):
        pass

    def getConfiguration(self) -> dict:
        return self._optsWidget.getConfiguration()

    def setConfiguration(self, config: dict):
        self._optsWidget.setConfiguration(config=config)

    def setCurrentMethod(self, method):
        self._optsWidget.setCurrentMethod(method=method)

    def getCurrentMethod(self):
        return self._optsWidget.getCurrentMethod()

    def setCurrentSource(self, source):
        self._optsWidget.setCurrentSource(source=source)

    def getCurrentSource(self):
        return self._optsWidget.getCurrentSource()

    def _modeChanged(self):
        self._sourceChanged()

    def _sourceChanged(self):
        source = self.getCurrentSource()
        method = self.getCurrentMethod()
        scan = self.getScan()

        methods_using_manual_roi = (Method.DIVISION, Method.SUBTRACTION)

        self._centralWidget.setManualROIVisible(
            source is _ValueSource.MANUAL_ROI and method in methods_using_manual_roi
        )
        if scan:
            methods_requesting_calculation = (Method.DIVISION, Method.SUBTRACTION)
            if method in methods_requesting_calculation:
                # if the normed sinogram can be obtained `directly`
                if source in (_ValueSource.MANUAL_SCALAR, _ValueSource.DATASET):
                    scan.intensity_normalization = self.getCurrentMethod().value
                    extra_info = self.getExtraArgs()
                    extra_info.update(
                        {
                            "tomwer_processing_res_code": True,
                            "source": source.value,
                        }
                    )
                    scan.intensity_normalization.set_extra_infos(extra_info)
        self._centralWidget._updateSinogramROI()

    def getScan(self):
        if self._scan is not None:
            return self._scan()
        else:
            return None

    def setScan(self, scan: TomwerScanBase | None):
        self._scan = weakref.ref(scan)
        self._centralWidget.setScan(scan=scan)
        self._optsWidget.setScan(scan=scan)

    def getExtraArgs(self) -> dict:
        return self._optsWidget.getExtraInfos()

    def getROI(self):
        return self._centralWidget.getROI()

    def setROI(self, start_x, end_x, start_y, end_y):
        self._centralWidget.setROI(
            start_x=start_x, end_x=end_x, start_y=start_y, end_y=end_y
        )

    def setResult(self, result):
        self._crtWidget.setResult(result)

    def clear(self):
        self._crtWidget.clear()

    def isLocked(self):
        return self._optsWidget.isLocked()

    def setLocked(self, locked):
        self._optsWidget.setLocked(locked)


class _Viewer(qt.QTabWidget):
    def __init__(self, parent, backend=None):
        if not isinstance(parent, SinoNormWindow):
            raise TypeError("Expect a NormIntensityWindow as parrent")
        qt.QTabWidget.__init__(self, parent)
        self._projView = _ProjPlotWithROI(parent=self, backend=backend)
        self.addTab(self._projView, "projection view")
        self._sinoView = SinogramViewer(parent=self, backend=backend)
        self.addTab(self._sinoView, "sinogram view")

        # connect signal / Slot
        self._sinoView.sigSinogramLineChanged.connect(self._projView.setSinogramLine)
        self._sinoView.sigSinoLoadEnded.connect(self._updateSinogramROI)
        self._projView.sigROIChanged.connect(self._updateSinogramROI)

    def setScan(self, scan: TomwerScanBase | None):
        """

        :param scan: scan to handle
        :return:
        """
        self._projView.setScan(scan)
        self._sinoView.setScan(scan, update=False)

    def _updateSinogramROI(self):
        source = self.parent().getCurrentSource()
        method = self.parent().getCurrentMethod()

        display_sino_roi = source is _ValueSource.MANUAL_ROI and method in (
            Method.DIVISION,
            Method.SUBTRACTION,
        )

        if display_sino_roi:
            roi = self._projView.getROI()
            sinogram_line = self._sinoView.getLine()
            y_min = roi.getOrigin()[1]
            y_max = roi.getOrigin()[1] + roi.getSize()[1]
            if y_min <= sinogram_line <= y_max:
                x_min = roi.getOrigin()[0]
                x_max = roi.getOrigin()[0] + roi.getSize()[0]
                self._sinoView.setROIRange(x_min, x_max)
                self._sinoView.setROIVisible(True)
            else:
                self._sinoView.setROIVisible(False)
        else:
            self._sinoView.setROIVisible(False)

    def setManualROIVisible(self, visible):
        self._projView.setManualROIVisible(visible=visible)
        self._sinoView.setROIVisible(visible=visible)

    def getROI(self):
        return self._projView.getROI()

    def setROI(self, start_x, end_x, start_y, end_y):
        self._projView.setROI(
            start_x=start_x, end_x=end_x, start_y=start_y, end_y=end_y
        )


class _ProjPlotWithROI(DataViewer):
    """DataViewer specialized on projections. Embed a RectangleROI"""

    sigROIChanged = qt.Signal()
    """signal emit when ROI change"""

    def __init__(self, *args, **kwargs):
        DataViewer.__init__(self, *args, **kwargs, show_overview=False)
        self._sinogramLine = 0
        self._roiVisible = False
        self.setScanInfoVisible(False)
        self.setDisplayMode("projections-radios")
        self.setDisplayModeVisible(False)

        dw = self.getUrlListDockWidget()
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, dw)
        dw.setFeatures(qt.QDockWidget.DockWidgetMovable)

        # add ROI
        self._roiManager = RegionOfInterestManager(self.getPlotWidget())
        self._roi = RectangleROI()
        self._roi.setName("ROI")
        self._roi.setLineStyle("-.")
        self._roi.setGeometry(origin=(0, 0), size=(200, 200))
        self._roi.setEditable(True)
        self._roi.setVisible(True)
        self._roiManager.addRoi(self._roi)

        # connect signal / slot
        self.getPlotWidget().sigActiveImageChanged.connect(self._updateSinogramLine)
        self.getPlotWidget().sigActiveImageChanged.connect(self._updateROI)
        self._roi.sigEditingFinished.connect(self._roiChanged)

    def getROI(self):
        return self._roi

    def setROI(self, start_x, end_x, start_y, end_y):
        self._roi.setOrigin((start_x, start_y))
        self._roi.setSize((end_x - start_x, end_y - start_y))

    def setManualROIVisible(self, visible):
        self._roiVisible = visible
        self._updateROIVisibility()

    def _updateROIVisibility(self):
        self._roi.setVisible(self._roiVisible)

    def _roiChanged(self):
        self.sigROIChanged.emit()

    def setSinogramLine(self, line):
        self._sinogramLine = line
        self._updateSinogramLine()

    def _updateROI(self):
        """ImageStack clean the plot which bring item removal. This is
        why we need to add them back"""
        if self._roi is not None:
            for item in self._roi.getItems():
                if item not in self.getPlotWidget().getItems():
                    self.getPlotWidget().addItem(item)

    def _updateSinogramLine(self):
        self._roiManager = RegionOfInterestManager(self.getPlotWidget())

        self.getPlotWidget().addYMarker(
            y=self._sinogramLine,
            legend="sinogram_line",
            text="sinogram line",
            color="blue",
            selectable=False,
        )
        sino_marker = self.getPlotWidget()._getMarker("sinogram_line")
        if sino_marker:
            sino_marker.setLineStyle("--")

    def clear(self):
        super().clear()
        self.getPlotWidget().removeMarker("sinogram_line")


class SinogramViewer(_SinogramViewer):
    """ "Sinogram viewer but adapated for Intensity normalization"""

    sigSinogramLineChanged = qt.Signal(int)
    """signal emit when the selected sinogram line changes"""

    def __init__(self, *args, **kwargs):
        _SinogramViewer.__init__(self, *args, **kwargs)

        dockWidget = self.getOptionsDockWidget()
        self.addDockWidget(qt.Qt.TopDockWidgetArea, dockWidget)
        dockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)

        # change ApplyButton name and icon
        self._loadButton = self._options._buttons.button(qt.QDialogButtonBox.Apply)
        self._loadButton.setText("load")
        style = qt.QApplication.style()
        self._loadButton.setIcon(style.standardIcon(qt.QStyle.SP_BrowserReload))

        # ROI
        self._roiManager = RegionOfInterestManager(self.getPlotWidget())
        self._roi = HorizontalRangeROI()
        self._roi.setRange(0, 0)
        self._roi.setVisible(True)
        self._roi.setColor((250, 50, 50, 150))
        self._roi.setLineWidth(1.5)
        self._roi.setLineStyle("-.")
        self._roiManager.addRoi(self._roi)

        # connect signal / Slots
        self._options._lineSB.valueChanged.connect(self._sinogramLineChanged)
        self.sigSinogramLineChanged.connect(self._plot.clear)
        self.getPlotWidget().sigActiveImageChanged.connect(self._updateROI)

    def _sinogramLineChanged(self):
        self.sigSinogramLineChanged.emit(self.getLine())

    def setROIRange(self, x_min, x_max):
        self._roi.setRange(x_min, x_max)

    def setROIVisible(self, visible):
        self._roi.setVisible(visible)

    def _updateROI(self):
        """ImageStack clean the plot which bring item removal. This is
        why we need to add them back"""
        if self._roi is not None:
            for item in self._roi.getItems():
                if item not in self.getPlotWidget().getItems():
                    self.getPlotWidget().addItem(item)

    def getPlotWidget(self):
        return self._plot

    def _updatePlot(self, sinogram):
        self.getPlotWidget().addImage(data=sinogram)
        self.getPlotWidget().replot()


class _NormIntensityOptions(qt.QWidget):
    sigValueCanBeLocked = qt.Signal(bool)

    sigProcessingRequested = qt.Signal()
    """Signal emit when the processing is requested"""

    sigModeChanged = qt.Signal()
    """signal emitted when the mode change"""

    sigSourceChanged = qt.Signal()
    """signal emitted when the source change"""

    sigValueUpdated = qt.Signal(object)
    """Signal emit when user defines manually the value"""

    sigConfigurationChanged = qt.Signal()
    """Signal emit when the configuration changes"""

    def __init__(self, parent):
        if not isinstance(parent, SinoNormWindow):
            raise TypeError(
                "parent is expected to be an instance of " "NormIntensityWindow "
            )
        qt.QWidget.__init__(self, parent)
        self._getROI = self.parent().getROI
        self.setLayout(qt.QGridLayout())
        # mode
        self._modeCB = qt.QComboBox(self)
        for mode in Method:
            if mode in (Method.LSQR_SPLINE,):
                continue
            else:
                self._modeCB.addItem(mode.value)
        self.layout().addWidget(qt.QLabel("mode:", self), 0, 0, 1, 1)
        self.layout().addWidget(self._modeCB, 0, 1, 1, 1)
        self._lockButton = PadlockButton(self)
        self._lockButton.setFixedWidth(25)
        self.layout().addWidget(self._lockButton, 0, 2, 1, 1)
        # source
        self._sourceCB = qt.QComboBox(self)
        for mode in _ValueSource:
            if mode == _ValueSource.NONE:
                # filter this value because does not have much sense for the GUI
                continue
            if mode in (_ValueSource.AUTO_ROI, _ValueSource.MONITOR):
                continue
            self._sourceCB.addItem(mode.value)
        self._sourceLabel = qt.QLabel("source:", self)
        self.layout().addWidget(self._sourceLabel, 1, 0, 1, 1)
        self.layout().addWidget(self._sourceCB, 1, 1, 1, 1)
        # method
        self._optsMethod = qt.QGroupBox(self)
        self._optsMethod.setTitle("options")
        self._optsMethod.setLayout(qt.QVBoxLayout())
        self.layout().addWidget(self._optsMethod, 2, 0, 1, 3)
        # intensity calculation options
        self._intensityCalcOpts = _NormIntensityCalcOpts(self)
        self._optsMethod.layout().addWidget(self._intensityCalcOpts)
        # dataset widget
        self._datasetWidget = _NormIntensityDatasetWidget(self)
        self._optsMethod.layout().addWidget(self._datasetWidget)
        # scalar value
        self._scalarValueWidget = _NormIntensityScalarValue(self)
        self.layout().addWidget(self._scalarValueWidget, 3, 0, 1, 3)
        # buttons
        self._buttonsGrp = qt.QWidget(self)
        self._buttonsGrp.setLayout(qt.QGridLayout())
        self._buttonsGrp.layout().setContentsMargins(0, 0, 0, 0)
        self._computeButton = qt.QPushButton("compute", self)
        self._buttonsGrp.layout().addWidget(self._computeButton, 0, 1, 1, 1)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._buttonsGrp.layout().addWidget(spacer)
        self.layout().addWidget(self._buttonsGrp, 4, 0, 1, 3)

        self._modeChanged()

        # connect signal / slot
        self._modeCB.currentIndexChanged.connect(self._modeChanged)
        self._modeCB.currentIndexChanged.connect(self.sigConfigurationChanged)
        self._sourceCB.currentIndexChanged.connect(self._sourceChanged)
        self._sourceCB.currentIndexChanged.connect(self.sigConfigurationChanged)
        self._computeButton.released.connect(self.sigProcessingRequested)
        self._scalarValueWidget.sigValueChanged.connect(self._valueUpdated)
        self._scalarValueWidget.sigValueChanged.connect(self.sigConfigurationChanged)
        self._datasetWidget.sigConfigurationChanged.connect(
            self.sigConfigurationChanged
        )
        self._intensityCalcOpts.sigConfigurationChanged.connect(
            self.sigConfigurationChanged
        )
        self._lockButton.toggled.connect(self._lockChanged)
        self._lockButton.toggled.connect(self.sigConfigurationChanged)

    def _sourceChanged(self):
        source = self.getCurrentSource()
        method = self.getCurrentMethod()
        interactive_methods = (Method.DIVISION, Method.SUBTRACTION)
        interactive_sources = (
            _ValueSource.MANUAL_ROI,
            _ValueSource.AUTO_ROI,
            _ValueSource.DATASET,
        )
        self._datasetWidget.setVisible(source == _ValueSource.DATASET)
        self.setManualROIVisible(source == _ValueSource.MANUAL_ROI)
        self._optsMethod.setVisible(
            method in interactive_methods and source in interactive_sources
        )
        self._intensityCalcOpts.setCalculationFctVisible(
            method in interactive_methods
            and source in interactive_sources
            and source is not _ValueSource.DATASET
        )
        self._scalarValueWidget.setVisible(source == _ValueSource.MANUAL_SCALAR)
        self._buttonsGrp.setVisible(
            method in interactive_methods and source in interactive_sources
        )

        self.sigSourceChanged.emit()

    def _lockChanged(self):
        self._scalarValueWidget.setEnabled(not self.isLocked())
        self._datasetWidget.setEnabled(not self.isLocked())
        self._intensityCalcOpts.setEnabled(not self.isLocked())
        self._modeCB.setEnabled(not self.isLocked())
        self._computeButton.setEnabled(not self.isLocked())

    def isLocked(self):
        return self._lockButton.isLocked()

    def setLocked(self, locked):
        self._lockButton.setChecked(locked)

    def _hideLockButton(self):
        self._lockButton.hide()

    def getCurrentMethod(self):
        return Method(self._modeCB.currentText())

    def setCurrentMethod(self, method):
        method = Method(method)
        idx = self._modeCB.findText(method.value)
        self._modeCB.setCurrentIndex(idx)

    def getCurrentSource(self):
        if self.getCurrentMethod() in (Method.DIVISION, Method.SUBTRACTION):
            return _ValueSource(self._sourceCB.currentText())
        else:
            return _ValueSource.NONE

    def setCurrentSource(self, source):
        source = _ValueSource(source)
        idx = self._sourceCB.findText(source.value)
        self._sourceCB.setCurrentIndex(idx)

    def _modeChanged(self, *args, **kwargs):
        mode = self.getCurrentMethod()
        mode_with_calculations = (Method.DIVISION, Method.SUBTRACTION)
        self._intensityCalcOpts.setVisible(mode in mode_with_calculations)
        self._sourceCB.setVisible(mode in mode_with_calculations)
        self._sourceLabel.setVisible(mode in mode_with_calculations)
        self._sourceChanged()
        self.sigModeChanged.emit()
        self.sigSourceChanged.emit()

    def _valueUpdated(self, *args):
        self.sigValueUpdated.emit(args)

    def setManualROIVisible(self, visible):
        pass

    def getConfiguration(self) -> dict:
        return _normParams.SinoNormalizationParams(
            method=self.getCurrentMethod(),
            source=self.getCurrentSource(),
            extra_infos=self.getExtraInfos(),
        ).to_dict()

    def setConfiguration(self, config: dict):
        params = _normParams.SinoNormalizationParams.from_dict(config)
        self.setCurrentMethod(params.method)
        extra_infos = params.extra_infos
        if (
            "start_x" in extra_infos
            and "start_y" in extra_infos
            and "end_x" in extra_infos
            and "end_y" in extra_infos
        ):
            start_x = extra_infos["start_x"]
            start_y = extra_infos["start_y"]
            end_x = extra_infos["end_x"]
            end_y = extra_infos["end_y"]
            self._getROI().setOrigin((start_x, start_y))
            self._getROI().setSize((end_x - start_x, end_y - start_y))
        if "calc_fct" in extra_infos:
            self._intensityCalcOpts.setCalculationFct(extra_infos["calc_fct"])
        if "calc_area" in extra_infos:
            self._intensityCalcOpts.setCalculationArea(extra_infos["calc_area"])
        if "calc_method" in extra_infos:
            self._intensityCalcOpts.setCalculationMethod(extra_infos["calc_method"])
        if params.source is _ValueSource.MANUAL_SCALAR:
            if "value" in extra_infos:
                self._scalarValueWidget.setValue(extra_infos["value"])

    def setScan(self, scan):
        self._datasetWidget.setScan(scan=scan)

    def getExtraInfos(self):
        method = self.getCurrentMethod()
        source = self.getCurrentSource()
        if method in (Method.CHEBYSHEV, Method.NONE):
            return {}
        else:
            if source is _ValueSource.MANUAL_SCALAR:
                return {"value": self._scalarValueWidget.getValue()}
            elif source is _ValueSource.AUTO_ROI:
                raise NotImplementedError("auto roi not implemented yet")
            elif source is _ValueSource.MANUAL_ROI:
                roi = self._getROI()
                return {
                    "start_x": roi.getOrigin()[0],
                    "end_x": roi.getOrigin()[0] + roi.getSize()[0],
                    "start_y": roi.getOrigin()[1],
                    "end_y": roi.getOrigin()[1] + roi.getSize()[1],
                    "calc_fct": self._intensityCalcOpts.getCalculationFct().value,
                }
            elif source is _ValueSource.DATASET:
                return {
                    "dataset_url": self._datasetWidget.getDatasetUrl().path(),
                }
            else:
                raise ValueError(f"unhandled source: {source} for method {method}")


class _NormIntensityCalcOpts(qt.QWidget):
    """Options to compute the norm intensity"""

    sigConfigurationChanged = qt.Signal()
    """Signal emitted when configuration changes"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QFormLayout())
        # calculation function
        self._calculationModeCB = qt.QComboBox(self)
        for fct in _normParams._ValueCalculationFct:
            self._calculationModeCB.addItem(fct.value)
        self._calculationModeLabel = qt.QLabel("calculation fct", self)
        self.layout().addRow(self._calculationModeLabel, self._calculationModeCB)

        # connect signal / slot
        self._calculationModeCB.currentIndexChanged.connect(
            self.sigConfigurationChanged
        )

    def setCalculationFctVisible(self, visible):
        self._calculationModeLabel.setVisible(visible)
        self._calculationModeCB.setVisible(visible)

    def getCalculationFct(self):
        return _normParams._ValueCalculationFct(self._calculationModeCB.currentText())

    def setCalculationFct(self, fct):
        idx = self._calculationModeCB.findText(_normParams._ValueCalculationFct(fct))
        self._calculationModeCB.setCurrentIndex(idx)


class _NormIntensityControl(ControlWidget):
    def __init__(self, parent=None):
        ControlWidget.__init__(self, parent)
        self._resultWidget = qt.QWidget(self)
        self._resultWidget.setLayout(qt.QFormLayout())
        self._result = None

        self._resultQLE = qt.QLineEdit("", self)
        self._resultWidget.layout().addRow("value:", self._resultQLE)
        self._resultQLE.setReadOnly(True)
        self.layout().insertWidget(0, self._resultWidget)

        self._computeBut.hide()

    def setResult(self, result):
        self._result = result
        if isinstance(result, tuple):
            result = ",".join([str(element) for element in result])
        self._resultQLE.setText(str(result))

    def getResult(self):
        return self._result

    def clear(self):
        self._resultQLE.clear()


class _NormIntensityScalarValue(qt.QWidget):
    sigValueChanged = qt.Signal(float)
    """emit when the scalar value to norm intensity change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QFormLayout())
        self._QLE = qt.QLineEdit("0.0", self)
        validator = qt.QDoubleValidator(parent=self)
        self._QLE.setValidator(validator)
        self.layout().addRow("value", self._QLE)

        # connect signal / slot
        self._QLE.editingFinished.connect(self._valueChanged)

    def setValue(self, value):
        self._QLE.setText(str(value))

    def getValue(self):
        return float(self._QLE.text())

    def _valueChanged(self):
        self.sigValueChanged.emit(self.getValue())


class _NormIntensityDatasetWidget(qt.QWidget):
    _FILE_PATH_LOCAL_VALUE = "scan master file"

    sigConfigurationChanged = qt.Signal()
    """emit when configuration change"""

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._lastGlobalPath = None
        self._scan = None

        self.setLayout(qt.QGridLayout())
        # file scope
        self._fileScopeGB = qt.QGroupBox("file scope", self)
        self._fileScopeGB.setLayout(qt.QVBoxLayout())
        self._buttonGrpBox = qt.QButtonGroup(self)
        self._globalRB = qt.QRadioButton(_normParams._DatasetScope.GLOBAL.value, self)
        self._buttonGrpBox.addButton(self._globalRB)
        self._globalRB.setToolTip("Global dataset. Will be constant with time")
        self._fileScopeGB.layout().addWidget(self._globalRB)
        self._localRB = qt.QRadioButton(_normParams._DatasetScope.LOCAL.value, self)
        self._buttonGrpBox.addButton(self._localRB)
        self._localRB.setToolTip(
            "Local dataset."
            "Must be contained in the NXtomo entry "
            "provided (not compatible with EDF)."
        )
        self._fileScopeGB.layout().addWidget(self._localRB)
        self.layout().addWidget(self._fileScopeGB, 0, 0, 3, 3)
        # file_path
        self._filePathLabel = qt.QLabel("file path", self)
        self.layout().addWidget(self._filePathLabel, 3, 0, 1, 1)
        self._filePathQLE = qt.QLineEdit("", self)
        self.layout().addWidget(self._filePathQLE, 3, 1, 1, 1)
        self._selectFileButton = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectFileButton, 3, 2, 1, 1)
        # data path
        self._dataPathLabel = qt.QLabel("data path", self)
        self.layout().addWidget(self._dataPathLabel, 4, 0, 1, 1)
        self._dataPathQLE = qt.QLineEdit("", self)
        self.layout().addWidget(self._dataPathQLE, 4, 1, 1, 1)
        self._selectDataPathButton = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectDataPathButton, 4, 2, 1, 1)

        # set up
        self._localRB.setChecked(True)
        self._updateFilePathVisibility()

        # connect signal / slot
        self._buttonGrpBox.buttonToggled.connect(self._updateFilePathVisibility)
        self._selectFileButton.released.connect(self._selectFile)
        self._selectDataPathButton.released.connect(self._selectDataPath)
        self._buttonGrpBox.buttonReleased.connect(self._configurationChanged)
        self._filePathQLE.editingFinished.connect(self._configurationChanged)
        self._dataPathQLE.editingFinished.connect(self._configurationChanged)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigurationChanged.emit()

    def setScan(self, scan):
        if scan is not None:
            self._scan = weakref.ref(scan)
        return None

    def getScan(self):
        if self._scan is not None:
            return self._scan()
        else:
            return None

    def getMode(self) -> _normParams._DatasetScope:
        if self._localRB.isChecked():
            return _normParams._DatasetScope.LOCAL
        else:
            return _normParams._DatasetScope.GLOBAL

    def getDataPath(self):
        return self._dataPathQLE.text()

    def setDataPath(self, path):
        self._dataPathQLE.setText(path)

    def getGlobalFilePath(self) -> str:
        return self._filePathQLE.text()

    def setGlobalFilePath(self, file_path):
        self._filePathQLE.setText(file_path)

    def getDatasetUrl(self) -> DataUrl:
        if self.getMode() is _normParams._DatasetScope.LOCAL:
            if self.getScan() is not None:
                scan = self.getScan()
                file_path = scan.master_file
            else:
                file_path = None
        else:
            file_path = self.getGlobalFilePath()
        data_path = self.getDataPath()
        if file_path is not None and file_path.lower().endswith("edf"):
            scheme = "fabio"
        else:
            scheme = "silx"

        return DataUrl(
            file_path=file_path,
            data_path=data_path,
            scheme=scheme,
        )

    def setDatasetUrl(self, url: DataUrl):
        raise NotImplementedError("")

    def _updateFilePathVisibility(self):
        self._filePathQLE.setReadOnly(self.getMode() == _normParams._DatasetScope.LOCAL)
        self._filePathQLE.setEnabled(self.getMode() == _normParams._DatasetScope.GLOBAL)
        self._selectFileButton.setEnabled(
            self.getMode() == _normParams._DatasetScope.GLOBAL
        )
        if (
            self.getMode() == _normParams._DatasetScope.LOCAL
            and self.getGlobalFilePath() != self._FILE_PATH_LOCAL_VALUE
        ):
            self._lastGlobalPath = self.getGlobalFilePath()
            self.setGlobalFilePath(self._FILE_PATH_LOCAL_VALUE)
        elif (
            self.getMode() == _normParams._DatasetScope.GLOBAL
            and self.getGlobalFilePath() == self._FILE_PATH_LOCAL_VALUE
        ):
            if self._lastGlobalPath is not None:
                self.setGlobalFilePath(self._lastGlobalPath)

    def _selectFile(self):  # pragma: no cover
        dialog = qt.QFileDialog(self)
        dialog.setNameFilters(["HDF5 file *.h5 *.hdf5 *.nx *.nxs *.nexus"])

        if not dialog.exec():
            dialog.close()
            return

        filesSelected = dialog.selectedFiles()
        if len(filesSelected) > 0:
            self.setGlobalFilePath(filesSelected[0])

    def _selectDataPath(self):
        """Open a dialog. If from a master file try to open the scan
        master file if any."""
        if self.getMode() is _normParams._DatasetScope.LOCAL:
            if self.getScan() is not None:
                scan = self.getScan()
                if not isinstance(scan, NXtomoScan):
                    mess = qt.QMessageBox(
                        parent=self,
                        icon=qt.QMessageBox.Warning,
                        text="local mode is only available for HDF5 acquisitions",
                    )
                    mess.setModal(False)
                    mess.show()
                    return
                else:
                    file_ = scan.master_file
            else:
                mess = qt.QMessageBox(
                    parent=self,
                    icon=qt.QMessageBox.Information,
                    text="No scan set. Unable to find the master file",
                )
                mess.setModal(False)
                mess.show()
                return
        elif self.getMode() is _normParams._DatasetScope.GLOBAL:
            file_ = self.getGlobalFilePath()
        else:
            raise ValueError(f"{self.getMode()} is not handled")

        dialog = DataFileDialog()
        dialog.selectFile(file_)
        dialog.setFilterMode(DataFileDialog.FilterMode.ExistingDataset)

        if not dialog.exec():
            dialog.close()
            return
        else:
            selected_url = dialog.selectedUrl()
            self.setDataPath(DataUrl(path=selected_url).data_path())

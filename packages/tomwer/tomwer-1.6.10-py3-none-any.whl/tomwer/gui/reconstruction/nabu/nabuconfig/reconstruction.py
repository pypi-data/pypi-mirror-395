# coding: utf-8
from __future__ import annotations


import functools
import logging

from silx.gui import qt
from silx.gui.dialog.DataFileDialog import DataFileDialog
from enum import Enum as _Enum

from nxtomomill.models.utils import convert_str_to_tuple
from tomwer.core.utils.char import DEGREE_CHAR
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.process.reconstruction.nabu.nabuslices import NabuSliceMode
from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuFBPFilterType,
    _NabuPaddingType,
    _NabuReconstructionMethods,
    _NabuStages,
)
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.gui.utils.inputwidget import SelectionLineEdit
from tomwer.gui.utils.scrollarea import (
    QComboBoxIgnoreWheel,
    QDoubleSpinBoxIgnoreWheel,
    QSpinBoxIgnoreWheel,
)
from tomwer.gui.utils.RangeWidget import RangeWidget
from tomwer.gui import icons
from tomwer.utils import docstring

_logger = logging.getLogger(__name__)


class SliceGroupBox(qt.QGroupBox):
    """GroupBox to define slice to be reconstructed"""

    sigSlicesChanged = qt.Signal()
    """Signal emitted when the selected slices change"""

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, "slices", parent)
        self.setCheckable(True)
        self.setLayout(qt.QHBoxLayout())
        # mode
        self._modeCB = QComboBoxIgnoreWheel(parent=self)
        for mode in NabuSliceMode:
            self._modeCB.addItem(mode.value)
        self.layout().addWidget(self._modeCB)
        self._modeCB.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        # slice line edit
        self._sliceQLE = SelectionLineEdit(parent=self, allow_negative_indices=True)
        self.layout().addWidget(self._sliceQLE)

        # warning icon
        warningIcon = icons.getQIcon("warning")
        self._noSliceWarning = qt.QLabel("")
        self._noSliceWarning.setPixmap(warningIcon.pixmap(20, state=qt.QIcon.On))
        self._noSliceWarning.setToolTip(
            "no slice defined, No slice reconstruction will be done"
        )
        self.layout().addWidget(self._noSliceWarning)

        # spacer
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        # set up
        self.setChecked(True)
        self.setMode(NabuSliceMode.MIDDLE)
        self._sliceQLE.setVisible(False)
        self._noSliceWarning.setVisible(False)

        # connect signal / slot
        self._modeCB.currentIndexChanged.connect(self._updateSliceQLEVisibility)
        self._modeCB.currentIndexChanged.connect(self.sigSlicesChanged)
        self._sliceQLE.editingFinished.connect(self.sigSlicesChanged)
        self._sliceQLE.textChanged.connect(self._updateNoSliceWarningVisibility)
        self.toggled.connect(self.sigSlicesChanged)

    def _updateSliceQLEVisibility(self, *args, **kwargs):
        self._sliceQLE.setVisible(self.getMode() == NabuSliceMode.OTHER)
        self._updateNoSliceWarningVisibility()

    def _updateNoSliceWarningVisibility(self):
        def no_other_slice_defined() -> bool:
            slices_defined = self._sliceQLE.text().replace(" ", "")
            slices_defined = self._sliceQLE.text().replace(",", "")
            slices_defined = self._sliceQLE.text().replace(";", "")
            return slices_defined == ""

        self._noSliceWarning.setVisible(
            self.getMode() is NabuSliceMode.OTHER and no_other_slice_defined()
        )

    def setMode(self, mode: NabuSliceMode):
        mode = NabuSliceMode(mode)
        item_index = self._modeCB.findText(mode.value)
        self._modeCB.setCurrentIndex(item_index)
        old = self.blockSignals(True)
        self._updateSliceQLEVisibility()
        self.blockSignals(old)

    def getMode(self) -> NabuSliceMode:
        mode = NabuSliceMode(self._modeCB.currentText())
        return mode

    def _getSliceSelected(self):
        if self.getMode() is NabuSliceMode.MIDDLE:
            return NabuSliceMode.MIDDLE.value
        else:
            return self._sliceQLE.text()

    def getSlices(self):
        """Slice selected"""
        if self.isChecked():
            return self._getSliceSelected()
        else:
            return None

    def setSlices(self, slices):
        if slices is None:
            self.setChecked(False)
        else:
            self.setChecked(True)
            if slices != NabuSliceMode.MIDDLE.value:
                self._sliceQLE.setText(slices)
                self.setMode(NabuSliceMode.OTHER)
            else:
                self.setMode(NabuSliceMode.MIDDLE)


class TranslationMvtFileWidget(qt.QWidget):
    """Widget used to define a .cvs or a DataUrl"""

    class Mode(_Enum):
        HDF5 = "hdf5"
        TEXT = "text"

    fileChanged = qt.Signal()
    """Signal emitted when the file change"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())

        self._checkBox = qt.QCheckBox(self)
        self.layout().addWidget(self._checkBox)

        self._translationFileQLE = qt.QLineEdit("", self)
        self._translationFileQLE.setReadOnly(True)
        self.layout().addWidget(self._translationFileQLE)

        self._grpBox = qt.QGroupBox("file type", self)
        self._grpBox.setLayout(qt.QVBoxLayout())
        self._grpBox.layout().setContentsMargins(0, 0, 0, 0)
        self._grpBox.layout().setSpacing(0)

        self._hdf5FileRB = qt.QRadioButton(
            TranslationMvtFileWidget.Mode.HDF5.value, self
        )
        self._grpBox.layout().addWidget(self._hdf5FileRB)
        self._textFileRB = qt.QRadioButton(
            TranslationMvtFileWidget.Mode.TEXT.value, self
        )
        self._grpBox.layout().addWidget(self._textFileRB)
        self.layout().addWidget(self._grpBox)

        self._selectButton = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectButton)

        # set up
        self._grpBox.setEnabled(False)
        self._translationFileQLE.setEnabled(False)
        self._selectButton.setEnabled(False)
        self._textFileRB.setChecked(True)

        # connect signal / slot
        self._selectButton.released.connect(self._selectCallback)
        self._checkBox.toggled.connect(self._toggleSelection)

    def _selectCallback(self, *args, **kwargs):
        if self.getSelectionMode() is self.Mode.HDF5:
            file_or_url = self._selectHDF5()
        elif self.getSelectionMode() is self.Mode.TEXT:
            file_or_url = self._selectTextFile()
        else:
            raise ValueError("")
        if file_or_url is not None:
            self.setFile(file_or_url)

    def _selectHDF5(self):
        dialog = DataFileDialog()
        dialog.setFilterMode(DataFileDialog.FilterMode.ExistingDataset)

        if not dialog.exec():
            dialog.close()
            return
        else:
            return dialog.selectedUrl()

    def _selectTextFile(self):  # pragma: no cover
        dialog = qt.QFileDialog(self)
        dialog.setFileMode(qt.QFileDialog.ExistingFile)

        if not dialog.exec():
            dialog.close()
            return
        if len(dialog.selectedFiles()) > 0:
            return dialog.selectedFiles()[0]

    def isChecked(self):
        return self._checkBox.isChecked()

    def setChecked(self, checked):
        self._checkBox.setChecked(checked)

    def getSelectionMode(self):
        if self._hdf5FileRB.isChecked():
            return self.Mode.HDF5
        else:
            return self.Mode.TEXT

    def setFile(self, file_):
        if file_ in (None, ""):
            self.setChecked(False)
        else:
            self.setChecked(True)
            self._translationFileQLE.setText(file_)
            self.fileChanged.emit()

    def getFile(self):
        if self.isChecked():
            return self._translationFileQLE.text()
        else:
            return None

    def _toggleSelection(self):
        self._translationFileQLE.setEnabled(self._checkBox.isChecked())
        self._grpBox.setEnabled(self._checkBox.isChecked())
        self._selectButton.setEnabled(self._checkBox.isChecked())


class AnglesFileWidget(qt.QWidget):
    """widget to retrieve the text file for angles to provide to nabu"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setLayout(qt.QHBoxLayout())
        self._qle = qt.QLineEdit("", self)
        self.layout().addWidget(self._qle)
        self._selectPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectPB)

        # connect signal / slot
        self._selectPB.released.connect(self._selectFile)

    def getFile(self) -> str:
        return self._qle.text().replace(" ", "")

    def setFile(self, file_path):
        self._qle.setText(file_path)

    def _selectFile(self) -> str:  # pragma: no cover
        dialog = qt.QFileDialog()
        dialog.setFileMode(qt.QFileDialog.ExistingFile)
        dialog.setNameFilters(
            [
                "Text file (*.txt)",
                "Any file (*)",
            ]
        )

        if not dialog.exec():
            dialog.close()
            return
        elif len(dialog.selectedFiles()) == 0:
            return
        else:
            file_path = dialog.selectedFiles()[0]
            self._qle.setText(file_path)


class _NabuReconstructionConfig(qt.QWidget, _NabuStageConfigBase):
    """
    Widget to define the configuration of nabu reconstruction processing and dataset configuration.
    At the gui side the "dataset" section as no real reason to be on its own. So we melt the two there.
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent, stage=_NabuStages.PRE)
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.PRE)
        self.setLayout(qt.QGridLayout())

        self.__optimizationIteAlgo = "chambolle-pock"

        # slices to be reconstructed online
        self._slicesWidget = SliceGroupBox(parent=self)
        self.layout().addWidget(self._slicesWidget, 0, 0, 1, 2)
        # ignore listener of the mouse for the slice widget, can
        # come with an issue as we are on a scroll area
        self._slicesWidget.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        # axis
        self._axisLabel = qt.QLabel("reconstruction plane", self)
        self._axisLabel.setToolTip("Over which axis the slice must be picked")
        self.layout().addWidget(self._axisLabel)
        self._axisQCB = QComboBoxIgnoreWheel(self)
        axis_tooltips = {
            NabuPlane.YZ.value: "along axis x (aka axis 2 - expected to be slow)",
            NabuPlane.XZ.value: "along axis y (aka axis 1 - expected to be slow)",
            NabuPlane.XY.value: "along axis Z (aka axis 0 - fastest)",
        }
        for item, tooltip in axis_tooltips.items():
            self._axisQCB.addItem(item)
            self._axisQCB.setItemData(
                self._axisQCB.findText(item),
                tooltip,
                qt.Qt.ToolTipRole,
            )
        self.layout().addWidget(self._axisQCB, 1, 1, 1, 1)

        # method
        self._methodLabel = qt.QLabel("method", self)
        self.layout().addWidget(self._methodLabel, 2, 0, 1, 1)
        self._methodQCB = QComboBoxIgnoreWheel(parent=self)
        for method in _NabuReconstructionMethods:
            self._methodQCB.addItem(method.value)
        self.layout().addWidget(self._methodQCB, 2, 1, 1, 1)
        self.registerWidget(self._methodLabel, "required")
        self.registerWidget(self._methodQCB, "required")

        self._methodWarningLabel = qt.QLabel(
            f"\tWARNING: \n\t1.' {_NabuReconstructionMethods.MLEM.value}' can be EXTREMELY SLOW on transmission\n\tdata and may produce erroneous results.\n\t2.MLEM should only be used with XRFCT data."
        )
        self._methodWarningLabel.setStyleSheet("color: red")
        self._methodWarningLabel.setVisible(False)
        self.layout().addWidget(self._methodWarningLabel, 3, 0, 1, 2)

        # angle_offset
        self._labelOffsetLabel = qt.QLabel("angle offset (in degree)", self)
        self.layout().addWidget(self._labelOffsetLabel, 4, 0, 1, 1)
        self._angleOffsetQDSB = QDoubleSpinBoxIgnoreWheel(self)
        self._angleOffsetQDSB.setMaximum(-180)
        self._angleOffsetQDSB.setMaximum(180)
        self.layout().addWidget(self._angleOffsetQDSB, 4, 1, 1, 1)
        self.registerWidget(self._labelOffsetLabel, "advanced")
        self.registerWidget(self._angleOffsetQDSB, "advanced")

        # fbp filter type
        self._fbpFilterCB = qt.QCheckBox("fbp filter", self)
        self.layout().addWidget(self._fbpFilterCB, 5, 0, 1, 1)
        self._fbpFilterType = QComboBoxIgnoreWheel(self)
        for filter_type in _NabuFBPFilterType:
            self._fbpFilterType.addItem(filter_type.value)
        self.layout().addWidget(self._fbpFilterType, 5, 1, 1, 1)
        self.registerWidget(self._fbpFilterCB, "advanced")
        self.registerWidget(self._fbpFilterType, "advanced")

        # padding type
        self._paddingTypeLabel = qt.QLabel("padding type", self)
        self.layout().addWidget(self._paddingTypeLabel, 6, 0, 1, 1)
        self._paddingType = QComboBoxIgnoreWheel(self)
        for fbp_padding_type in _NabuPaddingType:
            self._paddingType.addItem(fbp_padding_type.value)
        self.layout().addWidget(self._paddingType, 6, 1, 1, 1)
        self.registerWidget(self._paddingTypeLabel, "optional")
        self.registerWidget(self._paddingType, "optional")

        # sub region
        self._subRegionSelector = _NabuReconstructionSubRegion(parent=self)
        self.layout().addWidget(self._subRegionSelector, 8, 0, 1, 2)

        # iterations
        self._iterationsLabel = qt.QLabel("iterations", self)
        self.layout().addWidget(self._iterationsLabel, 9, 0, 1, 1)
        self._iterationSB = qt.QSpinBox(parent=self)
        self.layout().addWidget(self._iterationSB, 9, 1, 1, 1)
        self._iterationSB.setMinimum(1)
        self._iterationSB.setMaximum(9999)
        # not supported for now so hidden
        self._iterationsLabel.hide()
        self._iterationSB.hide()

        # binning - subsampling
        self._binSubSamplingGB = _BinSubSampling(
            "binning and sub-sampling", parent=self
        )
        self.layout().addWidget(self._binSubSamplingGB, 10, 0, 1, 2)

        # optimization algorithm:
        # set has default value for now, because has only one at the moment

        # weight total variation
        self._tvLabel = qt.QLabel("total variation weight", self)
        self.layout().addWidget(self._tvLabel, 11, 0, 1, 1)
        self._totalVariationWeight = qt.QDoubleSpinBox(self)
        self._totalVariationWeight.setMinimum(0.0)
        self._totalVariationWeight.setMaximum(1.0)
        self._totalVariationWeight.setDecimals(4)
        self._totalVariationWeight.setSingleStep(0.002)
        self.layout().addWidget(self._totalVariationWeight, 10, 1, 1, 1)
        # not supported for now so hidden
        self._tvLabel.hide()
        self._totalVariationWeight.hide()

        # preconditioning filter
        self._preconditioningFilter = qt.QCheckBox("preconditioning_filter", self)
        self._preconditioningFilter.setToolTip(
            'Whether to enable "filter ' 'preconditioning" for iterative' " methods"
        )
        self.layout().addWidget(self._preconditioningFilter, 11, 0, 1, 2)
        # not supported for now so hidden
        self._preconditioningFilter.hide()

        # positivity constraint
        self._positivityConstraintCB = qt.QCheckBox("positivity constraint", self)
        self._positivityConstraintCB.setToolTip(
            "Whether to enforce a " "positivity constraint in the " "reconstruction."
        )
        self.layout().addWidget(self._positivityConstraintCB, 12, 0, 1, 2)
        # not supported for now so hidden
        self._positivityConstraintCB.hide()

        # clip_outer_circle option
        self._clipOuterCircleCB = qt.QCheckBox("clip outer circle", self)
        self._clipOuterCircleCB.setToolTip(
            "Whether to set to zero voxels falling outside of the reconstruction region"
        )
        self.layout().addWidget(self._clipOuterCircleCB, 13, 0, 1, 2)
        self.registerWidget(self._clipOuterCircleCB, "optional")

        # centered axis option
        self._centeredAxisCB = qt.QCheckBox("centered axis", self)
        self._centeredAxisCB.setToolTip("")
        self.layout().addWidget(self._centeredAxisCB, 14, 0, 1, 2)
        self.registerWidget(self._centeredAxisCB, "optional")

        # translation movement file
        self._transMvtFileLabel = qt.QLabel("translation movement file", self)
        self.layout().addWidget(self._transMvtFileLabel, 22, 0, 1, 1)
        self._transMvtFileWidget = TranslationMvtFileWidget(self)
        self.layout().addWidget(self._transMvtFileWidget, 22, 1, 1, 1)
        self.registerWidget(self._transMvtFileLabel, "advanced")
        self.registerWidget(self._transMvtFileWidget, "advanced")
        translation_movement_tooltip = """
        A file where each line describes the horizontal and vertical translations of the sample (or detector).
        The order is 'horizontal, vertical'
        It can be created from a numpy array saved with 'numpy.savetxt'"""
        self._transMvtFileLabel.setToolTip(translation_movement_tooltip)
        self._transMvtFileWidget.setToolTip(translation_movement_tooltip)

        # angle files (if the user want's to overwrite rotation angles)
        self._angleFileLabel = qt.QLabel("angles file", self)
        self.layout().addWidget(self._angleFileLabel, 23, 0, 1, 1)
        self._anglesFileWidget = AnglesFileWidget(self)
        self.layout().addWidget(self._anglesFileWidget, 23, 1, 1, 1)
        self.registerWidget(self._angleFileLabel, "advanced")
        self.registerWidget(self._anglesFileWidget, "advanced")

        # exclude projections: [A, B] (if user want's to skip projection from degree A to degree B (included))
        self._excludeProjectionsQCB = qt.QCheckBox("exclude proj angles", self)
        self.layout().addWidget(self._excludeProjectionsQCB, 24, 0, 1, 1)
        self._excludeProjectionsWidget = RangeWidget(self)
        self._excludeProjectionsWidget.setRange(0.0, 360.0)
        self._excludeProjectionsWidget.setSuffix(DEGREE_CHAR)
        self._excludeProjectionsWidget.setToolTip(
            "Projections with a rotation in [a, b] range will be ignored."
        )
        self.layout().addWidget(self._excludeProjectionsWidget, 24, 1, 1, 1)
        self.registerWidget(self._excludeProjectionsQCB, "advanced")
        self.registerWidget(self._excludeProjectionsWidget, "advanced")

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 200, 1, 1, 1)

        # set up
        self.setNabuPlane("XY")
        self._fbpFilterCB.setChecked(True)
        fbp_item = self._methodQCB.findText(_NabuReconstructionMethods.FBP.value)
        self._methodQCB.setCurrentIndex(fbp_item)
        self._angleOffsetQDSB.setValue(0)
        ramlak_item = self._fbpFilterType.findText(_NabuFBPFilterType.RAMLAK.value)
        self._fbpFilterType.setCurrentIndex(ramlak_item)
        padding_type_item = self._paddingType.findText(_NabuPaddingType.ZEROS.value)
        self._fbpFilterType.setCurrentIndex(padding_type_item)
        self._iterationSB.setValue(200)
        self._totalVariationWeight.setValue(1.0e-2)
        self._preconditioningFilter.setChecked(True)
        self._positivityConstraintCB.setChecked(True)
        self._clipOuterCircleCB.setChecked(False)
        self._centeredAxisCB.setChecked(False)
        self._excludeProjectionsWidget.setEnabled(False)

        # connect signal / slot
        self._axisQCB.currentIndexChanged.connect(self._slicesChanged)
        self._methodQCB.currentIndexChanged.connect(self._methodChanged)
        self._angleOffsetQDSB.editingFinished.connect(self._angleOffsetChanged)
        self._fbpFilterCB.toggled.connect(self._FBPFilterTypeChanged)
        self._fbpFilterType.currentIndexChanged.connect(self._FBPFilterTypeChanged)
        self._paddingType.currentTextChanged.connect(self._paddingTypeChanged)
        self._subRegionSelector.sigConfChanged.connect(self._signalConfChanged)
        self._iterationSB.valueChanged.connect(self._nbIterationChanged)
        self._totalVariationWeight.valueChanged.connect(self._weightTvChanged)
        self._preconditioningFilter.toggled.connect(self._preconditionningFilterChanged)
        self._positivityConstraintCB.toggled.connect(self._positivityConstraintChanged)
        self._transMvtFileWidget.fileChanged.connect(self._mvtFileChanged)
        self._slicesWidget.sigSlicesChanged.connect(self._slicesChanged)
        self._binSubSamplingGB.binningChanged.connect(self._binningChanged)
        self._anglesFileWidget._qle.textChanged.connect(self._anglesFilechanged)
        self._clipOuterCircleCB.toggled.connect(self._clipOuterCircleChanged)
        self._centeredAxisCB.toggled.connect(self._centeredAxisChanged)
        self._excludeProjectionsQCB.toggled.connect(self._excludeProjectionsChanged)
        self._excludeProjectionsQCB.toggled.connect(
            self._excludeProjectionsWidget.setEnabled
        )
        self._excludeProjectionsWidget.sigChanged.connect(
            self._excludeProjectionsChanged
        )

    def getSlices(self):
        return self._slicesWidget.getSlices()

    def setSlices(self, slices):
        self._slicesWidget.setSlices(slices=slices)

    def hideSlicesInterface(self):
        self._slicesWidget.hide()

    def setConfigurationLevel(self, level):
        _NabuStageConfigBase.setConfigurationLevel(self, level)
        self._subRegionSelector.setConfigurationLevel(level=level)

    def _slicesChanged(self, *args, **kwargs):
        self._signalConfChanged("tomwer_slices")

    def _methodChanged(self, index):  # *args, **kwargs):
        self._signalConfChanged("method")
        selected_method = self.getMethod()
        self._methodWarningLabel.setVisible(
            selected_method == _NabuReconstructionMethods.MLEM
        )

    def _angleOffsetChanged(self, *args, **kwargs):
        self._signalConfChanged("angle_offset")

    def _FBPFilterTypeChanged(self, *args, **kwargs):
        self._signalConfChanged("fbp_filter_type")

    def _paddingTypeChanged(self, *args, **kwargs):
        self._signalConfChanged("padding_type")

    def _nbIterationChanged(self, *args, **kwargs):
        self._signalConfChanged("iterations")

    def _weightTvChanged(self, *args, **kwargs):
        self._signalConfChanged("weight_tv")

    def _preconditionningFilterChanged(self, *args, **kwargs):
        self._signalConfChanged("preconditioning_filter")

    def _positivityConstraintChanged(self, *args, **kwargs):
        self._signalConfChanged("positivity_constraint")

    def _mvtFileChanged(self, *args, **kwargs):
        self._signalConfChanged("translation_movements_file")

    def _clipOuterCircleChanged(self, *args, **kwargs):
        self._signalConfChanged("clip_outer_circle")

    def _centeredAxisChanged(self, *args, **kwargs):
        self._signalConfChanged("centered_axis")

    def _binningChanged(self, *args, **kwargs):
        self._signalConfChanged("binning")
        self._signalConfChanged("binning_z")

    def _anglesFilechanged(self, *args, **kwargs):
        self._signalConfChanged("angles_file")

    def _excludeProjectionsChanged(self):
        self._signalConfChanged("exclude_projections")

    def setScan(self, scan):
        raise NotImplementedError()

    def getMethod(self) -> _NabuReconstructionMethods:
        return _NabuReconstructionMethods(self._methodQCB.currentText())

    def setMethod(self, method):
        method = _NabuReconstructionMethods(method)
        item_index = self._methodQCB.findText(method.value)
        self._methodQCB.setCurrentIndex(item_index)

    def getAngleOffset(self) -> float:
        return self._angleOffsetQDSB.value()

    def setAngleOffset(self, value: str | float):
        self._angleOffsetQDSB.setValue(float(value))

    def getFBPFilterType(self) -> _NabuFBPFilterType | None:
        if self._fbpFilterCB.isChecked():
            return _NabuFBPFilterType(self._fbpFilterType.currentText())
        else:
            return None

    def setFBPFilterType(self, filter_type):
        if type(filter_type) is str and filter_type.lower() == "none":
            filter_type = None
        if filter_type is None:
            self._fbpFilterCB.setChecked(False)
        else:
            self._fbpFilterCB.setChecked(True)
            filter_type = _NabuFBPFilterType(filter_type)
            filter_index = self._fbpFilterType.findText(filter_type.value)
            self._fbpFilterType.setCurrentIndex(filter_index)

    def getFBPPaddingType(self) -> _NabuPaddingType:
        return _NabuPaddingType(self._paddingType.currentText())

    def setFBPPaddingType(self, padding):
        padding = _NabuPaddingType(padding)
        padding_index = self._paddingType.findText(padding.value)
        self._paddingType.setCurrentIndex(padding_index)

    def getNIterations(self):
        return self._iterationSB.value()

    def setNIterations(self, n_iterations):
        self._iterationSB.setValue(n_iterations)

    def getTotalVariationWeight(self) -> float:
        return self._totalVariationWeight.value()

    def setTotalVariationWeight(self, weight: float):
        self._totalVariationWeight.setValue(float(weight))

    def isPreconditioningFilterEnable(self):
        return self._preconditioningFilter.isChecked()

    def setPreconditioningFilterEnable(self, enable: bool | int):
        self._preconditioningFilter.setChecked(bool(enable))

    def isPositivityConstraintEnable(self):
        return self._positivityConstraintCB.isChecked()

    def setPositivityConstraintEnable(self, enable: bool | int):
        self._positivityConstraintCB.setChecked(bool(enable))

    def getTranslationMvtFile(self):
        return self._transMvtFileWidget.getFile()

    def setTranslationMvtFile(self, file_):
        self._transMvtFileWidget.setFile(file_)

    def getHorizontalBinning(self):
        return self._binSubSamplingGB.getHorizontalBinning()

    def setHorizontalBinning(self, binning):
        return self._binSubSamplingGB.setHorizontalBinning(binning=binning)

    def getVerticalBinning(self):
        return self._binSubSamplingGB.getVerticalBinning()

    def setVerticalBinning(self, binning):
        return self._binSubSamplingGB.setVerticalBinning(binning=binning)

    def getProjSubsampling(self):
        return self._binSubSamplingGB.getProjSubsampling()

    def setProjSubsampling(self, subsampling):
        return self._binSubSamplingGB.setProjSubsampling(subsampling=subsampling)

    def getAnglesFile(self) -> str:
        return self._anglesFileWidget.getFile()

    def setAnglesFile(self, angles_file: str):
        return self._anglesFileWidget.setFile(angles_file)

    def getClipOuterCircle(self) -> bool:
        return self._clipOuterCircleCB.isChecked()

    def setClipOuterCircle(self, checked: bool) -> None:
        self._clipOuterCircleCB.setChecked(checked)

    def getCenteredAxis(self) -> bool:
        return self._centeredAxisCB.isChecked()

    def setCenteredAxis(self, checked: bool):
        self._centeredAxisCB.setChecked(checked)

    def getNabuPlane(self) -> NabuPlane:
        """return over which axis we expect to do the reconstruction"""
        return NabuPlane.from_value(self._axisQCB.currentText())

    def setNabuPlane(self, axis: str | NabuPlane):
        axis = NabuPlane.from_value(axis)
        self._axisQCB.setCurrentText(axis.value)

    def getExcludeProjections(self) -> tuple:
        if self._excludeProjectionsQCB.isChecked():
            return self._excludeProjectionsWidget.getRange()
        else:
            return tuple()

    def setExcludeProjections(self, projections: tuple):
        if not isinstance(projections, tuple):
            raise TypeError(
                f"projections should be an instance of tuple. Got {type(projections)}"
            )
        if len(projections) == 0:
            self._excludeProjectionsQCB.setChecked(False)
        else:
            self._excludeProjectionsQCB.setChecked(True)
            self._excludeProjectionsWidget.setRange(*projections)

    @docstring(_NabuStageConfigBase)
    def getConfiguration(self) -> dict:
        fbp_filter_type = self.getFBPFilterType()
        if fbp_filter_type is None:
            fbp_filter_type = "none"
        else:
            fbp_filter_type = fbp_filter_type.value
        config = {
            "method": self.getMethod().value,
            "slice_plane": self.getNabuPlane().value,
            "angles_file": self.getAnglesFile(),
            "axis_correction_file": "",  # not managed for now
            "angle_offset": self.getAngleOffset(),
            "fbp_filter_type": fbp_filter_type,
            "padding_type": self.getFBPPaddingType().value,
            "iterations": self.getNIterations(),
            "optim_algorithm": self.__optimizationIteAlgo,
            "weight_tv": self.getTotalVariationWeight(),
            "preconditioning_filter": int(self.isPreconditioningFilterEnable()),
            "positivity_constraint": int(self.isPositivityConstraintEnable()),
            "rotation_axis_position": "",
            "translation_movements_file": self.getTranslationMvtFile() or "",
            "clip_outer_circle": int(self.getClipOuterCircle()),
            "centered_axis": int(self.getCenteredAxis()),
        }
        config.update(self._subRegionSelector.getConfiguration())
        return config

    def getDatasetConfiguration(self) -> dict:
        exclude_projections = self.getExcludeProjections()
        if len(exclude_projections) == 0:
            exclude_projections = ""
        else:
            exclude_projections = f"angular_range={str(list(exclude_projections))}"
        config = self._binSubSamplingGB.getConfiguration()
        config["exclude_projections"] = exclude_projections
        return config

    def setDatasetConfiguration(self, config):
        exclude_proj = config.pop("exclude_projections", None)
        if exclude_proj is not None:
            if isinstance(exclude_proj, str):
                exclude_proj = exclude_proj.replace("angular_range=", "")
            exclude_proj = convert_str_to_tuple(exclude_proj)
            self.setExcludeProjections(exclude_proj)
        return self._binSubSamplingGB.setConfiguration(config)

    @docstring(_NabuStageConfigBase)
    def setConfiguration(self, config):
        if "method" in config:
            self.setMethod(config["method"])
        if "angles_file" in config:
            self.setAnglesFile(config["angles_file"])
        if "angle_offset" in config:
            self.setAngleOffset(value=config["angle_offset"])
        if "fbp_filter_type" in config:
            self.setFBPFilterType(config["fbp_filter_type"])
        if "padding_type" in config:
            self.setFBPPaddingType(config["padding_type"])
        if "iterations" in config:
            self.setNIterations(int(config["iterations"]))
        if "optim_algorithm" in config:
            self.__optimizationIteAlgo = config["optim_algorithm"]
        if "weight_tv" in config:
            self.setTotalVariationWeight(weight=config["weight_tv"])
        if "preconditioning_filter" in config:
            self.setPreconditioningFilterEnable(int(config["preconditioning_filter"]))
        if "positivity_constraint" in config:
            self.setPositivityConstraintEnable(int(config["positivity_constraint"]))
        if "translation_movements_file" in config:
            self.setTranslationMvtFile(config["translation_movements_file"])
        if "clip_outer_circle" in config:
            self.setClipOuterCircle(bool(config["clip_outer_circle"]))
        if "centered_axis" in config:
            self.setCenteredAxis(bool(config["centered_axis"]))
        if "slice_plane" in config:
            self.setNabuPlane(config["slice_plane"])
        self._subRegionSelector.setConfiguration(config=config)

    def _signalConfChanged(self, param):
        self.sigConfChanged.emit(param)


class _SubRegionEditor(qt.QObject):
    sigConfChanged = qt.Signal(str)
    """Signal emitted each type a parameter is edited"""

    def __init__(
        self, parent, layout, layout_row: int, name: str, min_param: str, max_param: str
    ):
        assert type(layout_row) is int
        qt.QObject.__init__(self)
        self._layout = layout
        self.__minParam = min_param
        self.__maxParam = max_param

        validator = qt.QIntValidator()
        validator.setBottom(0)

        self._subRegionLabel = qt.QLabel(name, parent)
        self.layout().addWidget(self._subRegionLabel, layout_row, 0, 1, 1)

        # min
        self._minCB = qt.QCheckBox("min", parent)
        self.layout().addWidget(self._minCB, layout_row, 1, 1, 1)
        self._minQLE = qt.QLineEdit("0", parent)
        self._minQLE.setValidator(validator)
        self.layout().addWidget(self._minQLE, layout_row, 2, 1, 1)

        # max
        self._maxCB = qt.QCheckBox("max", parent)
        self.layout().addWidget(self._maxCB, layout_row, 3, 1, 1)
        self._maxQLE = qt.QLineEdit("0", parent)
        self._maxQLE.setValidator(validator)
        self.layout().addWidget(self._maxQLE, layout_row, 4, 1, 1)

        # spacer for style
        self._spacer = qt.QWidget(parent)
        self._spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._spacer, layout_row, 5, 1, 1)

        # set up
        self._minCB.setChecked(False)
        self._minQLE.setEnabled(False)
        self._maxCB.setChecked(False)
        self._maxQLE.setEnabled(False)

        # connect signal / slot
        self._minCB.toggled.connect(self._minQLE.setEnabled)
        self._maxCB.toggled.connect(self._maxQLE.setEnabled)
        self._minCB.toggled.connect(
            functools.partial(self._signalConfChanged, self.__minParam)
        )
        self._maxCB.toggled.connect(
            functools.partial(self._signalConfChanged, self.__maxParam)
        )
        self._minQLE.editingFinished.connect(
            functools.partial(self._signalConfChanged, self.__minParam)
        )
        self._maxQLE.editingFinished.connect(
            functools.partial(self._signalConfChanged, self.__maxParam)
        )

    def layout(self):
        return self._layout

    def getSubRegionMin(self) -> int | None:
        """

        :return: None if region is unbounded else the value of the bound
        """
        if self._minCB.isChecked():
            return int(self._minQLE.text())
        else:
            return None

    def getSubRegionMax(self) -> int | None:
        """

        :return: None if region is unbounded else the value of the bound
        """
        if self._maxCB.isChecked():
            return int(self._maxQLE.text())
        else:
            return None

    def setSubRegionMin(self, sub_region_min: int | None) -> None:
        """

        :param min: if min is None or -1 wr will expand it to - infinity
        """
        if sub_region_min in (-1, 0):
            sub_region_min = None
        if sub_region_min is None:
            self._minCB.setChecked(False)
        else:
            self._minCB.setChecked(True)
            self._minQLE.setText(str(sub_region_min))

    def setSubRegionMax(self, sub_region_max) -> None:
        """

        :param max: if max is None or -1 wr will expand it to infinity
        """
        if type(sub_region_max) is str:
            sub_region_max = int(sub_region_max)
        if sub_region_max == -1:
            sub_region_max = None
        if sub_region_max is None:
            self._maxCB.setChecked(False)
        else:
            self._maxCB.setChecked(True)
            self._maxQLE.setText(str(sub_region_max))

    def getSubRegion(self) -> tuple:
        """

        :return: min, max
        """
        return self.getSubRegionMin(), self.getSubRegionMax()

    def setSubRegion(
        self,
        sub_region_min: int | None,
        sub_region_max: int | None,
    ):
        self.setSubRegionMin(sub_region_min)
        self.setSubRegionMax(sub_region_max)

    def _signalConfChanged(self, param):
        self.sigConfChanged.emit(param)

    def setVisible(self, visible):
        for widget in (
            self._subRegionLabel,
            self._minCB,
            self._minQLE,
            self._maxCB,
            self._maxQLE,
            self._spacer,
        ):
            widget.setVisible(visible)


class _NabuReconstructionSubRegion(qt.QGroupBox, _NabuStageConfigBase):
    """Widget to select a sub region to reconstruct"""

    sigConfChanged = qt.Signal(str)
    """Signal emitted each type a parameter is edited"""

    def __init__(self, parent):
        qt.QGroupBox.__init__(self, parent, stage=_NabuStages.PROC)
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.PROC)
        self.setTitle("sub region")

        self.setLayout(qt.QGridLayout())

        self._xSubRegion = _SubRegionEditor(
            parent=self,
            layout=self.layout(),
            layout_row=0,
            name="x",
            min_param="start_x",
            max_param="end_x",
        )
        self.registerWidget(self._xSubRegion, "optional")

        self._ySubRegion = _SubRegionEditor(
            parent=self,
            layout=self.layout(),
            layout_row=1,
            name="y",
            min_param="start_y",
            max_param="end_y",
        )
        self.registerWidget(self._ySubRegion, "optional")

        self._zSubRegion = _SubRegionEditor(
            parent=self,
            layout=self.layout(),
            layout_row=2,
            name="z",
            min_param="start_z",
            max_param="end_z",
        )
        self.registerWidget(self._zSubRegion, "optional")

        # set up

        # connect signal / slot
        self._xSubRegion.sigConfChanged.connect(self._signalConfChanged)
        self._ySubRegion.sigConfChanged.connect(self._signalConfChanged)
        self._zSubRegion.sigConfChanged.connect(self._signalConfChanged)

    def getConfiguration(self) -> dict:
        return {
            "start_x": self._xSubRegion.getSubRegionMin() or 0,
            "end_x": self._xSubRegion.getSubRegionMax() or -1,
            "start_y": self._ySubRegion.getSubRegionMin() or 0,
            "end_y": self._ySubRegion.getSubRegionMax() or -1,
            "start_z": self._zSubRegion.getSubRegionMin() or 0,
            "end_z": self._zSubRegion.getSubRegionMax() or -1,
        }

    def setConfiguration(self, config):
        if "start_x" in config:
            self._xSubRegion.setSubRegionMin(int(config["start_x"]))
        if "end_x" in config:
            self._xSubRegion.setSubRegionMax(int(config["end_x"]))
        if "start_y" in config:
            self._ySubRegion.setSubRegionMin(int(config["start_y"]))
        if "end_y" in config:
            self._ySubRegion.setSubRegionMax(int(config["end_y"]))
        if "start_z" in config:
            self._zSubRegion.setSubRegionMin(int(config["start_z"]))
        if "end_z" in config:
            self._zSubRegion.setSubRegionMax(int(config["end_z"]))

    def _signalConfChanged(self, param):
        self.sigConfChanged.emit(param)


class _BinSubSampling(qt.QGroupBox):
    binningChanged = qt.Signal()
    """signal emitted when binning change"""

    def __init__(self, text, parent):
        qt.QGroupBox.__init__(self, text)
        self.setLayout(qt.QFormLayout())
        # binning
        self._binningSB = QSpinBoxIgnoreWheel(self)
        self._binningSB.setMinimum(1)
        self._binningSB.setMaximum(3)
        self.layout().addRow("binning", self._binningSB)
        self._binningSB.setToolTip(
            "Binning factor in the horizontal dimension when reading the data. \nThe final slices dimensions will be divided by this factor."
        )
        # z binning
        self._zBinningSB = QSpinBoxIgnoreWheel(self)
        self._zBinningSB.setMinimum(1)
        self._zBinningSB.setMaximum(100)
        self.layout().addRow("vertical binning", self._zBinningSB)
        self._zBinningSB.setToolTip(
            "Binning factor in the vertical dimension when reading the data. \nThis results in a lesser number of reconstructed slices."
        )
        # projection sub-sampling
        self._projSubsamplingSB = QSpinBoxIgnoreWheel(self)
        self._projSubsamplingSB.setMinimum(1)
        self._projSubsamplingSB.setMaximum(100)
        self.layout().addRow("projection sub-sampling", self._projSubsamplingSB)

        # connect signal / slot
        self._zBinningSB.valueChanged.connect(self._valueUpdated)
        self._binningSB.valueChanged.connect(self._valueUpdated)

    def getHorizontalBinning(self) -> int:
        return self._binningSB.value()

    def setHorizontalBinning(self, binning: int):
        return self._binningSB.setValue(int(binning))

    def getVerticalBinning(self) -> int:
        return self._zBinningSB.value()

    def setVerticalBinning(self, binning: int):
        return self._zBinningSB.setValue(int(binning))

    def getProjSubsampling(self) -> int:
        return self._projSubsamplingSB.value()

    def setProjSubsampling(self, subsampling: int):
        return self._projSubsamplingSB.setValue(int(subsampling))

    def getConfiguration(self) -> dict:
        return {
            "binning": self.getHorizontalBinning(),
            "binning_z": self.getVerticalBinning(),
            "projections_subsampling": self.getProjSubsampling(),
        }

    def setConfiguration(self, config: dict):
        if "binning" in config:
            self.setHorizontalBinning(config["binning"])
        if "binning_z" in config:
            self.setVerticalBinning(config["binning_z"])
        if "projections_subsampling" in config:
            self.setProjSubsampling(subsampling=config["projections_subsampling"])

    def _valueUpdated(self, *args, **kwargs):
        self.binningChanged.emit()

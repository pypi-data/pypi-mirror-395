from __future__ import annotations

import logging
import weakref
import pint
import numpy
from silx.gui import qt

from nxtomo.nxobject.nxdetector import ImageKey, FOV
from nxtomo.paths.nxtomo import LATEST_VERSION as _LATEST_NXTOMO_VERSION

from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorKeys
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.utils.scandescription import ScanNameLabelAndShape
from tomwer.gui.utils.unitsystem import MetricEntry
from tomwer.gui.edit.nxtomowarmer import NXtomoProxyWarmer

_logger = logging.getLogger(__name__)

_ureg = pint.get_application_registry()


class NXtomoEditorDialog(qt.QDialog):
    """
    Dialog embedding instances of NXtomoEditor and NXtomoProxyWarmer
    """

    def __init__(self, parent=None, hide_lockers=True) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self.mainWidget = NXtomoEditor(parent=self, hide_lockers=hide_lockers)
        self.layout().addWidget(self.mainWidget)
        self._warmer = NXtomoProxyWarmer(parent=self)
        self.layout().addWidget(self._warmer)

        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.button(qt.QDialogButtonBox.Ok).setText("validate")
        self.layout().addWidget(self._buttons)

    # expose API
    def setScan(self, scan: NXtomoScan) -> None:
        self.mainWidget.setScan(scan)
        self._warmer.setScan(scan)

    def hasLockField(self) -> bool:
        return self.mainWidget.hasLockField()

    def getConfiguration(self) -> dict:
        return self.mainWidget.getConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self.mainWidget.setConfiguration(config)

    def getConfigurationForTask(self) -> dict:
        return self.mainWidget.getConfigurationForTask()


class NXtomoEditor(qt.QWidget):
    """
    Widget to edit a set of field from a NXtomo.
    The preliminary goal is to let the user define pixel / voxel position and x and z positions
    in order to simplify stitching down the line

    As energy and field of view was also often requested this part is also editable.

    Each field contains a widget to define it values and a LockButton. The LockButton can be used to automate the
    processing.

    When the scan to edit is set each field widget will be updated **at the condition** the field is not locked.
    Else existing value will be kept.
    """

    sigEditingFinished = qt.Signal()
    """emit when edition is finished"""

    def __init__(self, parent=None, hide_lockers=True):
        super().__init__(parent)
        self._editableWidgets = []
        self._lockerPBs = []
        # list of all lockers
        self._scan = None
        self.setLayout(qt.QVBoxLayout())
        self._scanInfoQLE = ScanNameLabelAndShape(parent=self)
        self.layout().addWidget(self._scanInfoQLE)

        # nxtomo tree
        self._tree = qt.QTreeWidget(self)
        if hide_lockers:
            self._tree.setColumnCount(2)
            self._tree.setHeaderLabels(("entry", "value"))
        else:
            self._tree.setColumnCount(3)
            self._tree.setHeaderLabels(("entry", "value", "lockers"))
            self._tree.header().setStretchLastSection(False)
            self._tree.setColumnWidth(2, 20)
            self._tree.header().setSectionResizeMode(1, qt.QHeaderView.Stretch)
        self.layout().addWidget(self._tree)

        # 1: instrument
        self._instrumentQTWI = qt.QTreeWidgetItem(self._tree)
        self._instrumentQTWI.setText(0, "instrument")
        # handle energy
        self._beamQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._beamQTWI.setText(0, "beam")
        self._energyQTWI = qt.QTreeWidgetItem(self._beamQTWI)
        self._energyQTWI.setText(0, "energy (keV)")
        self._energyEntry = EnergyEntry("", self)
        self._energyEntry.setPlaceholderText("energy in kev")
        self._tree.setItemWidget(self._energyQTWI, 1, self._energyEntry)
        self._editableWidgets.append(self._energyEntry)
        self._energyLockerLB = PadlockButton(self)
        self._energyLockerLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._energyLockerLB)
        self._tree.setItemWidget(self._energyQTWI, 2, self._energyLockerLB)

        # 1.1 detector
        self._detectorQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._detectorQTWI.setText(0, "detector")
        ## pixel size
        self._xDetectorPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._xDetectorPixelSizeQTWI.setText(0, "x pixel size")
        self._xDetectorPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._xDetectorPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._xDetectorPixelSizeQTWI, 1, self._xDetectorPixelSizeMetricEntry
        )
        self._editableWidgets.append(self._xDetectorPixelSizeMetricEntry)
        self._xDetectorPixelSizeLB = PadlockButton(self)
        self._xDetectorPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xDetectorPixelSizeLB)
        self._tree.setItemWidget(
            self._xDetectorPixelSizeQTWI, 2, self._xDetectorPixelSizeLB
        )

        self._yDetectorPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._yDetectorPixelSizeQTWI.setText(0, "y pixel size")
        self._yDetectorPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._yDetectorPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._yDetectorPixelSizeQTWI, 1, self._yDetectorPixelSizeMetricEntry
        )
        self._editableWidgets.append(self._yDetectorPixelSizeMetricEntry)
        self._yDetectorPixelSizeLB = PadlockButton(self)
        self._yDetectorPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._yDetectorPixelSizeLB)
        self._tree.setItemWidget(
            self._yDetectorPixelSizeQTWI, 2, self._yDetectorPixelSizeLB
        )

        ## sample - distance
        self._sampleDetectorDistanceQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._sampleDetectorDistanceQTWI.setText(0, "sample-detector distance")
        self._sampleDetectorDistanceMetricEntry = MetricEntry("", parent=self)
        self._sampleDetectorDistanceMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._sampleDetectorDistanceQTWI, 1, self._sampleDetectorDistanceMetricEntry
        )
        self._editableWidgets.append(self._sampleDetectorDistanceMetricEntry)
        self._sampleDetectorDistanceLB = PadlockButton(self)
        self._sampleDetectorDistanceLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._sampleDetectorDistanceLB)
        self._tree.setItemWidget(
            self._sampleDetectorDistanceQTWI, 2, self._sampleDetectorDistanceLB
        )

        ## field of view
        self._fieldOfViewQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._fieldOfViewQTWI.setText(0, "field of view")
        self._fieldOfViewCB = qt.QComboBox(self)
        for FOV_item in FOV:
            self._fieldOfViewCB.addItem(FOV_item.value)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 1, self._fieldOfViewCB)
        self._editableWidgets.append(self._fieldOfViewCB)
        self._fieldOfViewLB = PadlockButton(self)
        self._fieldOfViewLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._fieldOfViewLB)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 2, self._fieldOfViewLB)

        ## x flipped
        self._lrFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._lrFlippedQTWI.setText(0, "lr flipped")
        self._lrFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._lrFlippedQTWI, 1, self._lrFlippedCB)
        self._editableWidgets.append(self._lrFlippedCB)
        self._lrFlippedLB = PadlockButton(self)
        self._lrFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._lrFlippedLB)
        self._tree.setItemWidget(self._lrFlippedQTWI, 2, self._lrFlippedLB)
        ## y flipped
        self._udFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._udFlippedQTWI.setText(0, "ud flipped")
        self._udFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._udFlippedQTWI, 1, self._udFlippedCB)
        self._editableWidgets.append(self._udFlippedCB)
        self._udFlippedLB = PadlockButton(self)
        self._udFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._udFlippedLB)
        self._tree.setItemWidget(self._udFlippedQTWI, 2, self._udFlippedLB)
        # source
        self._sourceQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._sourceQTWI.setText(0, "source")
        ## source - sample
        self._sampleSourceDistanceQTWI = qt.QTreeWidgetItem(self._sourceQTWI)
        self._sampleSourceDistanceQTWI.setText(0, "sample-source distance")
        self._sampleSourceDistanceMetricEntry = MetricEntry("", parent=self)
        self._sampleSourceDistanceMetricEntry.setToolTip(
            "sample-source distance. Expected to be negative"
        )
        self._sampleSourceDistanceMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._sampleSourceDistanceQTWI, 1, self._sampleSourceDistanceMetricEntry
        )
        self._editableWidgets.append(self._sampleSourceDistanceMetricEntry)
        self._sampleSourceDistanceLB = PadlockButton(self)
        self._sampleSourceDistanceLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._sampleSourceDistanceLB)
        self._tree.setItemWidget(
            self._sampleSourceDistanceQTWI, 2, self._sampleSourceDistanceLB
        )
        # 2: sample
        self._sampleQTWI = qt.QTreeWidgetItem(self._tree)
        self._sampleQTWI.setText(0, "sample")
        # ## pixel size
        self._xSamplePixelSizeQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._xSamplePixelSizeQTWI.setText(0, "x pixel size")
        self._xSamplePixelSizeMetricEntry = MetricEntry("", parent=self)
        self._xSamplePixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._xSamplePixelSizeQTWI, 1, self._xSamplePixelSizeMetricEntry
        )
        self._editableWidgets.append(self._xSamplePixelSizeMetricEntry)
        self._xSamplePixelSizeLB = PadlockButton(self)
        self._xSamplePixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xSamplePixelSizeLB)
        self._tree.setItemWidget(
            self._xSamplePixelSizeQTWI, 2, self._xSamplePixelSizeLB
        )

        self._ySamplePixelSizeQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._ySamplePixelSizeQTWI.setText(0, "y pixel size")
        self._ySamplePixelSizeMetricEntry = MetricEntry("", parent=self)
        self._ySamplePixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._ySamplePixelSizeQTWI, 1, self._ySamplePixelSizeMetricEntry
        )
        self._editableWidgets.append(self._ySamplePixelSizeMetricEntry)
        self._ySamplePixelSizeLB = PadlockButton(self)
        self._ySamplePixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._ySamplePixelSizeLB)
        self._tree.setItemWidget(
            self._ySamplePixelSizeQTWI, 2, self._ySamplePixelSizeLB
        )

        ## propagation distance
        self._propagationDistanceQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._propagationDistanceQTWI.setText(0, "propagation distance")
        self._propagationDistanceMetricEntry = MetricEntry("", parent=self)
        self._propagationDistanceMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._propagationDistanceQTWI, 1, self._propagationDistanceMetricEntry
        )
        self._editableWidgets.append(self._propagationDistanceMetricEntry)
        self._propagationDistanceLB = PadlockButton(self)
        self._propagationDistanceLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._propagationDistanceLB)
        self._tree.setItemWidget(
            self._propagationDistanceQTWI, 2, self._propagationDistanceLB
        )

        ## x translation
        self._xTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._xTranslationQTWI.setText(0, "x translation")
        self._xTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._xTranslationQTWI, 1, self._xTranslationQLE)
        self._editableWidgets.append(self._xTranslationQLE)

        ## z translation
        self._zTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._zTranslationQTWI.setText(0, "z translation")
        self._zTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._zTranslationQTWI, 1, self._zTranslationQLE)
        self._editableWidgets.append(self._zTranslationQLE)

        # set up
        self._instrumentQTWI.setExpanded(True)
        self._sampleQTWI.setExpanded(True)
        self._beamQTWI.setExpanded(True)
        self._detectorQTWI.setExpanded(True)
        self.hideLockers(hide_lockers)

        # connect signal / slot
        self._energyEntry.editingFinished.connect(self._editingFinished)
        self._energyLockerLB.toggled.connect(self._editingFinished)
        self._xDetectorPixelSizeMetricEntry.editingFinished.connect(
            self._editingFinished
        )
        self._xDetectorPixelSizeLB.toggled.connect(self._editingFinished)
        self._yDetectorPixelSizeMetricEntry.editingFinished.connect(
            self._editingFinished
        )
        self._yDetectorPixelSizeLB.toggled.connect(self._editingFinished)
        self._xSamplePixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._xSamplePixelSizeLB.toggled.connect(self._editingFinished)
        self._ySamplePixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._ySamplePixelSizeLB.toggled.connect(self._editingFinished)
        self._sampleDetectorDistanceMetricEntry.editingFinished.connect(
            self._editingFinished
        )
        self._sampleDetectorDistanceLB.toggled.connect(self._editingFinished)
        self._propagationDistanceMetricEntry.editingFinished.connect(
            self._editingFinished
        )
        self._propagationDistanceLB.toggled.connect(self._editingFinished)
        self._fieldOfViewCB.currentIndexChanged.connect(self._editingFinished)
        self._fieldOfViewLB.toggled.connect(self._editingFinished)
        self._lrFlippedCB.toggled.connect(self._editingFinished)
        self._lrFlippedLB.toggled.connect(self._editingFinished)
        self._udFlippedCB.toggled.connect(self._editingFinished)
        self._udFlippedLB.toggled.connect(self._editingFinished)

    def update_tree(self) -> None:
        scan = self.getScan()
        if scan is not None:
            self._updateInstrument()
            self._updateSample()
            self._updateSource()
            self._tree.resizeColumnToContents(0)

            # update items according to NXtomo nexus version
            nexus_version = scan.nexus_version
            if nexus_version is None:
                nexus_version = _LATEST_NXTOMO_VERSION
            # handle nxtomo 1.4 version
            allow_source_sample_distance = bool(nexus_version >= 1.4)
            self._sampleSourceDistanceMetricEntry.setEnabled(
                allow_source_sample_distance
            )
            self._sampleSourceDistanceLB.setEnabled(allow_source_sample_distance)

            # handle nxtomo 1.5 version
            allow_sample_pixel_size_and_prop_distance = bool(nexus_version >= 1.5)
            self._xSamplePixelSizeMetricEntry.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )
            self._xSamplePixelSizeLB.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )
            self._ySamplePixelSizeMetricEntry.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )
            self._ySamplePixelSizeLB.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )
            self._propagationDistanceMetricEntry.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )
            self._propagationDistanceLB.setEnabled(
                allow_sample_pixel_size_and_prop_distance
            )

    def _updateInstrument(self) -> None:
        scan = self.getScan()
        if scan is None:
            return
        update_dict = {
            "energy": self._updateEnergy,
            "detector pixel size": self._updateDetectorPixelSize,
            "frame flips": self._updateFlipped,
            "field of view": self._updateFieldOfView,
            "sample-detector distance": self._updateSampleDetectorDistance,
        }
        if scan.nexus_version is None or scan.nexus_version >= 1.4:
            update_dict.update(
                {
                    "sample-source distance": self._updateSampleSourceDistance,
                }
            )
        if scan.nexus_version is None or scan.nexus_version >= 1.5:
            update_dict.update(
                {
                    "propagation distance": self._updatePropagationDistance,
                }
            )
        for name, fct in update_dict.items():
            try:
                fct(scan=scan)
            except Exception as e:
                _logger.error(f"Could not update {name}. Error is {e}")

    def _updateSample(self) -> None:
        scan = self.getScan()
        if scan is None:
            return

        update_dict = {
            "translations": self._updateTranslations,
        }
        if scan.nexus_version is None or scan.nexus_version >= 1.5:
            update_dict.update(
                {
                    "sample pixel size": self._updateSamplePixelSize,
                    "propagation distance": self._updatePropagationDistance,
                }
            )
        for name, fct in update_dict.items():
            try:
                fct(scan=scan)
            except Exception as e:
                _logger.error(f"Fail to update {name}. Error is {e}")

    def _updateSource(self) -> None:
        scan = self.getScan()
        if scan is None:
            return
        if scan.nexus_version is None or scan.nexus_version >= 1.4:
            try:
                self._updateSampleSourceDistance(scan=scan)
            except Exception as e:
                _logger.error(
                    f"Could not update sample - source distance. Error is {e}"
                )

    def _updateTranslations(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)

        # note: for now and in order to allow edition we expect to have at most a unique value. Will fail for helicoidal
        def reduce(values):
            if values is None:
                return None
            values = numpy.array(values)
            values = numpy.unique(
                values[scan.image_key_control == ImageKey.PROJECTION.value]
            )
            if values.size == 1:
                return values[0]
            elif values.size == 0:
                return None
            else:
                return f"{values[0]} ... {values[-1]}"

        x_translation = reduce(scan.x_translation)
        z_translation = reduce(scan.z_translation)
        self._xTranslationQLE.setValue(x_translation)
        self._zTranslationQLE.setValue(z_translation)

    def _updateFieldOfView(self, scan: NXtomoScan) -> None:
        if not self._fieldOfViewLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            idx = self._fieldOfViewCB.findText(FOV.from_value(scan.field_of_view).value)
            if idx > 0:
                self._fieldOfViewCB.setCurrentIndex(idx)

    def _updateFlipped(self, scan: NXtomoScan) -> None:
        flip_lr = scan.detector_is_lr_flip
        flip_ud = scan.detector_is_ud_flip

        if (not self._lrFlippedLB.isLocked()) and flip_lr is not None:
            self._lrFlippedCB.setChecked(flip_lr)
        if (not self._udFlippedLB.isLocked()) and flip_ud is not None:
            self._udFlippedCB.setChecked(flip_ud)

    def _updateSampleDetectorDistance(self, scan: NXtomoScan) -> None:
        if not self._sampleDetectorDistanceLB.isLocked():
            # if in 'auto' mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._sampleDetectorDistanceMetricEntry.setValue(
                scan.sample_detector_distance
            )

    def _updateSampleSourceDistance(self, scan: NXtomoScan) -> None:
        if not self._sampleSourceDistanceLB.isLocked():
            self._sampleSourceDistanceMetricEntry.setValue(scan.source_sample_distance)

    def _updatePropagationDistance(self, scan: NXtomoScan) -> None:
        if not self._propagationDistanceLB.isLocked():
            # if in 'auto' mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._propagationDistanceMetricEntry.setValue(scan.propagation_distance)

    def _updateEnergy(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)
        if not self._energyLockerLB.isLocked():
            # if in 'auto' mode: we want to overwrite the NXtomo existing value by the one of the GUI
            energy_in_kev: float | None = scan.energy
            if energy_in_kev is not None:
                # move from float to pint.Quantity
                assert not isinstance(energy_in_kev, pint.Quantity)
            self._energyEntry.setValue(energy_in_kev)

    def _updateDetectorPixelSize(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)
        if not self._xDetectorPixelSizeLB.isLocked():
            x_pixel_size = scan.detector_x_pixel_size
            self._xDetectorPixelSizeMetricEntry.setValue(x_pixel_size)
        if not self._yDetectorPixelSizeLB.isLocked():
            y_pixel_size = scan.detector_y_pixel_size
            self._yDetectorPixelSizeMetricEntry.setValue(y_pixel_size)

    def _updateSamplePixelSize(self, scan: NXtomoScan) -> None:
        if not self._xSamplePixelSizeLB.isLocked():
            # if in 'auto' mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._xSamplePixelSizeMetricEntry.setValue(
                scan.get_sample_pixel_size(which="x", fallback_to_det_pixel_size=False)
            )
        if not self._ySamplePixelSizeLB.isLocked():
            # if in 'auto' mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._ySamplePixelSizeMetricEntry.setValue(
                scan.get_sample_pixel_size(which="y", fallback_to_det_pixel_size=False)
            )

    def _editingFinished(self, *args, **kwargs):
        self.sigEditingFinished.emit()

    def hasLockField(self) -> bool:
        """return True if the widget has at least one lock field"""
        return True in [locker.isLocked() for locker in self._lockerPBs]

    def hideLockers(self, hide: bool) -> None:
        for locker in self._lockerPBs:
            locker.setVisible(not hide)

    def getEditableWidgets(self) -> tuple[qt.QWidget]:
        return tuple(self._editableWidgets)

    def setScan(self, scan: NXtomoScan | None) -> None:
        if scan is None:
            self._scan = scan
        elif not isinstance(scan, NXtomoScan):
            raise TypeError(
                f"{scan} is expected to be an instance of {NXtomoScan}. Not {type(scan)}"
            )
        else:
            self._scan = weakref.ref(scan)
        self._scanInfoQLE.setScan(scan)
        # scan will only be read and not kept
        self.update_tree()

    def getScan(self) -> NXtomoScan | None:
        if self._scan is None or self._scan() is None:
            return None
        else:
            return self._scan()

    def getConfiguration(self) -> dict:
        """
        Return a dict with field full name as key
        and a tuple as value (field_value, is_locked)

        field_value is given in keV for energies else in 'base units'

        limitation: for now sample position are not handled because this is a 'corner case' for now
        """

        def to_base_units_magnitude_if_exists(value: None | pint.Quantity):
            if value is None:
                return None
            else:
                return value.to_base_units().magnitude

        energy = self._energyEntry.getValue()
        if energy is not None:
            assert isinstance(energy, float)

        return {
            NXtomoEditorKeys.ENERGY: (
                energy,
                self._energyLockerLB.isLocked(),
            ),
            NXtomoEditorKeys.DETECTOR_X_PIXEL_SIZE: (
                to_base_units_magnitude_if_exists(
                    self._xDetectorPixelSizeMetricEntry.getValue()
                ),
                self._xDetectorPixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.DETECTOR_Y_PIXEL_SIZE: (
                to_base_units_magnitude_if_exists(
                    self._yDetectorPixelSizeMetricEntry.getValue()
                ),
                self._yDetectorPixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.SAMPLE_X_PIXEL_SIZE: (
                to_base_units_magnitude_if_exists(
                    self._xSamplePixelSizeMetricEntry.getValue()
                ),
                self._xSamplePixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.SAMPLE_Y_PIXEL_SIZE: (
                to_base_units_magnitude_if_exists(
                    self._ySamplePixelSizeMetricEntry.getValue()
                ),
                self._ySamplePixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE: (
                to_base_units_magnitude_if_exists(
                    self._sampleDetectorDistanceMetricEntry.getValue()
                ),
                self._sampleDetectorDistanceLB.isLocked(),
            ),
            NXtomoEditorKeys.SAMPLE_SOURCE_DISTANCE: (
                to_base_units_magnitude_if_exists(
                    self._sampleSourceDistanceMetricEntry.getValue()
                ),
                self._sampleSourceDistanceLB.isLocked(),
            ),
            NXtomoEditorKeys.FIELD_OF_VIEW: (
                self._fieldOfViewCB.currentText(),
                self._fieldOfViewLB.isChecked(),
            ),
            NXtomoEditorKeys.LR_FLIPPED: (
                self._lrFlippedCB.isChecked(),
                self._lrFlippedLB.isChecked(),
            ),
            NXtomoEditorKeys.UD_FLIPPED: (
                self._udFlippedCB.isChecked(),
                self._udFlippedLB.isChecked(),
            ),
            NXtomoEditorKeys.PROPAGATION_DISTANCE: (
                to_base_units_magnitude_if_exists(
                    self._propagationDistanceMetricEntry.getValue(),
                ),
                self._propagationDistanceLB.isLocked(),
            ),
            NXtomoEditorKeys.X_TRANSLATION: (
                to_base_units_magnitude_if_exists(self._xTranslationQLE.getValue()),
            ),
            NXtomoEditorKeys.Z_TRANSLATION: (
                to_base_units_magnitude_if_exists(self._zTranslationQLE.getValue()),
            ),
        }

    def setConfiguration(self, config: dict) -> None:
        """
        Load given configuration. We expect all quantities to be given:
        * in keV for energies
        * else in base units
        """
        # energy
        energy = config.get(NXtomoEditorKeys.ENERGY, None)
        if energy is not None:
            energy, energy_locked = energy
            assert energy is None or isinstance(
                energy, float
            ), "energy is expected to be dimensionless (float) already in keV"
            self._energyEntry.setValue(energy)
            self._energyLockerLB.setLock(energy_locked)

        # detector pixel size
        detector_x_pixel_size = config.get(NXtomoEditorKeys.DETECTOR_X_PIXEL_SIZE, None)
        if detector_x_pixel_size is not None:
            detector_x_pixel_size, detector_x_pixel_size_locked = detector_x_pixel_size
            self._xDetectorPixelSizeMetricEntry.setValue(
                detector_x_pixel_size, displayed_unit=_ureg.meter
            )
            self._xDetectorPixelSizeLB.setLock(detector_x_pixel_size_locked)

        detector_y_pixel_size = config.get(NXtomoEditorKeys.DETECTOR_Y_PIXEL_SIZE, None)
        if detector_y_pixel_size is not None:
            detector_y_pixel_size, detector_y_pixel_size_locked = detector_y_pixel_size
            self._yDetectorPixelSizeMetricEntry.setValue(
                detector_y_pixel_size, displayed_unit=_ureg.meter
            )
            self._yDetectorPixelSizeLB.setLock(detector_y_pixel_size_locked)

        # sample detector distance
        sample_detector_distance = config.get(
            NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE, None
        )
        if sample_detector_distance is not None:
            sample_detector_distance, distance_locked = sample_detector_distance
            self._sampleDetectorDistanceMetricEntry.setValue(
                sample_detector_distance, displayed_unit=_ureg.meter
            )
            self._sampleDetectorDistanceLB.setLock(distance_locked)

        # field of view
        field_of_view = config.get(NXtomoEditorKeys.FIELD_OF_VIEW, None)
        if field_of_view is not None:
            field_of_view, field_of_view_locked = field_of_view
            field_of_view = FOV.from_value(field_of_view)
            self._fieldOfViewCB.setCurrentText(field_of_view.value)
            self._fieldOfViewLB.setLock(field_of_view_locked)

        lr_flipped = config.get(NXtomoEditorKeys.LR_FLIPPED, None)
        if lr_flipped is not None:
            lr_flipped, lr_flipped_locked = lr_flipped
            lr_flipped = lr_flipped in (True, "True", "true")
            self._lrFlippedCB.setChecked(lr_flipped)
            self._lrFlippedLB.setLock(lr_flipped_locked)

        ud_flipped = config.get(NXtomoEditorKeys.UD_FLIPPED, None)
        if ud_flipped is not None:
            ud_flipped, ud_flipped_locked = ud_flipped
            ud_flipped = ud_flipped in (True, "True", "true")
            self._udFlippedCB.setChecked(ud_flipped)
            self._udFlippedLB.setLock(ud_flipped_locked)

        # sample source distance
        sample_source_distance = config.get(
            NXtomoEditorKeys.SAMPLE_SOURCE_DISTANCE, None
        )
        if sample_source_distance is not None:
            sample_source_distance, sample_source_distance_locked = (
                sample_source_distance
            )
            if sample_source_distance >= 0:
                _logger.warning("the sample-source is expected to be negative")
            self._sampleSourceDistanceMetricEntry.setValue(sample_source_distance)
            self._sampleSourceDistanceLB.setLock(sample_source_distance_locked)

        # sample pixel size
        sample_x_pixel_size = config.get(NXtomoEditorKeys.SAMPLE_X_PIXEL_SIZE, None)
        if sample_x_pixel_size is not None:
            sample_x_pixel_size, x_sample_pixel_size_locked = sample_x_pixel_size
            self._xSamplePixelSizeMetricEntry.setValue(
                sample_x_pixel_size, displayed_unit=_ureg.meter
            )
            self._xSamplePixelSizeLB.setLock(x_sample_pixel_size_locked)

        sample_y_pixel_size = config.get(NXtomoEditorKeys.SAMPLE_Y_PIXEL_SIZE, None)
        if sample_y_pixel_size is not None:
            sample_y_pixel_size, sample_y_pixel_size_locked = sample_y_pixel_size
            self._ySamplePixelSizeMetricEntry.setValue(
                sample_y_pixel_size, displayed_unit=_ureg.meter
            )
            self._ySamplePixelSizeLB.setLock(sample_y_pixel_size_locked)

        # propagation distance
        propagation_distance = config.get(NXtomoEditorKeys.PROPAGATION_DISTANCE, None)
        if propagation_distance is not None:
            propagation_distance, propagation_distance_locked = propagation_distance
            self._propagationDistanceMetricEntry.setValue(propagation_distance)
            self._propagationDistanceLB.setChecked(propagation_distance_locked)

    def getConfigurationForTask(self) -> dict:
        """
        default configuration is stored as field: (field_value, filed_is_locked) when the task expects field_key: field_value
        Because we need to be able to reload settings of the LockButton.
        But the task doesn't care about it. She only want to know which field must be edited. So we need to filter the dict value.
        """
        return {key: value[0] for key, value in self.getConfiguration().items()}

    def clear(self) -> None:
        self._tree.clear()


class _TranslationMetricEntry(MetricEntry):
    """
    Widget to define a translation along one axis.

    The behavior is limited at the moment.
    * either the array contains a unique value on the array and a float is displayed
    * either the array contains several unique values and then '...' will be displayed. Users cannot provide an array in this case.
    """

    LOADED_ARRAY = "loaded array"

    class TranslationValidator(qt.QDoubleValidator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setNotation(qt.QDoubleValidator.ScientificNotation)

        def validate(self, a0: str, a1: int):
            if "..." in a0:
                return (qt.QDoubleValidator.Acceptable, a0, a1)
            else:
                return super().validate(a0, a1)

    def __init__(self, name, default_unit=_ureg.meter, parent=None):
        super().__init__(name, default_unit=default_unit, parent=parent)
        self._qlePixelSize.setValidator(self.TranslationValidator(self))

    def getValue(self) -> float:
        """

        :return: the value in meter
        """
        if "..." in self._qlePixelSize.text():
            # in this case this is the representation of an array, we don;t wan't to overwrite it
            return self.LOADED_ARRAY
        if self._qlePixelSize.text() in ("unknown", ""):
            return None
        else:
            return float(self._qlePixelSize.text()) * self.getCurrentUnit()


class EnergyEntry(qt.QLineEdit):
    """
    QLineEdit enabling to handle an energy in keV
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(MetricEntry.DoubleValidator())

    def setValue(self, value_kev: float | None):
        if not isinstance(value_kev, (float, type(None))):
            raise TypeError(
                f"a0 is expected to be {None} or an instance of {float}. Got {type(value_kev)}"
            )

        if value_kev is None:
            value_kev = "unknown"
        else:
            value_kev = str(value_kev)
        super().setText(value_kev)

    def getValue(self) -> float | None:
        """
        Return energy in keV or None
        """
        txt = self.text().replace(" ", "")
        if txt in ("unknown", ""):
            return None
        else:
            return float(txt)

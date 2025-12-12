from __future__ import annotations

from silx.gui import qt
from nabu.stitching.alignment import AlignmentAxis1, AlignmentAxis2


class _AlignmentGroupBox(qt.QGroupBox):
    DEFAULT_PAD_MODE = "constant"

    ALIGNMENT_DOC = (
        "https://tomotools.gitlab-pages.esrf.fr/nabu/stitching/alignment.html"
    )

    DEFAULT_ALIGNMENT_AXIS_1 = AlignmentAxis1.CENTER
    DEFAULT_ALIGNMENT_AXIS_2 = AlignmentAxis2.CENTER

    _PAD_MODES = (
        "constant",  # Pads with a constant value.
        "edge",  # Pads with the edge values of array.
        "linear_ramp",  # Pads with the linear ramp between end_value and the array edge value.
        "maximum",  # Pads with the maximum value of all or part of the vector along each axis.
        "mean",  # Pads with the mean value of all or part of the vector along each axis.
        "median",  # Pads with the median value of all or part of the vector along each axis.
        "minimum",  # Pads with the minimum value of all or part of the vector along each axis.
        "reflect",  # Pads with the reflection of the vector mirrored on the first and last values of the vector along each axis.
        "symmetric",  # Pads with the reflection of the vector mirrored along the edge of the array.
        "wrap",  # Pads with the wrap of the vector along the axis. The first values are used to pad the end and the end values are used to pad the beginning.
    )

    def __init__(self, parent: qt.QWidget = None, title="alignment") -> None:
        super().__init__(title, parent)
        self.setLayout(qt.QFormLayout())

        # alignment axis 1
        self._alignmentAxis1CB = qt.QComboBox(self)
        for alignment in AlignmentAxis1:
            self._alignmentAxis1CB.addItem(alignment.value)
        self.layout().addRow("Axis 1 alignment", self._alignmentAxis1CB)
        self._alignmentAxis1CB.setToolTip(
            f"Alignment to do in case of volumes with different size over axis 1. Only possible for post-processing (reconstructed volume). See {self.ALIGNMENT_DOC} for details."
        )

        # alignment axis 2
        self._alignmentAxis2CB = qt.QComboBox(self)
        for alignment in AlignmentAxis2:
            self._alignmentAxis2CB.addItem(alignment.value)
        self.layout().addRow("Axis 2 alignment", self._alignmentAxis2CB)
        self._alignmentAxis2CB.setToolTip(
            f"Alignment to do in case of frames with different size over axis 2. See {self.ALIGNMENT_DOC} for details."
        )

        # pad mode
        self._padModeCB = qt.QComboBox(self)
        for pad_mode in self._PAD_MODES:
            self._padModeCB.addItem(pad_mode)
        self.layout().addRow("pad mode", self._padModeCB)
        self._padModeCB.setToolTip("padding mode to apply for alignment")

        # set up
        self.setAlignmentAxis1(self.DEFAULT_ALIGNMENT_AXIS_1)
        self.setAlignmentAxis2(self.DEFAULT_ALIGNMENT_AXIS_2)

    def getAlignmentAxis1(self) -> AlignmentAxis1:
        return AlignmentAxis1(self._alignmentAxis1CB.currentText())

    def setAlignmentAxis1(self, alignment: AlignmentAxis1):
        alignment = AlignmentAxis1(alignment)
        self._alignmentAxis1CB.setCurrentIndex(
            self._alignmentAxis1CB.findText(alignment.value)
        )

    def getAlignmentAxis2(self) -> AlignmentAxis2:
        return AlignmentAxis2(self._alignmentAxis2CB.currentText())

    def setAlignmentAxis2(self, alignment: AlignmentAxis2):
        alignment = AlignmentAxis2(alignment)
        self._alignmentAxis2CB.setCurrentIndex(
            self._alignmentAxis2CB.findText(alignment.value)
        )

    def getPadMode(self) -> str:
        return self._padModeCB.currentText()

    def setPadMode(self, pad_mode: str):
        idx = self._padModeCB.findText(pad_mode)
        if idx >= 0:
            self._padModeCB.setCurrentIndex(idx)

    def setAlignmentAxis1Enabled(self, enabled: bool):
        self._alignmentAxis1CB.setEnabled(enabled)

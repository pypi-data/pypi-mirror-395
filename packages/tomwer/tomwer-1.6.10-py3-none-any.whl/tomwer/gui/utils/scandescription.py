from __future__ import annotations

from silx.gui import qt

from tomwer.core.scan.scanbase import TomwerScanBase


class ScanNameLabelAndShape(qt.QWidget):
    """Scan to display the scan name"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        label = qt.QLabel("scan: ", self)
        label.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.layout().addWidget(label)
        self._scanNameLabel = qt.QLabel("", self)
        self._scanNameLabel.setAlignment(qt.Qt.AlignLeft)
        self._scanNameLabel.setSizePolicy(
            qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum
        )
        self.layout().addWidget(self._scanNameLabel)

        self._shapeLabel = qt.QLabel("", self)
        self._shapeLabel.setAlignment(qt.Qt.AlignLeft)
        self._shapeLabel.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._shapeLabel)

        # set up
        self.clear()

    def setScan(self, scan: TomwerScanBase | None):
        if scan is None or scan.path is None:
            self.clear()
        elif not isinstance(scan, TomwerScanBase):
            raise TypeError(
                f"Scan is expected to be an  instance of {TomwerScanBase}. Get {type(scan)} instead"
            )
        else:
            assert isinstance(scan, TomwerScanBase)
            self._scanNameLabel.setText(scan.get_identifier().short_description())
            self._scanNameLabel.setToolTip(scan.get_identifier().to_str())

            shape_x = scan.dim_1 if scan.dim_1 is not None else "?"
            shape_y = scan.dim_2 if scan.dim_2 is not None else "?"
            self._shapeLabel.setText(f"dims: x={shape_x}, y={shape_y}")

    def clear(self):
        self._scanNameLabel.setText("-")
        self._scanNameLabel.setToolTip("")
        self._shapeLabel.setText("")

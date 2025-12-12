from __future__ import annotations

import functools
from silx.gui import qt
from tomwer.gui.utils.qt_utils import block_signals


class StepSizeSelectorWidget(qt.QGroupBox):
    """
    Widget to define some steps size (as float). Used by the Axis and the AxisOrdered widgets

    :param title: title to provide to the group box
    :param label: text for the label set at the left of the QLineEdit
    :param fine_value: (optional) value to provide for 'fine' step
    :param medium_value: (optional) value to provide for 'medium' step
    :param rough_value: (optional) value to provide for 'rough' step
    :param dtype: type of the step. Can be int or float
    """

    valueChanged = qt.Signal()
    """emit when the step size change"""

    def __init__(
        self,
        parent=None,
        title="",
        label: str = "step size",
        fine_value: float | int | None = 0.1,
        medium_value: float | int | None = 0.5,
        rough_value: float | int | None = 1.0,
        unit: str | None = "px",
        dtype: int | float = float,
    ):
        assert fine_value is None or isinstance(
            fine_value, dtype
        ), f"fine_value is expected to be None or a {dtype}. Get {type(fine_value)}"
        assert medium_value is None or isinstance(
            medium_value, dtype
        ), f"medium_value is expected to be None or a {dtype}. Get {type(medium_value)}"
        assert rough_value is None or isinstance(
            rough_value, dtype
        ), f"rough_value is expected to be None or a {dtype}. Get {type(rough_value)}"
        super().__init__(title, parent)
        self._dtype = dtype
        if unit is None:
            unit = ""
        else:
            unit = f" {unit}"
        self.setLayout(qt.QGridLayout())
        self.layout().setSpacing(2)

        # label
        self.layout().addWidget(qt.QLabel(label), 0, 0, 3, 1)

        # QLE manual step size
        default_value = medium_value or fine_value or rough_value
        self._manualLE = qt.QLineEdit(str(default_value), parent=self)
        if dtype is float:
            validator = qt.QDoubleValidator(parent=self._manualLE, decimals=2)
            validator.setBottom(0.0)
        elif dtype is int:
            validator = qt.QIntValidator(parent=self._manualLE)
            validator.setBottom(0)
        else:
            raise ValueError("dtype is expected to be int or float")
        self._manualLE.setValidator(validator)
        self.layout().addWidget(self._manualLE, 0, 1, 3, 1)

        # buttons
        buttons_font = self.font()
        buttons_font.setPixelSize(10)
        self._expectedValues = {}
        # for each button associate the expected value

        # fine
        if fine_value is not None:
            self._fineButton = qt.QPushButton(f"fine ({fine_value}{unit})", parent=self)
            self._fineButton.setCheckable(True)
            self._fineButton.setFont(buttons_font)
            self.layout().addWidget(self._fineButton, 0, 2, 1, 1)
            self._fineButton.released.connect(
                functools.partial(self.setStepSize, fine_value)
            )
            self._expectedValues[self._fineButton] = fine_value
        else:
            self._fineButton = None

        # medium
        if medium_value is not None:
            self._mediumButton = qt.QPushButton(
                f"medium ({medium_value}{unit})", parent=self
            )
            self._mediumButton.setCheckable(True)
            self._mediumButton.setFont(buttons_font)
            self.layout().addWidget(self._mediumButton, 1, 2, 1, 1)
            self._mediumButton.released.connect(
                functools.partial(self.setStepSize, medium_value)
            )
            self._expectedValues[self._mediumButton] = medium_value
        else:
            self._mediumButton = None

        # rough
        if rough_value is not None:
            self._roughButton = qt.QPushButton(
                f"rough ({rough_value}{unit})", parent=self
            )
            self._roughButton.setCheckable(True)
            self._roughButton.setFont(buttons_font)
            self.layout().addWidget(self._roughButton, 2, 2, 1, 1)
            self._roughButton.released.connect(
                functools.partial(self.setStepSize, rough_value)
            )
            self._expectedValues[self._roughButton] = rough_value
        else:
            self._roughButton = None

        # connect signal / slot
        self._manualLE.textChanged.connect(self._updateButtonChecked)
        self._manualLE.textChanged.connect(self.valueChanged)
        # set up
        self._updateButtonChecked(self._manualLE.text())

    def _updateButtonChecked(self, text):
        if text == "":
            return
        current_value = self._dtype(text)
        for button, activation_value in self._expectedValues.items():
            with block_signals(button):
                button.setChecked(activation_value == current_value)

    def getStepSize(self) -> float | int:
        """

        :return: displacement shift defined. Output is of same type as the 'dtype' provided during construction.
        """
        return self._dtype(self._manualLE.text())

    def setStepSize(self, value: float | int):
        """

        :param value: shift step
        """
        assert isinstance(value, self._dtype)
        self._manualLE.setText(str(value))

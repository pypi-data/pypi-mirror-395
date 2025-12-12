from silx.gui import qt


class SliderPlayWidgetAction(qt.QWidgetAction):

    sigValueChanged = qt.Signal(int)

    def __init__(
        self,
        parent: qt.QWidget | None = None,
        label: str | None = None,
        tooltip: str | None = None,
    ):
        super().__init__(parent)
        self._build(label=label, tooltip=tooltip)

    def _build(self, label: str, tooltip: str):
        widget = qt.QWidget()
        layout = qt.QHBoxLayout()
        widget.setLayout(layout)
        self._spinbox = qt.QSpinBox()
        self._spinbox.setToolTip(tooltip)
        self._spinbox.setRange(1, 1000000)
        self._spinbox.valueChanged.connect(self.sigValueChanged)
        label = qt.QLabel(label)
        label.setToolTip(tooltip)
        layout.addWidget(label)
        layout.addWidget(self._spinbox)
        self.setDefaultWidget(widget)

    def value(self) -> int:
        return self._spinbox.value()

    def setValue(self, value: int):
        self._spinbox.setValue(value)


class PlayButtonContextMenu(qt.QMenu):

    sigFrameRateChanged = qt.Signal(int)

    def __init__(self, parent: qt.QWidget | None = None):
        super().__init__(parent)
        self._build()

    def _build(self):
        self._framerateAction = SliderPlayWidgetAction(
            self, label="FPS:", tooltip="Display speed in frames per second"
        )
        self._framerateAction.sigValueChanged.connect(self.sigFrameRateChanged)
        self._stepAction = SliderPlayWidgetAction(
            self, label="Step:", tooltip="Step between displayed frames"
        )
        self.addAction(self._framerateAction)
        self._framerateAction.setValue(10)
        self.addAction(self._stepAction)
        self._stepAction.setValue(1)

    def getFrameRate(self) -> int:
        return self._framerateAction.value()

    def setFrameRate(self, rate: int):
        self._framerateAction.setValue(rate)

    def getStep(self) -> int:
        return self._stepAction.value()

    def setStep(self, interval: int):
        self._stepAction.setValue(interval)

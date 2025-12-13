from __future__ import annotations

from silx.gui import qt
from silx.gui import icons

from silx.gui.widgets.FrameBrowser import FrameBrowser

try:
    from silx.gui.widgets.FrameBrowser import PlayButtonContextMenu
except ImportError:
    from tomwer.third_part.FrameBrowser import PlayButtonContextMenu


class HorizontalSliderWithBrowser(qt.QAbstractSlider):
    """
    Slider widget combining a :class:`QSlider` and a :class:`FrameBrowser`.

    .. image:: img/HorizontalSliderWithBrowser.png

    The data model is an integer within a range.

    The default value is the default :class:`QSlider` value (0),
    and the default range is the default QSlider range (0 -- 99)

    The signal emitted when the value is changed is the usual QAbstractSlider
    signal :attr:`valueChanged`. The signal carries the value (as an integer).

    :param QWidget parent: Optional parent widget
    """

    def __init__(self, parent=None):
        qt.QAbstractSlider.__init__(self, parent)
        self.setOrientation(qt.Qt.Horizontal)

        self.mainLayout = qt.QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(2)

        self._slider = qt.QSlider(self)
        self._slider.setOrientation(qt.Qt.Horizontal)

        self._browser = FrameBrowser(self)

        # avoid focus on the on buttons that can be activated when editing the slice index (from the QLinEdit)
        for button in (
            self._browser.firstButton,
            self._browser.previousButton,
            self._browser.nextButton,
            self._browser.lastButton,
        ):
            button.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)

        self.mainLayout.addWidget(self._slider, 0, 0, 1, 7)
        self.mainLayout.addWidget(self._browser, 0, 7, 1, 1)

        self._slider.valueChanged[int].connect(self._sliderSlot)
        self._browser.sigIndexChanged.connect(self._browserSlot)

        fontMetric = self.fontMetrics()
        iconSize = qt.QSize(fontMetric.height(), fontMetric.height())

        self.__timer = qt.QTimer(self)
        self.__timer.timeout.connect(self._updateState)

        self._playButton = qt.QToolButton(self)
        self._playButton.setToolTip("Display dataset movie.")
        self._playButton.setIcon(icons.getQIcon("camera"))
        self._playButton.setIconSize(iconSize)
        self._playButton.setCheckable(True)
        self.mainLayout.addWidget(self._playButton, 0, 8, 1, 1)

        self._playButton.toggled.connect(self._playButtonToggled)
        self._menuPlaySlider = PlayButtonContextMenu(self)
        self._menuPlaySlider.sigFrameRateChanged.connect(self._frameRateChanged)
        self._frameRateChanged(self.getFrameRate())
        self._playButton.setMenu(self._menuPlaySlider)
        self._playButton.setPopupMode(qt.QToolButton.MenuButtonPopup)

        # handle slice index buttons
        sliceButtonFont = self.font()
        sliceButtonFont.setPixelSize(8)
        # one-quarters button
        self.mainLayout.setColumnStretch(0, 1)
        self._oneQuarterButton = qt.QPushButton()
        self._oneQuarterButton.setFont(sliceButtonFont)
        self._oneQuarterButton.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        self.mainLayout.addWidget(self._oneQuarterButton, 1, 1, 1, 1)

        # two-quarters button
        self.mainLayout.setColumnStretch(2, 1)
        self._twoQuarterButton = qt.QPushButton()
        self._twoQuarterButton.setFont(sliceButtonFont)
        self._twoQuarterButton.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        self.mainLayout.addWidget(self._twoQuarterButton, 1, 3, 1, 1)

        # three-quarters button
        self.mainLayout.setColumnStretch(4, 1)
        self._threeQuarterButton = qt.QPushButton()
        self._threeQuarterButton.setFont(sliceButtonFont)
        self._threeQuarterButton.setFocusPolicy(qt.Qt.FocusPolicy.NoFocus)
        self.mainLayout.addWidget(self._threeQuarterButton, 1, 5, 1, 1)
        self.mainLayout.setColumnStretch(6, 1)

        self.setSliceIndices(None)
        self.setSliceBrowsingEnabled(False)

        # connect signal / slot
        for button in (
            self._oneQuarterButton,
            self._twoQuarterButton,
            self._threeQuarterButton,
        ):
            button.pressed.connect(self.__quarterButtonPressed)

    def lineEdit(self):
        """Returns the line edit provided by this widget.

        :rtype: qt.QLineEdit
        """
        return self._browser.lineEdit()

    def limitWidget(self):
        """Returns the widget displaying axes limits.

        :rtype: qt.QLabel
        """
        return self._browser.limitWidget()

    def setMinimum(self, value):
        """Set minimum value

        :param int value: Minimum value"""
        self._slider.setMinimum(value)
        maximum = self._slider.maximum()
        self._browser.setRange(value, maximum)

    def setMaximum(self, value):
        """Set maximum value

        :param int value: Maximum value
        """
        self._slider.setMaximum(value)
        minimum = self._slider.minimum()
        self._browser.setRange(minimum, value)

    def setRange(self, first, last):
        """Set minimum/maximum values

        :param int first: Minimum value
        :param int last: Maximum value"""
        self._slider.setRange(first, last)
        self._browser.setRange(first, last)

    def getRange(self) -> tuple[int, int]:
        return self._browser.getRange()

    def _sliderSlot(self, value):
        """Emit selected value when slider is activated"""
        self._browser.setValue(value)
        self.valueChanged.emit(value)

    def _browserSlot(self, ddict):
        """Emit selected value when browser state is changed"""
        self._slider.setValue(ddict["new"])

    def setValue(self, value):
        """Set value

        :param int value: value"""
        self._slider.setValue(value)
        self._browser.setValue(value)

    def value(self):
        """Get selected value"""
        return self._slider.value()

    def setFrameRate(self, value: int):
        """Set the frame rate at which images are displayed"""
        self._menuPlaySlider.setFrameRate(value)

    def getFrameRate(self) -> int:
        """Get the frame rate at which images are displayed"""
        return self._menuPlaySlider.getFrameRate()

    def setPlayImageStep(self, value: int):
        """Set the step between displayed images when playing"""
        self._menuPlaySlider.setStep(value)

    def getPlayImageStep(self) -> int:
        """Returns the step between displayed images"""
        return self._menuPlaySlider.getStep()

    def _frameRateChanged(self, framerate: int):
        """Update the timer interval"""
        self.__timer.setInterval(int(1 / framerate * 1e3))

    def _playButtonToggled(self, checked: bool):
        """Start/Stop the slider sequence."""
        if checked:
            self.__timer.start()
            return
        self.__timer.stop()

    def _updateState(self):
        """Advance an interval number of frames in the browser sequence."""
        currentIndex = self._browser.getValue()
        if currentIndex < self._browser.getRange()[-1]:
            self.setValue(currentIndex + self.getPlayImageStep())
        else:
            self._playButton.setChecked(False)

    def setSliceIndices(self, slices: None | tuple[int]):
        if (slices is not None) and len(slices) != 3:
            raise TypeError("slices is not None or a tuple of three elements.")
        slices_buttons = (
            self._oneQuarterButton,
            self._twoQuarterButton,
            self._threeQuarterButton,
        )
        if slices is None:
            [button.setVisible(False) for button in slices_buttons]
        else:
            slices = sorted(slices)
            for button_index, button in zip(slices, slices_buttons):
                button.setText(str(button_index))
                button.setVisible(True)

    def __quarterButtonPressed(self):
        self._slider.setValue(int(self.sender().text()))

    def setSliceBrowsingEnabled(self, enable):
        """
        Slice browsing is enabled if we agree to let the user browsing the entire stack of slice
        (if the volume is fully load or if on the fast-reading) axis. Else he can only select a pre-defined set of slice.
        """
        self._slider.setEnabled(enable)
        self._playButton.setEnabled(enable)
        self._browser.setEnabled(enable)

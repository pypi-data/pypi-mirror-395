# coding: utf-8
from __future__ import annotations

import logging
import weakref

import numpy
from silx.gui import icons as silx_icons
from silx.gui import qt
from silx.gui.plot.CompareImages import (
    CompareImages as _CompareImages,
    VisualizationMode,
)

from silx.gui.plot.tools.compare.toolbar import VisualizationModeToolButton
from silx.gui.plot import tools


_logger = logging.getLogger(__name__)


class CompareImages(_CompareImages):
    sigCropImagesChanged = qt.Signal()
    """Emit when cropping of the compared images has changed"""

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)

        # create crop images action
        icon = silx_icons.getQIcon("crop")
        action = qt.QAction(icon, "crop compared images", self)
        action.setCheckable(True)
        action.setChecked(True)
        action.triggered.connect(self.__cropComparedImagesChanged)
        self.__cropComparedImages = action
        self._compareToolBar.addAction(action)

        # define visible compare mode
        self._compareToolBar._visualizationToolButton.setVisibleModes(
            [
                VisualizationMode.ONLY_A,
                VisualizationMode.ONLY_B,
                VisualizationMode.COMPOSITE_RED_BLUE_GRAY_NEG,
                VisualizationMode.COMPOSITE_A_MINUS_B,
            ]
        )

    def __cropComparedImagesChanged(self):
        cropCompositeImage = self.__cropComparedImages.isChecked()
        self.setCropComparedImages(cropCompositeImage)

    def cropComparedImages(self) -> bool:
        return self.__cropComparedImages.isChecked()

    def setCropComparedImages(self, crop):
        self.__cropComparedImages.setChecked(crop)
        self.sigCropImagesChanged.emit()

    def _createToolBars(self, plot):
        """Create tool bars displayed by the widget"""
        toolBar = tools.InteractiveModeToolBar(parent=self, plot=plot)
        self._interactiveModeToolBar = toolBar
        toolBar = tools.ImageToolBar(parent=self, plot=plot)
        self._imageToolBar = toolBar
        toolBar = CompareImagesToolBar(self)
        toolBar.setCompareWidget(self)
        self._compareToolBar = toolBar


class CompareImagesStatusBar(qt.QStatusBar):
    """StatusBar containing specific information contained in a
    :class:`CompareImages` widget

    Use :meth:`setCompareWidget` to connect this toolbar to a specific
    :class:`CompareImages` widget.

    :param parent: Parent of this widget.
    """

    def __init__(self, parent=None):
        qt.QStatusBar.__init__(self, parent)
        self.setSizeGripEnabled(False)
        self.layout().setSpacing(0)
        self.__compareWidget = None
        self._label1 = qt.QLabel(self)
        self._label1.setFrameShape(qt.QFrame.WinPanel)
        self._label1.setFrameShadow(qt.QFrame.Sunken)
        self._label2 = qt.QLabel(self)
        self._label2.setFrameShape(qt.QFrame.WinPanel)
        self._label2.setFrameShadow(qt.QFrame.Sunken)
        self._transform = qt.QLabel(self)
        self._transform.setFrameShape(qt.QFrame.WinPanel)
        self._transform.setFrameShadow(qt.QFrame.Sunken)
        self.addWidget(self._label1)
        self.addWidget(self._label2)
        self.addWidget(self._transform)
        self._pos = None
        self._updateStatusBar()

    def setCompareWidget(self, widget):
        """
        Connect this tool bar to a specific :class:`CompareImages` widget.

        :param widget: The widget to connect with.
        """
        compareWidget = self.getCompareWidget()
        if compareWidget is not None:
            compareWidget.getPlot().sigPlotSignal.disconnect(self.__plotSignalReceived)
            compareWidget.sigConfigurationChanged.disconnect(self.__dataChanged)
        compareWidget = widget
        if compareWidget is None:
            self.__compareWidget = None
        else:
            self.__compareWidget = weakref.ref(compareWidget)
        if compareWidget is not None:
            compareWidget.getPlot().sigPlotSignal.connect(self.__plotSignalReceived)
            compareWidget.sigConfigurationChanged.connect(self.__dataChanged)

    def getCompareWidget(self) -> CompareImages:
        """Returns the connected widget."""
        if self.__compareWidget is None:
            return None
        else:
            return self.__compareWidget()

    def __plotSignalReceived(self, event):
        """Called when old style signals at emmited from the plot."""
        if event["event"] == "mouseMoved":
            x, y = event["x"], event["y"]
            self.__mouseMoved(x, y)

    def __mouseMoved(self, x, y):
        """Called when mouse move over the plot."""
        self._pos = x, y
        self._updateStatusBar()

    def __dataChanged(self):
        """Called when internal data from the connected widget changes."""
        self._updateStatusBar()

    def _formatData(self, data: int | float | None) -> str:
        """Format pixel of an image.

        It supports intensity, RGB, and RGBA.

        :param data: Value of a pixel
        """
        if data is None:
            return "-"
        if isinstance(data, (int, numpy.integer)):
            return "%d" % data
        if isinstance(data, (float, numpy.floating)):
            return "%f" % data
        if isinstance(data, numpy.ndarray):
            # RGBA value
            if data.shape == (3,):
                return "R:%d G:%d B:%d" % (data[0], data[1], data[2])
            elif data.shape == (4,):
                return "R:%d G:%d B:%d A:%d" % (data[0], data[1], data[2], data[3])
        _logger.debug("Unsupported data format %s. Cast it to string.", type(data))
        return str(data)

    def _updateStatusBar(self):
        """Update the content of the status bar"""
        widget = self.getCompareWidget()
        if widget is None:
            self._label1.setText("Frame 1: -")
            self._label2.setText("Frame 2: -")
            self._transform.setVisible(False)
        else:
            transform = widget.getTransformation()
            self._transform.setVisible(transform is not None)
            if transform is not None:
                has_notable_translation = not numpy.isclose(
                    transform.tx, 0.0, atol=0.01
                ) or not numpy.isclose(transform.ty, 0.0, atol=0.01)
                has_notable_scale = not numpy.isclose(
                    transform.sx, 1.0, atol=0.01
                ) or not numpy.isclose(transform.sy, 1.0, atol=0.01)
                has_notable_rotation = not numpy.isclose(transform.rot, 0.0, atol=0.01)

                strings = []
                if has_notable_translation:
                    strings.append("Translation")
                if has_notable_scale:
                    strings.append("Scale")
                if has_notable_rotation:
                    strings.append("Rotation")
                if strings == []:
                    has_translation = not numpy.isclose(
                        transform.tx, 0.0
                    ) or not numpy.isclose(transform.ty, 0.0)
                    has_scale = not numpy.isclose(
                        transform.sx, 1.0
                    ) or not numpy.isclose(transform.sy, 1.0)
                    has_rotation = not numpy.isclose(transform.rot, 0.0)
                    if has_translation or has_scale or has_rotation:
                        text = "No big changes"
                    else:
                        text = "No changes"
                else:
                    text = "+".join(strings)
                self._transform.setText("Align: " + text)

                strings = []
                if not numpy.isclose(transform.ty, 0.0):
                    strings.append("Translation x: %0.3fpx" % transform.tx)
                if not numpy.isclose(transform.ty, 0.0):
                    strings.append("Translation y: %0.3fpx" % transform.ty)
                if not numpy.isclose(transform.sx, 1.0):
                    strings.append("Scale x: %0.3f" % transform.sx)
                if not numpy.isclose(transform.sy, 1.0):
                    strings.append("Scale y: %0.3f" % transform.sy)
                if not numpy.isclose(transform.rot, 0.0):
                    _rot = transform.rot * 180 / numpy.pi
                    strings.append(f"Rotation: {_rot:0.3f}deg")
                if strings == []:
                    text = "No transformation"
                else:
                    text = "\n".join(strings)
                self._transform.setToolTip(text)

            if self._pos is None:
                self._label1.setText("Frame 1: -")
                self._label2.setText("Frame 2: -")
            else:
                data1, data2 = widget.getRawPixelData(self._pos[0], self._pos[1])
                if isinstance(data1, str):
                    self._label1.setToolTip(data1)
                    text1 = "-"
                else:
                    self._label1.setToolTip("")
                    text1 = self._formatData(data1)
                if isinstance(data2, str):
                    self._label2.setToolTip(data2)
                    text2 = "-"
                else:
                    self._label2.setToolTip("")
                    text2 = self._formatData(data2)
                self._label1.setText("Frame 1: %s" % text1)
                self._label2.setText("Frame 2: %s" % text2)


class CompareImagesToolBar(qt.QToolBar):
    def __init__(self, parent=None):
        qt.QToolBar.__init__(self, parent)

        self.__compareWidget = None

        self._visualizationToolButton = VisualizationModeToolButton(self)
        self._visualizationToolButton.setPopupMode(qt.QToolButton.InstantPopup)
        self._visualizationToolButton.sigSelected.connect(self.__visualizationChanged)
        self.addWidget(self._visualizationToolButton)

    def __visualizationChanged(self, mode: VisualizationMode):
        widget = self.getCompareWidget()
        if widget is not None:
            widget.setVisualizationMode(mode)

    def setCompareWidget(self, widget: None | CompareImages):
        """
        Connect this tool bar to a specific :class:`CompareImages` widget.

        :param widget: The widget to connect the toolbar with.
        """
        compareWidget = self.getCompareWidget()
        if compareWidget is not None:
            compareWidget.sigConfigurationChanged.disconnect(
                self.__updateSelectedActions
            )
        compareWidget = widget
        self.setEnabled(compareWidget is not None)
        if compareWidget is None:
            self.__compareWidget = None
        else:
            self.__compareWidget = weakref.ref(compareWidget)
        if compareWidget is not None:
            widget.sigConfigurationChanged.connect(self.__updateSelectedActions)
        self.__updateSelectedActions()

    def getCompareWidget(self) -> CompareImages:
        """Returns the connected widget."""
        if self.__compareWidget is None:
            return None
        else:
            return self.__compareWidget()

    def __updateSelectedActions(self):
        """
        Update the state of this tool bar according to the state of the
        connected :class:`CompareImages` widget.
        """
        widget = self.getCompareWidget()
        if widget is None:
            return
        self._visualizationToolButton.setSelected(widget.getVisualizationMode())

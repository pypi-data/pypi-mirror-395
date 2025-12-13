from __future__ import annotations

from silx.gui import qt
from silx.gui.colors import Colormap
from tomwer.gui import icons as tomwer_icons
from tomwer.core.utils.char import ALPHA_CHAR


class AlphaChannelWidget(qt.QWidget):
    """
    Widget to select alpha level of the stiched image and of the background
    """

    sigAlphaImgChanged = qt.Signal()
    """signal emit when the alpha of the stitched image changed"""
    sigAlphaBackgroundChanged = qt.Signal()
    """signal emit when the alpha of the background image changed"""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setLayout(qt.QFormLayout())
        self._alphaImgSlider = qt.QSlider(qt.Qt.Horizontal, self)
        self._alphaImgSlider.setMinimumWidth(40)
        self._alphaImgSlider.setRange(0, 100)
        self.layout().addRow(f"{ALPHA_CHAR} image", self._alphaImgSlider)
        self._alphaBackgroundSlider = qt.QSlider(qt.Qt.Horizontal, self)
        self._alphaBackgroundSlider.setMinimumWidth(40)
        self._alphaBackgroundSlider.setRange(0, 100)
        self.layout().addRow(f"{ALPHA_CHAR} overlay", self._alphaBackgroundSlider)

        # connect signal / slot
        self._alphaImgSlider.valueChanged.connect(self._alphaImgchanged)
        self._alphaBackgroundSlider.valueChanged.connect(self._alphaBackgroundchanged)

    def _alphaImgchanged(self, *args, **kwargs):
        self.sigAlphaImgChanged.emit()

    def _alphaBackgroundchanged(self, *args, **kwargs):
        self.sigAlphaBackgroundChanged.emit()

    def setAlphaStitchedImg(self, alpha: float):
        self._alphaImgSlider.setValue(int(alpha * 100.0))

    def getAlphaStitchedImg(self) -> float:
        return self._alphaImgSlider.value() / 100.0

    def setAlphaBackgroundImg(self, alpha: float):
        self._alphaBackgroundSlider.setValue(int(alpha * 100.0))

    def getAlphaBackgroundImg(self) -> float:
        return self._alphaBackgroundSlider.value() / 100.0


class StitchAndBackgroundAlphaMixIn:
    """
    Mix in class for windows displaying a stitched image with or without the background
    """

    LEGEND_STITCHED_FRAME = "stitched frame"
    LEGEND_BACKGROUND = "background"

    def __init__(self) -> None:
        self._stitched_image = None
        self._composition_background = None
        # background action to show / hide the backgrounds
        self._backGroundAction = qt.QAction("overlay", self)
        self._backGroundAction.setToolTip("Toggle overlay on top of image")
        self._backGroundAction.setCheckable(True)
        save_icon = tomwer_icons.getQIcon("background")
        self._backGroundAction.setIcon(save_icon)
        self.__firstPlot = True
        self._backgroundColormap = Colormap(name="viridis")

        # build
        self._alphaChannelWidget = AlphaChannelWidget(parent=self)

        # connect signal / slot
        self._backGroundAction.toggled.connect(self._update)
        self._alphaChannelWidget.sigAlphaImgChanged.connect(self._updateAlphaImg)
        self._alphaChannelWidget.sigAlphaBackgroundChanged.connect(
            self._updateAlphaBackgroundImg
        )

    def getStitchedImgAlpha(self) -> float:
        """
        :return: alpha value to set to the stitched image. If only the image is displayed then will be 1.0 else will be the value defined by the "alpha channel' widget
        """
        if self._backGroundAction.isChecked():
            return self._alphaChannelWidget.getAlphaStitchedImg()
        else:
            return 1.0

    def getBackgroundImgAlpha(self) -> float | None:
        """return 0.0 if there is no background image"""
        if self._backGroundAction.isChecked():
            return self._alphaChannelWidget.getAlphaBackgroundImg()
        else:
            return 0.0

    def _updateAlphaImg(self, *args, **kwargs):
        alpha_img = self.getImage(self.LEGEND_STITCHED_FRAME)
        if alpha_img is not None:
            alpha_img.setAlpha(self.getStitchedImgAlpha())

    def _updateAlphaBackgroundImg(self, *args, **kwargs):
        background_img = self.getImage(self.LEGEND_BACKGROUND)
        if background_img is not None:
            background_img.setAlpha(self.getBackgroundImgAlpha())

    def _update(self):
        """
        update display. Allow to handle modification of alpha values and to dsiplay or not the background / composition
        """
        if self._stitched_image is None:
            return
        if self._backGroundAction.isChecked():
            self.addImage(
                self._stitched_image,
                legend=self.LEGEND_STITCHED_FRAME,
                resetzoom=self.__firstPlot,
            )
            image_data = self.getImage(legend=self.LEGEND_STITCHED_FRAME)
            image_data.setAlpha(self.getStitchedImgAlpha())
            self.addImage(
                self._composition_background,
                legend=self.LEGEND_BACKGROUND,
                resetzoom=self.__firstPlot,
                colormap=self._backgroundColormap,
            )
            background_data = self.getImage(legend=self.LEGEND_BACKGROUND)
            background_data.setAlpha(self.getBackgroundImgAlpha())
        else:
            if self.getImage(self.LEGEND_BACKGROUND) is not None:
                self.removeImage(self.LEGEND_BACKGROUND)
            self.addImage(
                self._stitched_image,
                legend=self.LEGEND_STITCHED_FRAME,
                resetzoom=self.__firstPlot,
            )
            background_data = self.getImage(legend=self.LEGEND_STITCHED_FRAME)
            background_data.setAlpha(self.getStitchedImgAlpha())
        self.setActiveImage(legend=self.LEGEND_STITCHED_FRAME)
        self.__firstPlot = False

    # expose API
    def setAlphaBackgroundImg(self, value):
        self._alphaChannelWidget.setAlphaBackgroundImg(value)

    def setAlphaStitchedImg(self, value):
        self._alphaChannelWidget.setAlphaStitchedImg(value)

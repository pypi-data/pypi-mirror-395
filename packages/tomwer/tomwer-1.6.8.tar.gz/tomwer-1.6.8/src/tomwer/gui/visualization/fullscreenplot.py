from __future__ import annotations

import weakref
from silx.gui import qt
from silx.gui.plot import Plot2D
from silx.gui.colors import Colormap

from tomwer.gui import icons
from tomwer.gui.settings import Y_AXIS_DOWNWARD
from tomwer.gui.stitching.stitchandbackground import StitchAndBackgroundAlphaMixIn


class FullScreenPlot2D(Plot2D):
    """
    Window which goal is to display a single frame into full screen

    :param master_colormap: optional colormap that could redefine values of the current plot colormap
    """

    def __init__(self, parent=None, backend=None, master_colormap=None):
        super().__init__(parent, backend)
        if master_colormap is None:
            self.__master_colormap = master_colormap
        else:
            assert isinstance(master_colormap, Colormap)
            self.__master_colormap = weakref.ref(master_colormap)

        self.getPositionInfoWidget().hide()
        self.setYAxisInverted(Y_AXIS_DOWNWARD)
        self.setKeepDataAspectRatio(True)

        self.setAxesDisplayed(False)
        self.getColorBarWidget().hide()
        self.setWindowIcon(icons.getQIcon("tomwer"))

        # add toolbar to ease exit
        self.exit_toolbar = qt.QToolBar("exit", self)
        # add a spacer for conveniance
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Preferred)
        self.exit_toolbar.addWidget(spacer)
        self.addToolBar(self.exit_toolbar)
        # add exit button wen displayed full screen
        exit_icon = icons.getQIcon("exit")
        self._quitAction = qt.QAction(exit_icon, "exit", self)
        self.exit_toolbar.addAction(self._quitAction)

        if self.master_colormap is not None:
            master_colormap.sigChanged.connect(self._updateColormapFromMaster)

        self._updateColormapFromMaster()

        # connect signal / slot
        self._quitAction.triggered.connect(self.close)

    @property
    def master_colormap(self) -> Colormap | None:
        if self.__master_colormap is None:
            return None
        else:
            return self.__master_colormap()

    def _updateColormapFromMaster(self):
        if self.master_colormap is not None:
            current_colormap = self.getDefaultColormap()
            current_colormap.setFromColormap(self.master_colormap)


class FullScreenStitching(FullScreenPlot2D, StitchAndBackgroundAlphaMixIn):
    def __init__(
        self,
        stitching_img,
        background_img,
        parent=None,
        backend=None,
        master_colormap=None,
    ):
        super().__init__(parent, backend, master_colormap)
        self._stitched_image = stitching_img
        self._composition_background = background_img
        self._update()

        self._backgroundToolbar = qt.QToolBar("background")
        self._backgroundToolbar.addAction(self._backGroundAction)
        self.insertToolBar(self.toolBar(), self._backgroundToolbar)
        self._backgroundToolbar.addWidget(self._alphaChannelWidget)

        # set up
        self.setKeepDataAspectRatio(True)

    def _updateAlphaImg(self, *args, **kwargs):
        alpha_img = self.getImage(self.LEGEND_STITCHED_FRAME)
        if alpha_img is not None:
            alpha_img.setAlpha(self.getStitchedImgAlpha())

    def _updateAlphaBackgroundImg(self, *args, **kwargs):
        background_img = self.getImage(self.LEGEND_BACKGROUND)
        if background_img is not None:
            background_img.setAlpha(self.getBackgroundImgAlpha())

    @property
    def mother_plot(self) -> Plot2D | None:
        if self._mother_plot is None:
            return None
        else:
            return self._mother_plot()

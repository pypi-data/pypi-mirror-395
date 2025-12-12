from __future__ import annotations
import functools
from enum import Enum as _Enum
from silx.gui import qt
from tomwer.gui import icons


class LoadingMode(_Enum):
    ON_SHOW_LOADING = "load when show requested"
    LAZY_LOADING = "lazy loading"
    ASAP_LOADING = "load ASAP"

    def icon(self):
        if self is self.ON_SHOW_LOADING:
            return icons.getQIcon("low_speed")
        elif self is self.LAZY_LOADING:
            return icons.getQIcon("medium_low_speed")
        elif self is self.ASAP_LOADING:
            return icons.getQIcon("high_speed")
        else:
            raise ValueError(f"loading mode {self} not handled")

    def tooltip(self):
        if self is self.ON_SHOW_LOADING:
            return "will load data only when requiring"
            return icons.getQIcon("medium_low_speed")
        elif self is self.LAZY_LOADING:
            return "load data with reduce prefetch"
        elif self is self.ASAP_LOADING:
            return "load data as soon as possible"
        else:
            raise ValueError(f"loading mode {self} not handled")


class LoadingModeToolButton(qt.QToolButton):
    """Tool button to switch keep aspect ratio of a plot"""

    sigLoadModeChanged = qt.Signal(str)

    def __init__(self, parent=None):
        super(LoadingModeToolButton, self).__init__(parent=parent)
        menu = qt.QMenu(self)

        action_lazy_loading = LazyLoadingAction(parent=self)
        # by default icons are not visible from the menu. In this case we want to display it
        action_lazy_loading.setIconVisibleInMenu(True)
        fctLL = functools.partial(self.setLoadingMode, LoadingMode.LAZY_LOADING)
        menu.addAction(action_lazy_loading)

        action_asap_loading = ASAP_LoadingAction(parent=self)
        action_asap_loading.setIconVisibleInMenu(True)
        fctAL = functools.partial(self.setLoadingMode, LoadingMode.ASAP_LOADING)
        menu.addAction(action_asap_loading)

        self.setMenu(menu)
        # connect signal / slot
        action_lazy_loading.triggered.connect(fctLL)
        action_asap_loading.triggered.connect(fctAL)

        # set up
        self.setPopupMode(qt.QToolButton.InstantPopup)
        self.setLoadingMode(LoadingMode.LAZY_LOADING)

    def setLoadingMode(self, loadingMode: LoadingMode | str):
        loadingMode = LoadingMode(loadingMode)
        assert loadingMode in LoadingMode
        self.setIcon(loadingMode.icon())
        self.setToolTip(loadingMode.tooltip())
        self.sigLoadModeChanged.emit(loadingMode.value)


class LazyLoadingAction(qt.QAction):
    def __init__(self, parent):
        super().__init__("load data with small prefetch", parent=parent)
        self.setIcon(LoadingMode.LAZY_LOADING.icon())


class ASAP_LoadingAction(qt.QAction):
    def __init__(self, parent):
        super().__init__("load data ASAP", parent=parent)
        self.setIcon(LoadingMode.ASAP_LOADING.icon())

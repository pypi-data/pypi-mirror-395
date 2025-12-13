from __future__ import annotations

from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from tomwer.gui.configuration.level import ConfigurationLevel


class _FilteringObject:
    """
    Simple class to define if the widget should be visible or not if visible
    (at some moment the 'option' wudget should be visible) and if filtered.
    Should avoid some conflict when set set visible
    """

    def __init__(self, widget):
        self._widget = widget
        self._visible = True
        # is this
        self._filtered = False

    def setVisible(self, visible):
        self._visible = visible
        self._updateVisibility()

    def setFiltered(self, filtered):
        self._filtered = filtered
        self._updateVisibility()

    def _updateVisibility(self):
        self._widget.setVisible(self._visible and self._filtered)


class _NabuStageConfigBase:
    """Define interface for a specific nabu stage configuration widget
    (or a part of the stage configuration)
    """

    def __init__(self, stage: _NabuStages | str | None):
        if stage is None:
            self.__stage = None
        else:
            self.__stage = _NabuStages(stage)
        self._registeredWidgets = {}
        # list required widgets. Key is widget, value is the configuration
        # level

    def registerWidget(self, widget, config_level):
        """register a widget with a configuration level.

        :returns: _FilteringObject to use to define widget visibility
        """
        filteringObj = _FilteringObject(widget=widget)
        self._registeredWidgets[filteringObj] = ConfigurationLevel(config_level)
        return filteringObj

    def getConfiguration(self) -> dict:
        raise NotImplementedError("Base class")

    def setConfiguration(self, config) -> None:
        raise NotImplementedError("Base class")

    def getStage(self) -> _NabuStages | None:
        return self.__stage

    def setConfigurationLevel(self, level):
        for widget in self._registeredWidgets:
            filtered = self._registeredWidgets[widget] <= level
            widget.setFiltered(filtered)

# coding: utf-8
from __future__ import annotations


import functools
from typing import Iterable

from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import _NabuStages
from tomwer.gui import icons
from tomwer.utils import docstring

from ...utils.flow import FlowCanvas, FlowDirection


class NabuFlowControl(qt.QWidget):
    """
    Widget which is composed of three `FlowCanvas`: one for pre processing
    (where dockers are not movable), one for processing (where dockers are
    movable) and one for post-processing (where dockers are not movable)
    """

    sigConfigurationChanged = qt.Signal(tuple)
    """signal emitted when the `focus` process on the flow is changed.
    tuple is (stage, option)
    """
    sigResetConfiguration = qt.Signal()
    """Signal emitted when the configuration should be reset"""

    def __init__(self, parent, direction):
        qt.QWidget.__init__(self, parent=parent)

        self._direction = FlowDirection(direction)

        if self._direction is FlowDirection.VERTICAL:
            self.setLayout(qt.QVBoxLayout())
        else:
            self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        # initialization
        self._iniProcessWidgets = FlowCanvas(
            direction=direction, parent=self, show_lock_state=False
        )

        # preprocessing flow
        self._preProcessWidgets = FlowCanvas(
            direction=direction, parent=self, show_lock_state=False
        )

        # phase processing flow
        self._phaseProcessWidgets = FlowCanvas(
            direction=direction, parent=self, show_lock_state=False
        )

        # processing flow
        self._processWidgets = FlowCanvas(
            direction=direction, parent=self, show_lock_state=False
        )

        # postprocessing flow
        self._postProcessWidgets = FlowCanvas(
            direction=direction, parent=self, show_lock_state=False
        )

        for widget in (
            self._iniProcessWidgets,
            self._preProcessWidgets,
            self._phaseProcessWidgets,
            self._processWidgets,
            self._postProcessWidgets,
        ):
            self.layout().addWidget(widget)

        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)

        # connect signal / slot
        self._iniProcessWidgets.sigWidgetActivated.connect(
            functools.partial(self._updateActiveProcess, _NabuStages.INI)
        )
        self._iniProcessWidgets.sigWidgetDeactivated.connect(self.sigResetConfiguration)
        self._preProcessWidgets.sigWidgetActivated.connect(
            functools.partial(self._updateActiveProcess, _NabuStages.PRE)
        )
        self._preProcessWidgets.sigWidgetDeactivated.connect(self.sigResetConfiguration)
        self._phaseProcessWidgets.sigWidgetActivated.connect(
            functools.partial(self._updateActiveProcess, _NabuStages.PHASE)
        )
        self._phaseProcessWidgets.sigWidgetDeactivated.connect(
            self.sigResetConfiguration
        )
        self._processWidgets.sigWidgetActivated.connect(
            functools.partial(self._updateActiveProcess, _NabuStages.PROC)
        )
        self._processWidgets.sigWidgetDeactivated.connect(self.sigResetConfiguration)
        self._postProcessWidgets.sigWidgetActivated.connect(
            functools.partial(self._updateActiveProcess, _NabuStages.POST)
        )
        self._postProcessWidgets.sigWidgetDeactivated.connect(
            self.sigResetConfiguration
        )

        # set up
        self.setIniprocVisible(False)
        self.setPreProcVisible(True)
        self.setPhaseVisible(True)
        self.setProcVisible(True)
        self.setPostVisible(True)

    def _updateActiveProcess(self, stage):
        stage = _NabuStages(stage)

        if stage is _NabuStages.INI:
            activeWidget = self._iniProcessWidgets
        elif stage is _NabuStages.PRE:
            activeWidget = self._preProcessWidgets
        elif stage is _NabuStages.PHASE:
            activeWidget = self._phaseProcessWidgets
        elif stage is _NabuStages.PROC:
            activeWidget = self._processWidgets
        elif stage is _NabuStages.POST:
            activeWidget = self._postProcessWidgets
        else:
            raise ValueError("nabu stage not recognized")

        for widget in (
            self._iniProcessWidgets,
            self._preProcessWidgets,
            self._phaseProcessWidgets,
            self._processWidgets,
            self._postProcessWidgets,
        ):
            if widget != activeWidget:
                widget.clearActiveProcess()
        self.sigConfigurationChanged.emit(self.getProcessFocused())

    def setIniprocVisible(self, visible):
        """
        change visibility of the widgets relative to initialization process

        :param visible:
        """
        self._iniProcessWidgets.setVisible(visible)

    def setPreProcVisible(self, visible):
        """
        change visibility of the widgets relative to pre processing process

        :param visible:
        """
        self._preProcessWidgets.setVisible(visible)

    def setPhaseVisible(self, visible: bool):
        """
        change visibility of the widgets relative to pre processing process
        """
        self._phaseProcessWidgets.setVisible(visible)

    def setProcVisible(self, visible: bool):
        """
        change visibility of the widgets relative to processing process
        """
        self._processWidgets.setVisible(visible)

    def setPostVisible(self, visible: bool):
        """
        change visibility of the widgets relative to post processing process
        """
        self._postProcessWidgets.setVisible(visible)

    def setIniProcessing(self, processes: Iterable, icons: Iterable):
        """
        Defines the processing to execute for initialization

        :param processes: processes to display
        :param icons: icons associated to the processes if any
        """
        draggability = [False] * len(processes)
        self._iniProcessWidgets.setProcesses(
            processes=processes, icons=icons, draggability=draggability
        )
        self.setIniprocVisible(len(processes) != 0)

    def setPreProcessing(self, processes: Iterable, icons: Iterable):
        """

        :param processes: processes to display
        :param icons: icons associated to the processes if any
        """
        draggability = [False] * len(processes)
        self._preProcessWidgets.setProcesses(
            processes=processes, icons=icons, draggability=draggability
        )
        self.setPreProcVisible(len(processes) != 0)

    def setPhaseProcessing(self, processes: Iterable, icons: Iterable):
        """

        :param processes: processes to display
        :param icons: icons associated to the processes if any
        """
        draggability = [False] * len(processes)
        self._phaseProcessWidgets.setProcesses(
            processes=processes, icons=icons, draggability=draggability
        )
        self.setPhaseVisible(len(processes) != 0)

    def setProcessing(self, processes: Iterable, icons: Iterable):
        """

        :param processes: processes to display
        :param icons: icons associated to the processes if any
        """
        draggability = [False] * len(processes)
        self._processWidgets.setProcesses(
            processes=processes, icons=icons, draggability=draggability
        )
        self.setProcVisible(len(processes) != 0)

    def setPostProcessing(self, processes: Iterable, icons: Iterable):
        """

        :param processes: processes to display
        :param icons: icons associated to the processes if any
        """
        draggability = [False] * len(processes)
        self._postProcessWidgets.setProcesses(
            processes=processes, icons=icons, draggability=draggability
        )
        self.setPostVisible(len(processes) != 0)

    def getIniProcessingFlow(self) -> list:
        """

        :return: list of initialization processes
        """
        return self._iniProcessWidgets.getFlow()

    def getPreProcessingFlow(self):
        """

        :return: list of preprocessing
        """
        return self._preProcessWidgets.getFlow()

    def getProcessingFlow(self):
        """

        :return: list of processing
        """
        return self._processWidgets.getFlow()

    def getPostProcessingFlow(self):
        """

        :return: list of postprocessing
        """
        return self._postProcessWidgets.getFlow()

    def getFlow(self) -> dict:
        """
        Returns the concatenation of pre-processing, processing, and post-processing flows.

        :return: Dictionary where the keys are Nabu stages, and the values are lists of flows for each stage.
        :rtype: dict

        This method fetches the processing flows for all stages and returns them
        as a dictionary, allowing easy access to the current configuration.
        """
        return {
            _NabuStages.INI: self._iniProcessWidget.getFlow(),
            _NabuStages.PRE: self._preProcessWidgets.getFlow(),
            _NabuStages.PHASE: self._phaseProcessWidget.getFlow(),
            _NabuStages.PROC: self._processWidgets.getFlow(),
            _NabuStages.POST: self._processWidgets.getFlow(),
        }

    def getProcessFocused(self) -> tuple:
        """

        :return: the process under focus
        """
        stages = (
            _NabuStages.INI,
            _NabuStages.PRE,
            _NabuStages.PHASE,
            _NabuStages.PROC,
            _NabuStages.POST,
        )
        widgets = (
            self._iniProcessWidgets,
            self._preProcessWidgets,
            self._phaseProcessWidgets,
            self._processWidgets,
            self._postProcessWidgets,
        )
        for stage, widget in zip(stages, widgets):
            process_id = widget.getProcessFocused()
            if process_id is not None:
                return stage, process_id
        return None, None

    def _removeActiveProcess(self):
        for widget in (
            self._iniProcessWidgets,
            self._preProcessWidgets,
            self._phaseProcessWidgets,
            self._processWidgets,
            self._postProcessWidgets,
        ):
            if widget.hasProcessFocus():
                widget._removeActiveProcess()

        self.sigConfigurationChanged.emit((None, None))


class NabuFlowArea(qt.QWidget):
    """Define the flow dedicated to nabu"""

    sigConfigurationChanged = qt.Signal(tuple)
    """signal emitted when the `focus` process on the flow is changed.
    tuple is (stage, option)"""
    sigResetConfiguration = qt.Signal()
    """Signal emitted when the configuration should be reset"""

    def __init__(self, parent, direction):
        qt.QWidget.__init__(self, parent=parent)
        direction = FlowDirection(direction)

        if direction is FlowDirection.VERTICAL:
            self.setLayout(qt.QHBoxLayout(self))
        else:
            self.setLayout(qt.QVBoxLayout(self))

        self._control = NabuFlowControl(parent=self, direction=direction)
        self._control.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self._addRmWidget = _AddRemoveProcessWidget(parent=self, direction=direction)
        self._addRmWidget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self._control.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)

        if direction is FlowDirection.VERTICAL:
            # if vertical illustration left sided
            self.layout().addWidget(self._control)
            self.layout().addWidget(self._addRmWidget)
        else:
            # if horizontal illustration bottom sided
            self.layout().addWidget(self._control)
            self.layout().addWidget(self._addRmWidget)

        # set up
        # for now hide the add and remove option
        self._addRmWidget.setVisible(False)

        # connect signal / slot
        self._addRmWidget.sigRmProcess.connect(self._control._removeActiveProcess)
        self._control.sigConfigurationChanged.connect(self.sigConfigurationChanged)
        self._control.sigResetConfiguration.connect(self.sigResetConfiguration)

    @docstring(NabuFlowControl)
    def setIniProcessing(self, processes, icons):
        return self._control.setIniProcessing(processes=processes, icons=icons)

    @docstring(NabuFlowControl)
    def setPreProcessing(self, processes, icons):
        return self._control.setPreProcessing(processes=processes, icons=icons)

    @docstring(NabuFlowControl)
    def setPhaseProcessing(self, processes, icons):
        return self._control.setPhaseProcessing(processes=processes, icons=icons)

    @docstring(NabuFlowControl)
    def setProcessing(self, processes, icons):
        return self._control.setProcessing(processes=processes, icons=icons)

    @docstring(NabuFlowControl)
    def setPostProcessing(self, processes, icons):
        return self._control.setPostProcessing(processes=processes, icons=icons)

    @docstring(NabuFlowControl)
    def getFlow(self):
        return self._control.getFlow()

    @docstring(NabuFlowControl)
    def getProcessFocused(self):
        return self._control.getProcessFocused()


class _AddRemoveProcessWidget(qt.QWidget):
    sigAddProcess = qt.Signal()
    """Signal emitted when the user request a process to be added"""

    sigRmProcess = qt.Signal()
    """Signal emitted when the user request a process to be removed"""

    def __init__(self, parent, direction):
        qt.QWidget.__init__(self, parent=parent)
        if direction is FlowDirection.VERTICAL:
            self.setLayout(qt.QVBoxLayout())
            spacer_size_policy = (qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        else:
            self.setLayout(qt.QHBoxLayout())
            spacer_size_policy = (qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        add_icon = icons.getQIcon("add")
        rm_icon = icons.getQIcon("rm")

        self._addButton = qt.QPushButton(add_icon, "", self)
        self._addButton.setToolTip("add process")
        self._rmButton = qt.QPushButton(rm_icon, "", self)
        self._rmButton.setToolTip("remove process")
        spacer = qt.QWidget(parent=self)
        spacer.setSizePolicy(*spacer_size_policy)
        self.layout().addWidget(spacer)
        self.layout().addWidget(self._addButton)
        self.layout().addWidget(self._rmButton)

        # connect signal / slot
        self._addButton.pressed.connect(self._addProcess)
        self._rmButton.pressed.connect(self.sigRmProcess)

    def _addProcess(self):
        # should be able to add a process from ini, post, processing and pre

        raise NotImplementedError(" not implemented, to be defined")

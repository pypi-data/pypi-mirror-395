from __future__ import annotations

import os
import re
import logging
from functools import lru_cache as cache

from silx.gui import qt
from sluurp.utils import get_partitions, get_partition_gpus, get_partition_walltime

from tomwer.core.settings import SlurmSettings, SlurmSettingsMode
from tomwer.gui import icons
from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.configuration.action import (
    BasicConfigurationAction,
    ExpertConfigurationAction,
)
from tomwer.gui.configuration.level import ConfigurationLevel

from nxtomomill.models.utils import convert_str_to_tuple

_logger = logging.getLogger(__name__)


class SlurmSettingsDialog(qt.QDialog):
    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(qt.QVBoxLayout())
        self._mainWidget = SlurmSettingsWindow(parent=self)
        self._mainWidget.setWindowFlags(qt.Qt.Widget)
        self.layout().addWidget(self._mainWidget)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Close
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        self._buttons.button(qt.QDialogButtonBox.Close).clicked.connect(self.close)

        # connect signal /slot
        self._mainWidget.sigConfigChanged.connect(self.sigConfigChanged)

    def isSlurmActive(self):
        return self._mainWidget.isSlurmActive()

    def getConfiguration(self) -> dict:
        return self._mainWidget.getConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self._mainWidget.setConfiguration(config=config)


class SlurmSettingsWindow(qt.QMainWindow):
    """
    Main window to define slurm settings.
    Composed of the SlurmSettingsWidget and a combobox with some predefined settings
    """

    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        super().__init__(parent)

        # define toolbar
        toolbar = qt.QToolBar(self)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        self.__configurationModesAction = qt.QAction(self)
        self.__configurationModesAction.setCheckable(False)
        menu = qt.QMenu(self)
        self.__configurationModesAction.setMenu(menu)
        toolbar.addAction(self.__configurationModesAction)

        self.__configurationModesGroup = qt.QActionGroup(self)
        self.__configurationModesGroup.setExclusive(True)
        self.__configurationModesGroup.triggered.connect(self._userModeChanged)

        self._basicConfigAction = BasicConfigurationAction(toolbar)
        menu.addAction(self._basicConfigAction)
        self.__configurationModesGroup.addAction(self._basicConfigAction)
        self._expertConfiguration = ExpertConfigurationAction(toolbar)
        menu.addAction(self._expertConfiguration)
        self.__configurationModesGroup.addAction(self._expertConfiguration)

        # define maini widget
        self._mainWidget = qt.QWidget(self)
        self._mainWidget.setLayout(qt.QFormLayout())

        self._modeCombox = qt.QComboBox(self)
        self._mainWidget.layout().addRow("configuration: ", self._modeCombox)
        self._modeCombox.addItems([item.value for item in SlurmSettingsMode])
        self._modeCombox.setCurrentText(SlurmSettingsMode.GENERIC.value)

        self._settingsWidget = SlurmSettingsWidget(self, jobLimitation=None)
        self._mainWidget.layout().addRow(self._settingsWidget)

        self.setCentralWidget(self._mainWidget)

        # set up
        self._reloadPredefinedSettings()
        self._basicConfigAction.setChecked(True)
        self._userModeChanged(self._basicConfigAction)

        # connect signal / slot
        self._modeCombox.currentIndexChanged.connect(self._reloadPredefinedSettings)
        self._settingsWidget.sigConfigChanged.connect(self._configChanged)
        self._modeCombox.currentIndexChanged.connect(self.sigConfigChanged)
        # when the settings widget is edited them we automatically move to 'manual' settings. To notify visually the user
        self._settingsWidget.sigConfigChanged.connect(self._switchToManual)

    def _userModeChanged(self, action):
        self.__configurationModesAction.setIcon(action.icon())
        self.__configurationModesAction.setToolTip(action.tooltip())
        if action is self._basicConfigAction:
            level = ConfigurationLevel.OPTIONAL
        elif action is self._expertConfiguration:
            level = ConfigurationLevel.ADVANCED
        else:
            raise NotImplementedError
        self._settingsWidget.setConfigurationLevel(level)

    def _reloadPredefinedSettings(self, *args, **kkwargs):
        """
        reload settings from some predefined configuration
        """
        mode = self.getCurrentSettingsMode()
        settingsClass = SlurmSettingsMode.get_settings_class(mode)
        if settingsClass:
            with block_signals(self._settingsWidget):
                self.setConfiguration(
                    {
                        "cpu-per-task": settingsClass.N_CORES_PER_TASK,
                        "n_tasks": settingsClass.N_TASKS,
                        "n_jobs": settingsClass.N_JOBS,
                        "memory": settingsClass.MEMORY_PER_WORKER,
                        "partition": settingsClass.PARTITION,
                        "n_gpus": settingsClass.N_GPUS_PER_WORKER,
                        "job_name": settingsClass.PROJECT_NAME,
                        "walltime": settingsClass.DEFAULT_WALLTIME,
                        "python_venv": settingsClass.PYTHON_VENV,
                        "modules": settingsClass.MODULES_TO_LOAD,
                    }
                )

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def _switchToManual(self):
        self._modeCombox.setCurrentText(SlurmSettingsMode.MANUAL.value)

    def getCurrentSettingsMode(self) -> SlurmSettingsMode:
        return SlurmSettingsMode(self._modeCombox.currentText())

    def setCurrentSettingsMode(self, mode: SlurmSettingsMode) -> SlurmSettingsMode:
        mode = SlurmSettingsMode(mode)
        self._modeCombox.setCurrentText(mode.value)

    def setMode(self, mode: SlurmSettingsMode) -> None:
        """Alias for setCurrentSettingsMode(), used by SlurmClusterOW."""
        self.setCurrentSettingsMode(mode)

    def mode(self) -> SlurmSettingsMode:
        """Alias for getCurrentSettingsMode(), used by SlurmClusterOW."""
        return self.getCurrentSettingsMode()

    # expose API
    def getConfiguration(self) -> dict:
        return self._settingsWidget.getConfiguration()

    def getSlurmClusterConfiguration(self) -> dict:
        return self._settingsWidget.getSlurmClusterConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self._settingsWidget.setConfiguration(config=config)

    def isSlurmActive(self):
        return self._settingsWidget.isSlurmActive()


class SlurmSettingsWidget(qt.QWidget):
    """Widget used to define Slurm configuration to be used"""

    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    WALL_TIME_INVALID_COLOR = qt.QColor("#FF0000")

    def __init__(
        self,
        parent=None,
        n_gpu=SlurmSettings.N_GPUS_PER_WORKER,
        jobLimitation: int | None = 1,
    ) -> None:
        """
        :param n_gpu: if provided will set the value to the number of gpu requested
                          (default is one as most of the job are nabu reconstruction)
        :param jobLimitation: if set then will hide the option to define the number of job
        """
        super().__init__(parent=parent)
        self.setLayout(qt.QGridLayout())
        """Action to display warning in case of possible 'wrong' setting"""
        # define some optional warning
        warning_icon = icons.getQIcon("warning")
        self._warning_opd_p9 = qt.QLabel("")
        self._warning_opd_p9.setPixmap(warning_icon.pixmap(20, state=qt.QIcon.On))
        self._warning_opd_p9.setToolTip(
            f"'{get_login()}' account cannot submit job on p9 architecture"
        )
        self._warning_opd_export_opts = qt.QLabel("")
        self._warning_opd_export_opts.setPixmap(
            warning_icon.pixmap(20, state=qt.QIcon.On)
        )
        self._warning_opd_export_opts.setToolTip(
            f"'{get_login()}' account needs to export job with ALL option (advanced settings)"
        )

        # queues
        self._queueLabel = qt.QLabel("queue / partition")
        self.layout().addWidget(self._queueLabel, 0, 0, 1, 1)
        self._queueCB = qt.QComboBox(self)
        self._queueCB.setEditable(True)
        for partition in get_partitions():
            if partition in ("nice*",):
                # filter some node that we cannot access in fact
                continue
            self._queueCB.addItem(partition)
        self.layout().addWidget(self._queueCB, 0, 1, 1, 1)
        self.layout().addWidget(self._warning_opd_p9, 0, 2, 1, 1)

        # n workers
        self._nWorkersLabel = qt.QLabel("number of task", self)
        self.layout().addWidget(self._nWorkersLabel, 1, 0, 1, 1)
        self._nWorkersSP = qt.QSpinBox(self)
        self._nWorkersSP.setRange(1, 100)
        self.layout().addWidget(self._nWorkersSP, 1, 1, 1, 1)

        # ncores active
        self._nCoresLabel = qt.QLabel("number of cores per task")
        self.layout().addWidget(self._nCoresLabel, 2, 0, 1, 1)
        self._nCoresSB = qt.QSpinBox(self)
        self._nCoresSB.setRange(1, 500)
        self.layout().addWidget(self._nCoresSB, 2, 1, 1, 1)

        # memory
        self._memoryLabel = qt.QLabel("memory per task")
        self.layout().addWidget(self._memoryLabel, 3, 0, 1, 1)
        self._memorySB = qt.QSpinBox(self)
        self._memorySB.setRange(1, 10000)
        self._memorySB.setSuffix("GB")
        self.layout().addWidget(self._memorySB, 3, 1, 1, 1)

        # gpu
        self._nGpuLabel = qt.QLabel("number of GPUs per task")
        self.layout().addWidget(self._nGpuLabel, 4, 0, 1, 1)
        self._nGpuSB = qt.QSpinBox(self)
        self._nGpuSB.setRange(0, 12)
        self.layout().addWidget(self._nGpuSB, 4, 1, 1, 1)

        # n jobs
        self._nJobsLabel = qt.QLabel("number of job", self)
        self.layout().addWidget(self._nJobsLabel, 5, 0, 1, 1)

        self._nJobs = qt.QSpinBox(self)
        self._nJobs.setRange(1, 100000)
        self._nJobs.setValue(1)
        self._nJobs.setToolTip("Define on how many part the job should be split in")
        self._nJobsLabel.setVisible(jobLimitation is None)
        self._nJobs.setVisible(jobLimitation is None)
        self.layout().addWidget(self._nJobs, 5, 1, 1, 1)

        # wall time
        self._wallTimeLabel = qt.QLabel("wall time", self)
        self.layout().addWidget(self._wallTimeLabel, 6, 0, 1, 1)
        self._wallTimeQLE = qt.QLineEdit("", self)
        self.__reWallTime = qt.QRegularExpression(
            r"[0-9]?[0-9]:[0-9]?[0-9]:[0-9]?[0-9]"
        )
        self._wallTimeQLE.setPlaceholderText("HH:MM:SS")
        self._wallTimeValidator = qt.QRegularExpressionValidator(
            self.__reWallTime, self
        )
        self._wallTimeQLE.setValidator(self._wallTimeValidator)
        self.layout().addWidget(self._wallTimeQLE, 6, 1, 1, 1)
        self.__defaultWallTimeBackgroundColor = self.palette().color(
            self._wallTimeQLE.backgroundRole()
        )
        self._warningWallTime = qt.QLabel("")
        self._warningWallTime.setPixmap(warning_icon.pixmap(20, state=qt.QIcon.On))
        self.layout().addWidget(self._warningWallTime, 6, 2, 1, 1)

        # python exe / modules
        self._preProcessingGroup = qt.QGroupBox("pre-processing", self)
        self._preProcessingGroup.setLayout(qt.QFormLayout())
        self._preProcessingButtonGroup = qt.QButtonGroup(self)
        self._preProcessingButtonGroup.setExclusive(True)
        self.layout().addWidget(self._preProcessingGroup, 10, 0, 1, 2)

        # python venv
        self._sourceScriptCB = qt.QRadioButton("source script (python venv)", self)
        self._pythonVenv = qt.QLineEdit("/scisoft/tomotools/activate stable", self)
        self._preProcessingButtonGroup.addButton(self._sourceScriptCB)
        self._pythonVenv.setToolTip(
            """
            Optional path to a bash script to source before executing the script.
            """
        )
        self._preProcessingGroup.layout().addRow(self._sourceScriptCB, self._pythonVenv)
        # module
        self._modulesQLE = qt.QLineEdit(", ".join(SlurmSettings.MODULES_TO_LOAD), self)
        self._modulesCB = qt.QRadioButton("module(s) to load", self)
        self._preProcessingButtonGroup.addButton(self._modulesCB)
        self._preProcessingGroup.setToolTip(
            """
            Optional list of modules to load before executing the script. each module must be separated by a coma
            """
        )
        self._preProcessingGroup.layout().addRow(self._modulesCB, self._modulesQLE)

        # job name
        self._job_nameQLabel = qt.QLabel("job name", self)
        self.layout().addWidget(self._job_nameQLabel, 13, 0, 1, 1)

        self._jobName = qt.QLineEdit("", self)
        self._jobName.setToolTip(
            """Job name. Can contains several keyword that will be formatted:
            - scan: will be replaced by the scan name
            - process: will be replaced by the process name (nabu slices, nabu volume...)
            - info: some extra information that can be provided by the process to `specify` the processing
            note: those key word have to be surrounding by surrounded `{` and `}` in order to be formatted.
            """
        )
        self.layout().addWidget(self._jobName, 13, 1, 1, 1)

        # port
        # fixme: replace by a dedicated widget / validator for TCP adress
        self._portLabel = qt.QLabel("port", self)
        self.layout().addWidget(self._portLabel, 14, 0, 1, 1)
        self._port = _PortRangeSelection(self)
        self._port.setRange(0, 99999)
        self._port.setToolTip("TCP Port for the dask-distributed scheduler")
        self.layout().addWidget(self._port, 14, 1, 1, 1)

        # dashboard port
        self._dashboardPort = qt.QSpinBox(self)
        self.layout().addWidget(self._dashboardPort, 15, 0, 1, 1)
        self._dashboardPort.setRange(0, 99999)
        self._dashboardPort.setToolTip("TCP Port for the dashboard")
        self._dashboardPortLabel = qt.QLabel("dashboard port", self)
        self.layout().addWidget(self._dashboardPort, 15, 1, 1, 1)

        # sbatch advance parameters
        self._sbatchAdvancedParameters = qt.QGroupBox("sbatch advanced settings", self)
        self._sbatchAdvancedParameters.setLayout(qt.QFormLayout())
        self.layout().addWidget(self._sbatchAdvancedParameters, 16, 0, 1, 2)

        ## export parameter
        self._exportValueCM = qt.QComboBox(self)
        self._exportValueCM.addItems(("NONE", "ALL"))
        self._exportValueCM.setItemData(
            self._exportValueCM.findText("NONE"),
            """
            Only SLURM_* variables from the user environment will be defined. User must use absolute path to the binary to be executed that will define the environment. User can not specify explicit environment variables with "NONE". However, Slurm will then implicitly attempt to load the user's environment on the node where the script is being executed, as if --get-user-env was specified. \nThis option is particularly important for jobs that are submitted on one cluster and execute on a different cluster (e.g. with different paths). To avoid steps inheriting environment export settings (e.g. "NONE") from sbatch command, the environment variable SLURM_EXPORT_ENV should be set to "ALL" in the job script.
            """,
        )
        self._exportValueCM.setItemData(
            self._exportValueCM.findText("ALL"),
            """
            All of the user's environment will be loaded (either from the caller's environment or from a clean environment if --get-user-env is specified). \nCan fail when submitting cross-platform jobs and user has some module loaded
            """,
        )
        self._exportValueCM.setCurrentText("ALL")
        self._sbatchAdvancedParameters.layout().addRow("--export", self._exportValueCM)
        self.layout().addWidget(self._warning_opd_export_opts, 16, 2, 1, 1)

        ## gpu card
        self._gpuCardCB = qt.QComboBox(self)
        self._gpuCardCB.setToolTip(
            "Specify a GPU card to be used. Using the -C command from sbatch"
        )
        self._gpuCardCB.setEditable(
            True
        )  # let the user the ability to provide a GPU that is not found for now (expecting he knows what he is doing)
        self._sbatchAdvancedParameters.layout().addRow("-C (gpu card)", self._gpuCardCB)

        # simplify gui
        self._dashboardPort.hide()
        self._dashboardPortLabel.hide()
        self._jobName.hide()
        self._job_nameQLabel.hide()
        self._portLabel.hide()  # for now we don't use the port. This can be done automatically
        self._port.hide()  # for now we don't use the port. This can be done automatically
        # for now nworker == ntask is not used
        self._nWorkersSP.setVisible(False)
        self._nWorkersLabel.setVisible(False)

        # set up the gui
        self._nCoresSB.setValue(SlurmSettings.N_CORES_PER_TASK)
        self._nWorkersSP.setValue(SlurmSettings.N_TASKS)
        self._memorySB.setValue(SlurmSettings.MEMORY_PER_WORKER)
        if self._queueCB.findText(SlurmSettings.PARTITION) >= 0:
            self._queueCB.setCurrentText(SlurmSettings.PARTITION)
        self._nGpuSB.setValue(n_gpu)
        self._jobName.setText(SlurmSettings.PROJECT_NAME)
        self._wallTimeQLE.setText(SlurmSettings.DEFAULT_WALLTIME)
        self._modulesCB.setChecked(True)  # by default we go for modules
        self._warning_opd_p9.setVisible(False)
        self._warning_opd_export_opts.setVisible(False)
        self._warningWallTime.setVisible(False)
        self._preProcessingModeChanged()
        self._partitionChanged()
        self._sbatchAdvancedSettingsChanged()
        self._nGpuChanged()

        # connect signal / slot
        self._nCoresSB.valueChanged.connect(self._configurationChanged)
        self._nWorkersSP.valueChanged.connect(self._configurationChanged)
        self._memorySB.valueChanged.connect(self._configurationChanged)
        self._queueCB.currentTextChanged.connect(self._configurationChanged)
        self._queueCB.currentTextChanged.connect(self._updateWallTimeWarnings)
        self._queueCB.currentTextChanged.connect(self._updateWallTimeTooltip)
        self._nGpuSB.valueChanged.connect(self._configurationChanged)
        self._jobName.editingFinished.connect(self._configurationChanged)
        self._wallTimeQLE.editingFinished.connect(self._configurationChanged)
        self._wallTimeQLE.editingFinished.connect(self._updateWallTimeWarnings)
        self._wallTimeQLE.editingFinished.connect(self._updateWallTimeTooltip)
        self._pythonVenv.editingFinished.connect(self._configurationChanged)
        self._modulesQLE.editingFinished.connect(self._configurationChanged)
        self._preProcessingButtonGroup.buttonClicked.connect(self._configurationChanged)
        self._port.sigRangeChanged.connect(self._configurationChanged)
        self._dashboardPort.valueChanged.connect(self._configurationChanged)
        self._preProcessingButtonGroup.buttonClicked.connect(
            self._preProcessingModeChanged
        )
        self._queueCB.currentTextChanged.connect(self._partitionChanged)
        self._nGpuSB.valueChanged.connect(self._nGpuChanged)
        self._gpuCardCB.currentTextChanged.connect(self._configurationChanged)
        self._exportValueCM.currentIndexChanged.connect(self._configurationChanged)
        self._exportValueCM.currentIndexChanged.connect(
            self._sbatchAdvancedSettingsChanged
        )

    def _updateWallTimeWarnings(self):
        time_limit, _ = self._getPartitionWallTime(partition=self.getQueue())
        palette = self._wallTimeQLE.palette()
        wall_time_limit_exceed = time_limit is not None and _WallTime(
            self.getWallTime()
        ) > _WallTime(time_limit)
        if wall_time_limit_exceed:
            palette.setColor(self.backgroundRole(), self.WALL_TIME_INVALID_COLOR)
        else:
            palette.setColor(
                self.backgroundRole(), self.__defaultWallTimeBackgroundColor
            )
        self._warningWallTime.setVisible(wall_time_limit_exceed)
        self._wallTimeQLE.setPalette(palette)

    def _updateWallTimeTooltip(self):
        partition = self.getQueue()
        time_limit, default_wall_time = self._getPartitionWallTime(partition=partition)
        if time_limit is not None and default_wall_time is not None:
            tooltip = "\n".join(
                (
                    f"for partition {partition}:",
                    f"time limit: {time_limit}",
                    f"default limit: {default_wall_time}",
                )
            )
        else:
            tooltip = f"no wall time found for {partition}"
        self._wallTimeQLE.setToolTip(tooltip)
        self._warningWallTime.setToolTip(tooltip)

    def _nGpuChanged(self, *args, **kwargs):
        nGpu = self.getNGPU()
        self._gpuCardCB.setEnabled(nGpu > 0)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getNCores(self) -> int:
        return self._nCoresSB.value()

    def setNCores(self, n: int) -> None:
        self._nCoresSB.setValue(int(n))

    def getNWorkers(self) -> int:
        return self._nWorkersSP.value()

    def setNWorkers(self, n) -> None:
        self._nWorkersSP.setValue(int(n))

    def getMemory(self) -> int:
        return self._memorySB.value()

    def setMemory(self, memory: int) -> None:
        self._memorySB.setValue(int(memory))

    def getQueue(self) -> str:
        return self._queueCB.currentText()

    def setQueue(self, text: str) -> None:
        self._queueCB.setCurrentText(text)

    def getNGPU(self) -> int:
        return self._nGpuSB.value()

    def setNGPU(self, n: int) -> None:
        self._nGpuSB.setValue(int(n))

    def getNJobs(self) -> int:
        return self._nJobs.value()

    def setNJobs(self, value: int):
        self._nJobs.setValue(int(value))

    def getProjectName(self):
        return self._jobName.text()

    def setProjectName(self, name):
        self._jobName.setText(name)

    def getWallTime(self):
        parts = self._wallTimeQLE.text().split(":")
        hours = parts[0]
        if len(parts) > 1:
            minutes = parts[1]
        else:
            minutes = ""
        if len(parts) > 2:
            seconds = parts[2]
        else:
            seconds = ""

        return ":".join(
            [
                hours.zfill(2),
                minutes.zfill(2),
                seconds.zfill(2),
            ]
        )

    def setWallTime(self, walltime):
        self._wallTimeQLE.setText(walltime)
        self._updateWallTimeWarnings()
        self._updateWallTimeTooltip()

    def getPythonExe(self):
        if self._sourceScriptCB.isChecked():
            return self._pythonVenv.text()
        else:
            return None

    def setPythonExe(self, python_venv):
        self._pythonVenv.setText(python_venv)
        if python_venv != "":
            self._sourceScriptCB.setChecked(True)

    def getModulesToLoad(self) -> tuple:
        if self._modulesCB.isChecked():
            return convert_str_to_tuple(self._modulesQLE.text())
        else:
            return tuple()

    def setModulesToLoad(self, modules: tuple):
        if not isinstance(modules, (tuple, list)):
            raise TypeError(
                f"modules is expected to be a tuple or a list. Get {type(modules)} instead"
            )
        self._modulesQLE.setText(str(modules))
        if len(modules) > 0:
            self._modulesCB.setChecked(True)

    def getGpuCard(self) -> str | None:
        card = self._gpuCardCB.currentText()
        if card == "any" or self._nGpuSB == 0:
            return None
        else:
            return card

    def getSBatchExtraParams(self):
        return {
            "export": self._exportValueCM.currentText(),
            "gpu_card": self.getGpuCard(),
        }

    def setSBatchExtraParams(self, params: dict):
        export_ = params.get("export", None)
        if export_ is not None:
            index = self._exportValueCM.findText(export_)
            if index >= 0:
                self._exportValueCM.setCurrentIndex(index)
        gpu_card = params.get("gpu_card", None)
        if gpu_card is not None:
            index = self._gpuCardCB.findText("gpu_card")
            if index >= 0:
                self._gpuCardCB.setCurrentIndex(index)
            else:
                # policy when setting the extra params: if doesn't exists / found then won't set it.
                # because they can be part of .ows, this parameter is hidden by default.
                # so safer to use 'any' in the case it is unknown (debatable).
                _logger.warning(f"unable to find gpu {gpu_card}. Won't set it")

    def setConfiguration(self, config: dict) -> None:
        with block_signals(self):
            active_slurm = config.get("active_slurm", None)
            if active_slurm is not None:
                self._slurmCB.setChecked(active_slurm)

            n_cores = config.get("cpu-per-task", None)
            if n_cores is not None:
                self.setNCores(n_cores)

            n_workers = config.get("n_tasks", None)
            if n_workers is not None:
                self.setNWorkers(n_workers)

            memory = config.get("memory", None)
            if memory is not None:
                if isinstance(memory, str):
                    memory = memory.replace(" ", "").lower().rstrip("gb")
                self.setMemory(int(memory))

            queue_ = config.get("partition", None)
            if queue_ is not None:
                queue_ = queue_.rstrip("'").rstrip('"')
                queue_ = queue_.lstrip("'").lstrip('"')
                self.setQueue(queue_)

            n_gpu = config.get("n_gpus", None)
            if n_gpu is not None:
                self.setNGPU(int(n_gpu))

            project_name = config.get("job_name", None)
            if project_name is not None:
                self.setProjectName(project_name)

            wall_time = config.get("walltime", None)
            if wall_time is not None:
                self.setWallTime(wall_time)

            python_venv = config.get("python_venv", None)
            if python_venv is not None:
                python_venv = python_venv.rstrip("'").rstrip('"')
                python_venv = python_venv.lstrip("'").lstrip('"')
                self.setPythonExe(python_venv)

            modules = config.get("modules", None)
            if modules is not None:
                modules = convert_str_to_tuple(modules)
                self.setModulesToLoad(modules)

            sbatch_extra_params = config.get("sbatch_extra_params", {})
            self.setSBatchExtraParams(sbatch_extra_params)

            n_jobs = config.get("n_jobs", None)
            if n_jobs is not None:
                self.setNJobs(n_jobs)
            self._preProcessingModeChanged()  # make sure modules and python venv is enabled according to the activate mode

        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        config = {
            "cpu-per-task": self.getNCores(),
            "n_tasks": self.getNWorkers(),
            "n_jobs": self.getNJobs(),
            "memory": self.getMemory(),
            "partition": self.getQueue(),
            "n_gpus": self.getNGPU(),
            "job_name": self.getProjectName(),
            "walltime": self.getWallTime(),
            "sbatch_extra_params": self.getSBatchExtraParams(),
        }
        if self._modulesCB.isChecked():
            config["modules"] = self.getModulesToLoad()
        elif self._sourceScriptCB.isChecked():
            config["python_venv"] = self.getPythonExe()
        else:
            raise ValueError("'modules' or python environment should be enable")
        return config

    def getSlurmClusterConfiguration(self):
        from tomwer.core.cluster import SlurmClusterConfiguration

        return SlurmClusterConfiguration().from_dict(self.getConfiguration())

    def _preProcessingModeChanged(self):
        self._modulesQLE.setEnabled(self._modulesCB.isChecked())
        self._pythonVenv.setEnabled(self._sourceScriptCB.isChecked())

    def setConfigurationLevel(self, level: ConfigurationLevel):
        self._sbatchAdvancedParameters.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._wallTimeLabel.setVisible(level >= ConfigurationLevel.ADVANCED)
        self._wallTimeQLE.setVisible(level >= ConfigurationLevel.ADVANCED)

    def _partitionChanged(self, *args, **kwargs):
        partition = self.getQueue()
        # op(erator) accounts (from icc computers) cannot export to p9. they don't have home directories
        self._warning_opd_p9.setVisible(
            current_login_is_op_account() and partition.lower().startswith("p9")
        )
        gpus = self._getGpus(partition=partition)
        self._gpuCardCB.clear()
        self._gpuCardCB.addItems(gpus)
        self._gpuCardCB.setCurrentText("any")

    def _sbatchAdvancedSettingsChanged(self, *args, **kwargs):
        # op(erator) accounts (from icc computers) must export ALL environment variable. Else job fails
        # warning: we want to display the warning no matter if we are in 'advance options' or not.
        # this way the user always see the warning when necessary
        self._warning_opd_export_opts.setVisible(
            current_login_is_op_account()
            and self._exportValueCM.currentText() == "NONE"
        )

    @cache(maxsize=None)
    def _getGpus(self, partition) -> tuple:
        try:
            gpus = get_partition_gpus(partition)
        except Exception as e:
            _logger.error(f"Failed to detect GPU on {partition}. Error is {e}")
            gpus = ("any",)
        else:
            gpus = list(gpus) + [
                "any",
            ]
            return gpus

    @cache(maxsize=None)
    def _getPartitionWallTime(self, partition: str) -> tuple[str | None, str | None]:
        try:
            times = get_partition_walltime(partition=partition)
        except Exception:
            return None, None
        else:
            return times["time"], times["default_time"]


class _PortRangeSelection(qt.QWidget):
    sigRangeChanged = qt.Signal()
    """Signal emit when the port range change"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # from label
        self._fromLabel = qt.QLabel("from", self)
        self._fromLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._fromLabel)
        self._fromQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._fromQSpinBox)
        # to label
        self._toLabel = qt.QLabel("to", self)
        self._toLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._toLabel)
        self._toQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._toQSpinBox)
        # steps label
        self._stepLabel = qt.QLabel("step", self)
        self._stepLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._stepLabel)
        self._stepQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._stepQSpinBox)

        # connect signal / slot
        self._fromQSpinBox.valueChanged.connect(self._rangeChanged)
        self._toQSpinBox.valueChanged.connect(self._rangeChanged)
        self._stepQSpinBox.valueChanged.connect(self._rangeChanged)

    def _rangeChanged(self, *args, **kwargs):
        self.sigRangeChanged.emit()

    def getRange(self) -> tuple:
        return (
            self._fromQSpinBox.value(),
            self._toQSpinBox.value(),
            self._stepQSpinBox.value(),
        )

    def setRange(self, min_: int, max_: int, step: int | None = None) -> None:
        self._fromQSpinBox.setValue(min(min_, max_))
        self._toQSpinBox.setValue(max(min_, max_))
        if step is not None:
            self._stepQSpinBox.setValue(step)


def get_login() -> str | None:
    try:
        return os.getlogin()
    except OSError:
        """In CI computer this raises the following error
        OSError: [Errno 6] No such device or address
        """
        return None


def current_login_is_op_account() -> bool:
    """
    return True if the current login is a op[i]dXX login.
    """
    return is_op_account(get_login())


def is_op_account(user: str | None) -> bool:
    """
    Determines if a given username follows the 'op' account format,
    specifically 'opdXX' or 'opidXX', where 'XX' are numeric digits.

    Args:
        user (Optional[str]): The username to check.

    Returns:
        bool: True if the username matches the pattern, False otherwise.
    """

    if user is None:
        return False

    op_account_pattern = r"^opi?d\d{2}$"
    return bool(re.match(op_account_pattern, user))


class _WallTime:
    """Util class to compare two walltime provided as D-HH:MM:SS or as HH:MM:SS"""

    def __init__(self, walltime: str):
        parts = walltime.split("-")
        if len(parts) > 1:
            assert len(parts) == 2, f"unexpected walltime format ({walltime})"
            days = int(parts[0])
        else:
            days = 0

        def minutes_to_seconds(value):
            return value * 60

        def hours_to_seconds(value):
            return minutes_to_seconds(value * 60)

        def days_to_seconds(value):
            return hours_to_seconds(value * 24)

        hours, minutes, seconds = map(int, parts[-1].split(":"))
        self.value = (
            seconds
            + minutes_to_seconds(minutes)
            + hours_to_seconds(hours)
            + days_to_seconds(days)
        )

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

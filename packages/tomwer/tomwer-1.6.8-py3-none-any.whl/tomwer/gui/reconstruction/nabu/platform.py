from __future__ import annotations
from silx.gui import qt

from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.gui.utils.gpu import SelectGPUGroupBox


class NabuPlatformSettings(qt.QWidget, _NabuStageConfigBase):
    """define settings to be used for the local reconstruction like gpu..."""

    sigConfigChanged = qt.Signal()

    DEFAULT_GPU_FRACTION = 90
    DEFAULT_CPU_FRACTION = 90

    def __init__(self, parent: qt.QWidget | None = None) -> None:
        qt.QWidget.__init__(self, parent, stage=None)
        _NabuStageConfigBase.__init__(self, stage=None)

        self.setLayout(qt.QFormLayout())
        self._gpuSelWidget = SelectGPUGroupBox()
        self._gpuSelWidget.setChecked(False)
        # keep default behavior: don't set any default gpu
        self.layout().addRow(self._gpuSelWidget)

        # gpu percentage
        self._GPUFractionLabel = qt.QLabel("GPU percentage usage", self)
        self.registerWidget(self._GPUFractionLabel, "advanced")
        self._GPUFractionSB = qt.QSpinBox(self)
        self._GPUFractionSB.setSingleStep(10)
        self._GPUFractionSB.setSuffix("%")
        self._GPUFractionSB.setMinimum(1)
        self._GPUFractionSB.setMaximum(100)
        self._GPUFractionSB.setToolTip("Which fraction of GPU memory to use.")
        self.registerWidget(self._GPUFractionSB, "advanced")
        self.layout().addRow(self._GPUFractionLabel, self._GPUFractionSB)

        # cpu percentage
        self._CPUFractionLabel = qt.QLabel("CPU percentage usage", self)
        self.registerWidget(self._CPUFractionLabel, "advanced")
        self._CPUFractionSB = qt.QSpinBox(self)
        self._CPUFractionSB.setSingleStep(10)
        self._CPUFractionSB.setSuffix("%")
        self._CPUFractionSB.setMinimum(1)
        self._CPUFractionSB.setMaximum(100)
        self._CPUFractionSB.setToolTip("Which fraction of CPU memory to use.")
        self.registerWidget(self._CPUFractionSB, "advanced")
        self.layout().addRow(self._CPUFractionLabel, self._CPUFractionSB)

        # set up
        self._GPUFractionSB.setValue(NabuPlatformSettings.DEFAULT_GPU_FRACTION)
        self._CPUFractionSB.setValue(NabuPlatformSettings.DEFAULT_CPU_FRACTION)

        # connect signal / slot
        self._gpuSelWidget.sigGPUChanged.connect(self.sigConfigChanged)
        self._GPUFractionSB.valueChanged.connect(self._triggerSigConfChanged)
        self._CPUFractionSB.valueChanged.connect(self._triggerSigConfChanged)

    def getCPUFraction(self) -> float:
        return self._CPUFractionSB.value() / 100.0

    def setCPUFraction(self, value: float):
        return self._CPUFractionSB.setValue(int(value * 100.0))

    def getGPUFraction(self) -> float:
        return self._GPUFractionSB.value() / 100.0

    def setGPUFraction(self, value: float):
        return self._GPUFractionSB.setValue(int(value * 100.0))

    def _triggerSigConfChanged(self, *args, **kwargs) -> None:
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        config = {
            "gpu_mem_fraction": self.getGPUFraction(),
            "cpu_mem_fraction": self.getCPUFraction(),
        }
        selected_gpu_id = self._gpuSelWidget.getSelectedGPUId()
        if selected_gpu_id is not None:
            config["resources"] = {
                "gpu_id": selected_gpu_id,
            }
        return config

    def setConfiguration(self, config: dict) -> None:
        gpu_id = config.get("resources", {}).get("gpu_id", None)
        if gpu_id not in (None, ""):
            self._gpuSelWidget.setSelectedGPUId(value=gpu_id)
            self._gpuSelWidget.setChecked(True)
        if "gpu_mem_fraction" in config:
            self.setGPUFraction(config["gpu_mem_fraction"])
        if "cpu_mem_fraction" in config:
            self.setCPUFraction(config["cpu_mem_fraction"])

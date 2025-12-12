from __future__ import annotations

import logging

try:
    from nabu.cuda.utils import collect_cuda_gpus
except ImportError:
    raise
except Exception:
    _has_collect_cuda_gpus = False
else:
    # issue with cuda driver. see https://gitlab.esrf.fr/tomotools/tomwer/-/issues/1515
    _has_collect_cuda_gpus = True
from silx.gui import qt

_logger = logging.getLogger(__name__)


class SelectGPUGroupBox(qt.QGroupBox):
    """Interface to select a (local) GPU"""

    sigGPUChanged = qt.Signal()
    """Emit when the selected GPU changed"""

    def __init__(self, parent=None, title="select (local) GPU"):
        super().__init__(parent=parent, title=title)
        self.setCheckable(True)
        self.setLayout(qt.QFormLayout())
        if _has_collect_cuda_gpus:
            self.__cuda_gpus = collect_cuda_gpus() or {}
        else:
            _logger.warning("Fail to found cuda devices")
            self.__cuda_gpus = {}

        # warn user if no gpu found: reconstruction will work but will take way more time
        if len(self.__cuda_gpus) == 0:
            style = qt.QApplication.style()
            icon = style.standardIcon(qt.QStyle.SP_MessageBoxWarning)
            self.__iconLabel = qt.QLabel(parent=self)
            self.__iconLabel.setPixmap(icon.pixmap(80, 80))
            self.__noGPULabel = qt.QLabel("No cuda GPU detected")
            self.__noGPULabel.setToolTip(
                "No cuda GPU device detected. Reconstruction will be done on CPU which is much more slower"
            )
            self.layout().addRow(self.__iconLabel, self.__noGPULabel)

        self._gpusCB = qt.QComboBox(self)
        for gpu_id, gpu_desc in self.__cuda_gpus.items():
            name = gpu_desc.get("name", f"unknown gpu {gpu_id}")
            self._gpusCB.addItem(f"{name} (id-{gpu_id})", gpu_id)
        self.layout().addRow(self._gpusCB)

        # connect signal / slot
        self._gpusCB.currentIndexChanged.connect(self.__GPUChanged)

    @property
    def cuda_gpus(self) -> dict:
        return self.__cudaGPUs

    def getSelectedGPUId(self) -> int | None:
        if self.isChecked():
            selected_gpu = self._gpusCB.currentIndex()
            if selected_gpu == -1:
                return None
            else:
                return self._gpusCB.itemData(selected_gpu, qt.Qt.UserRole)
        else:
            return None

    def setSelectedGPUId(self, value: int):
        cb_index = self._gpusCB.findData(value, role=qt.Qt.UserRole)
        if cb_index >= 0:
            self._gpusCB.setCurrentIndex(cb_index)

    def __GPUChanged(self, *args, **kwargs):
        self.sigGPUChanged.emit()

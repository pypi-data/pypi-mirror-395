# coding: utf-8
from __future__ import annotations


import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.core.settings import SlurmSettings
from tomwer.gui.cluster.slurm import (
    is_op_account,
    SlurmSettingsMode,
    SlurmSettingsWidget,
    SlurmSettingsWindow,
    _WallTime,
)
from tomwer.tests.utils import skip_gui_test
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestSlurmWidget(TestCaseQt):
    def setUp(self):
        TestCaseQt.setUp(self)
        self.slurmWidget = SlurmSettingsWidget(parent=None)

    def tearDown(self):
        self.slurmWidget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.slurmWidget.close()
        self.slurmWidget = None

    def testGetConfiguration(self):
        dict_res = self.slurmWidget.getConfiguration()
        expected_dict = {
            "cpu-per-task": SlurmSettings.N_CORES_PER_TASK,
            "n_tasks": SlurmSettings.N_TASKS,
            "memory": SlurmSettings.MEMORY_PER_WORKER,
            "partition": "",
            "n_gpus": SlurmSettings.N_GPUS_PER_WORKER,
            "job_name": "tomwer_{scan}_-_{process}_-_{info}",
            "n_jobs": 1,
            "modules": ("tomotools/stable",),
            "walltime": "01:00:00",
            "sbatch_extra_params": {
                "export": "ALL",
                "gpu_card": None,
            },
        }
        assert dict_res == expected_dict, f"{dict_res} vs {expected_dict}"

    def testSetConfiguration(self):
        self.slurmWidget.setConfiguration(
            {
                "cpu-per-task": 2,
                "n_tasks": 3,
                "memory": 156,
                "partition": "test-queue",
                "n_gpus": 5,
                "modules": "mymodule, mysecond/10.3",
                "sbatch_extra_params": {
                    "export": "NONE",
                },
            }
        )

        assert self.slurmWidget.getNCores() == 2
        assert self.slurmWidget.getNWorkers() == 3
        assert self.slurmWidget.getMemory() == 156
        assert self.slurmWidget.getQueue() == "test-queue"
        assert self.slurmWidget.getNGPU() == 5
        assert self.slurmWidget.getSBatchExtraParams() == {
            "export": "NONE",
            "gpu_card": None,
        }


def test_SlurmSettingsWindow(qtapp):  # noqa F811
    """
    test that slurm SettingsWindow can load all the different slurm settings modes
    """
    widget = SlurmSettingsWindow()
    for mode in SlurmSettingsMode:
        widget.setCurrentSettingsMode(mode)
        widget.getConfiguration()


def test_is_op_account():
    assert is_op_account("opid19")
    assert not is_op_account("opid0")
    assert not is_op_account("dopid05")
    assert not is_op_account("opid")
    assert is_op_account("opd12")


def test__WallTime():
    assert _WallTime("11:00:02") > _WallTime("10:25:45")
    assert _WallTime("1-00:00:00") > _WallTime("10:25:45")
    assert _WallTime("01:00:0") < _WallTime("01:00:01")
    assert _WallTime("1-00:00:00") == _WallTime(
        "24:00:0"
    ), f"{_WallTime('1-00:00:00').value} != {_WallTime('24:00:0').value} "

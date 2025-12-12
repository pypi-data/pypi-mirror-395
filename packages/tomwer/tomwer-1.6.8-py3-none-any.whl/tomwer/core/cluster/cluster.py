# coding: utf-8

"""
Contains processing relative to a `Slurmcluster`
"""

from __future__ import annotations

import logging
from tomwer.core.settings import SlurmSettings as _SlurmSettings

_logger = logging.getLogger(__name__)


class SlurmClusterConfiguration:
    """Object shipping the configuration of a slurm cluster"""

    def __init__(
        self,
        n_cpu_per_task=_SlurmSettings.N_CORES_PER_TASK,
        n_tasks=_SlurmSettings.N_TASKS,
        memory=_SlurmSettings.MEMORY_PER_WORKER,
        queue=_SlurmSettings.PARTITION,
        n_gpus=_SlurmSettings.N_GPUS_PER_WORKER,
        project_name=_SlurmSettings.PROJECT_NAME,
        walltime=_SlurmSettings.DEFAULT_WALLTIME,
        python_venv=_SlurmSettings.PYTHON_VENV,
        n_jobs=_SlurmSettings.N_JOBS,
        modules_to_load: tuple = _SlurmSettings.MODULES_TO_LOAD,
        sbatch_extra_params: dict = _SlurmSettings.SBATCH_EXTRA_PARAMS,
    ) -> None:
        self._n_cpu_per_task = n_cpu_per_task
        self._n_task = n_tasks
        self._memory = memory
        self._queue = queue
        self._n_gpus = n_gpus
        self._project_name = project_name
        self._walltime = walltime
        self._python_venv = python_venv
        self._modules_to_load = modules_to_load
        self._n_jobs = n_jobs
        self._sbatch_extra_params = sbatch_extra_params
        if python_venv not in (None, "") and len(modules_to_load) > 0:
            _logger.warning(
                "Either 'modules to load' of 'python venv' can be provided. Not both"
            )

    @property
    def n_cpu_per_task(self):
        return self._n_cpu_per_task

    @property
    def n_task(self):
        return self._n_task

    @property
    def memory(self):
        return self._memory

    @property
    def queue(self):
        return self._queue

    @property
    def n_gpus(self):
        return self._n_gpus

    @property
    def n_jobs(self):
        return self._n_jobs

    @property
    def project_name(self):
        return self._project_name

    @property
    def walltime(self):
        return self._walltime

    @property
    def python_venv(self):
        return self._python_venv

    @property
    def modules_to_load(self) -> tuple:
        return self._modules_to_load

    @property
    def port_range(self) -> tuple:
        """port range as (start:int, strop:int, step: int)"""
        return self._port_range

    @property
    def sbatch_extra_params(self) -> dict:
        return self._sbatch_extra_params

    @property
    def dashboard_port(self):
        return self._dashboard_port

    def to_dict(self) -> dict:
        return {
            "cpu-per-task": self.n_cpu_per_task,
            "n_tasks": self.n_task,
            "n_jobs": self.n_jobs,
            "memory": self.memory,
            "partition": self.queue,
            "n_gpus": self.n_gpus,
            "job_name": self.project_name,
            "walltime": self.walltime,
            "python_venv": self.python_venv,
            "modules": self.modules_to_load,
            "sbatch_extra_params": self.sbatch_extra_params,
        }

    @staticmethod
    def from_dict(dict_: dict):
        return SlurmClusterConfiguration().load_from_dict(dict_=dict_)

    def load_from_dict(self, dict_: dict):
        if "cpu-per-task" in dict_:
            self._n_cpu_per_task = dict_["cpu-per-task"]
        if "n_tasks" in dict_:
            self._n_task = dict_["n_tasks"]
        if "n_jobs" in dict_:
            self._n_jobs = dict_["n_jobs"]
        if "memory" in dict_:
            self._memory = dict_["memory"]
        if "partition" in dict_:
            self._queue = dict_["partition"]
        if "n_gpus" in dict_:
            self._n_gpus = dict_["n_gpus"]
        if "job_name" in dict_:
            self._project_name = dict_["job_name"]
        if "walltime" in dict_:
            self._walltime = dict_["walltime"]
        if "python_venv" in dict_:
            self._python_venv = dict_["python_venv"]
        modules = dict_.get("modules", None)
        if modules is not None:
            self._modules_to_load = modules
        if "port_range" in dict_:
            self._port_range = dict_["port_range"]
        if "dashboard_port" in dict_:
            self._dashboard_port = dict_["dashboard_port"]
        if "sbatch_extra_params" in dict_:
            self._sbatch_extra_params = dict_["sbatch_extra_params"]
        return self

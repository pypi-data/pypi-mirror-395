# coding: utf-8
"""
Utils for slurm
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sluurp.utils import has_sbatch_available


def is_slurm_available() -> bool:
    """
    Return True if the environment knows about slurm command (sbatch)
    """
    return has_sbatch_available()


def get_slurm_script_name(prefix: str | None = None) -> str:
    now_str = datetime.now().strftime("%y-%m-%d_%H:%M:%S")
    random_str = str(uuid.uuid4()).split("-")[0]
    suffix = f"{now_str}_{random_str}_.sh"
    if prefix in ("", None):
        return suffix
    else:
        return f"{prefix}_{suffix}"

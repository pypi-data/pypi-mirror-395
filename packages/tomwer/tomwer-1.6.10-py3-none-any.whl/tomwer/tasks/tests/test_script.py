# coding: utf-8
from __future__ import annotations

import os

from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.tasks.script.python import PythonScript


def test_python_script(tmp_path):

    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    dim = 10
    scan = MockNXtomo(
        scan_path=os.path.join(test_dir, "scan1"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=dim,
    ).scan

    task = PythonScript(
        inputs={
            "data": scan,
            "scriptText": "print('toto')",
        },
    )
    task.execute()

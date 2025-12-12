# coding: utf-8

from tomwer.core.process.visualization.diffviewer import _DiffViewerPlaceHolder


def test_diff_viewer():
    process = _DiffViewerPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

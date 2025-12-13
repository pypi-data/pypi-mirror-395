# coding: utf-8

from tomwer.core.process.visualization.dataviewer import _DataViewerPlaceHolder


def test_data_viewer():
    process = _DataViewerPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

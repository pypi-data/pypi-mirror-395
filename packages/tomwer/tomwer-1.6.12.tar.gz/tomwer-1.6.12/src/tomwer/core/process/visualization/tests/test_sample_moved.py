# coding: utf-8

from tomwer.core.process.visualization.imagestackviewer import (
    _ImageStackViewerPlaceHolder,
)


def test_sample_moved():
    process = _ImageStackViewerPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

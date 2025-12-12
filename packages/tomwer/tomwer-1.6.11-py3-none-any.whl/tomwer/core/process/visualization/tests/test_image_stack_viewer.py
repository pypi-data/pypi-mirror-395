# coding: utf-8

from tomwer.core.process.visualization.imagestackviewer import (
    _ImageStackViewerPlaceHolder,
)


def test_image_stack_viewer():
    process = _ImageStackViewerPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

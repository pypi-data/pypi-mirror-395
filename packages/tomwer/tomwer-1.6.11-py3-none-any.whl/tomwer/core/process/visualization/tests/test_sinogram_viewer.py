# coding: utf-8


from tomwer.core.process.visualization.sinogramviewer import _SinogramViewerPlaceHolder


def test_sinogram_viewer():
    process = _SinogramViewerPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

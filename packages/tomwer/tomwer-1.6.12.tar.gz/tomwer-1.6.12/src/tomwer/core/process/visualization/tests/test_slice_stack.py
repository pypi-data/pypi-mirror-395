# coding: utf-8


from tomwer.core.process.visualization.slicestack import _SliceStackPlaceHolder


def test_slice_stack():
    process = _SliceStackPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

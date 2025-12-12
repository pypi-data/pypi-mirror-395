# coding: utf-8

from tomwer.core.process.visualization.radiostack import _RadioStackPlaceHolder


def test_radio_stack():
    process = _RadioStackPlaceHolder(
        inputs={
            "data": None,
        }
    )
    process.run()

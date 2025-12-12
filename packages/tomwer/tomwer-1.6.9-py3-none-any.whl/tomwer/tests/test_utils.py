from __future__ import annotations

import pint
import numpy

from tomwer.utils import Launcher
from nxtomo.nxobject.nxtransformations import (
    get_lr_flip,
    get_ud_flip,
)

_ureg = pint.get_application_registry()


def test_launcher():
    launcher = Launcher(prog="tomwer", version="1.0")
    launcher.add_command(
        "canvas", module_name="tomwer.app.canvas", description="open the orange-canvas"
    )
    launcher.print_help()
    launcher.execute_help(["tomwer", "canvas"])


def is_lr_flip(transformations) -> bool:
    """sum all rotation the detector 'y' axis and check that the sum is 180 (in this case we consider this is a detector left-right flip)"""
    lr_rot_sum = sum(
        [trans.transformation_values for trans in get_lr_flip(transformations)]
    )
    assert isinstance(lr_rot_sum, pint.Quantity)
    return bool(
        numpy.isclose(
            lr_rot_sum,
            180.0 * _ureg.degree,
        )
    )


def is_ud_flip(transformations) -> bool:
    """sum all rotation the detector 'x' axis and check that the sum is 180 (in this case we consider this is a detector up-down flip)"""
    ud_rot_sum = sum(
        [trans.transformation_values for trans in get_ud_flip(transformations)]
    )
    assert isinstance(ud_rot_sum, pint.Quantity)
    return bool(
        numpy.isclose(
            ud_rot_sum,
            180.0 * _ureg.degree,
        )
    )

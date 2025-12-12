# coding: utf-8
from __future__ import annotations


from silx.gui import qt


class _IgnoreWheelBase:
    """QWidget ignoring "wheelEvent" and forwarding it to its parent in case this is a QScrollArea"""

    def wheelEvent(self, *args, **kwargs):
        pass


class QComboBoxIgnoreWheel(qt.QComboBox, _IgnoreWheelBase):
    pass


class QDoubleSpinBoxIgnoreWheel(qt.QDoubleSpinBox, _IgnoreWheelBase):
    pass


class QSpinBoxIgnoreWheel(qt.QSpinBox, _IgnoreWheelBase):
    pass

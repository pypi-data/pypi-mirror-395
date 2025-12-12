# coding: utf-8

"""
contains gui to select a slice in a volume
"""

from __future__ import annotations


from silx.gui import qt


class ControlWidget(qt.QWidget):
    """
    Widget to lock cor position or compute it or validate it and to
    display the cor value
    """

    sigComputationRequest = qt.Signal()
    """Signal emitted when user request a computation from the settings"""

    sigValidateRequest = qt.Signal()
    """Signal emitted when user validate the current settings"""

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        self._buttons = qt.QWidget(parent=self)
        self._buttons.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(self._buttons)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self._buttons.layout().addWidget(spacer)

        self._computeBut = qt.QPushButton("compute", parent=self)
        self._buttons.layout().addWidget(self._computeBut)
        style = qt.QApplication.style()
        applyIcon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)
        self._applyBut = qt.QPushButton(applyIcon, "validate", parent=self)
        self._buttons.layout().addWidget(self._applyBut)
        self.layout().addWidget(self._buttons)

        # make connection
        self._computeBut.pressed.connect(self.sigComputationRequest)
        self._applyBut.pressed.connect(self.sigValidateRequest)

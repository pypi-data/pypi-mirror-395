# coding: utf-8

"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""
from __future__ import annotations


from silx.gui import qt

from tomwer.core.process.conditions.filters import FileNameFilterTask
from tomwer.gui import icons
from tomwer.gui.utils.sandboxes import (
    RegularExpressionSandBox,
    RegularExpressionSandBoxDialog,
)


class FileNameFilterWidget(qt.QWidget):
    """
    Simple widget allowing the user to define a pattern and emitting a signal
    'sigValid' or 'sigUnvalid' if passing through the filter or not
    """

    sigValid = qt.Signal(str)
    """Signal emitted when the string pass through the filter"""
    sigUnvalid = qt.Signal(str)
    """Signal emitted when the string doesn't pass through the filter"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(qt.QGridLayout())

        self._invertCB = qt.QCheckBox("Invert filter action", parent=self)
        self._invertCB.setToolTip(
            "If not inverted and match the filter "
            "condition then let the scan pass through"
        )
        self.layout().addWidget(self._invertCB, 0, 0, 1, 3)

        self.layout().addWidget(qt.QLabel("filter type:", self), 1, 0)
        self._filterTypeCB = qt.QComboBox(parent=self)
        for filter_type in FileNameFilterTask.FILTER_TYPES:
            self._filterTypeCB.addItem(filter_type)
        self.layout().addWidget(self._filterTypeCB, 1, 1, 1, 2)

        self.layout().addWidget(qt.QLabel("pattern:", parent=self), 2, 0)
        self._patternLE = qt.QLineEdit(parent=self)
        self._patternLE.setToolTip(self.getPatternTooltip())
        self.layout().addWidget(self._patternLE, 2, 1)

        icon = icons.getQIcon("information")
        self._sandBoxPB = qt.QPushButton(icon=icon, parent=self)
        # self._sandBoxPB.setPixmap(icon.pixmap(qt.QSize(32, 32)))
        self._sandBoxPB.setToolTip(RegularExpressionSandBox.description())
        self._sandBoxPB.pressed.connect(self._showSandBox)
        self.layout().addWidget(self._sandBoxPB, 2, 2)

        # set up
        self._sandBoxPB.setVisible(False)
        self._filterTypeCB.setCurrentText(FileNameFilterTask._DEFAULT_FILTER_TYPE)

        self.sandboxDialog = None

    def _showSandBox(self):
        self.getSandboxDialog().show()

    def getSandboxDialog(self):
        if self.sandboxDialog is None:
            self.sandboxDialog = RegularExpressionSandBoxDialog(
                parent=None, pattern=self.getPattern()
            )
            self.sandboxDialog.setModal(False)
        return self.sandboxDialog

    def getPatternTooltip(self):
        return (
            "define the pattern to accept file using the python `re` "
            "library.\n"
            "For example if we two series of acquisition named serie_10_XXX\n"
            "and serie_100_YYY and we want to filter all the serie_10_XXX\n"
            'then we can define the pattern "serie_100_" \n'
            "which will only let the serie_100_YYY go through."
        )

    def _updateSandBoxPattern(self):
        self.getSandboxDialog().setPattern(self._patternLE.text())

    def getPattern(self) -> str:
        return self._patternLE.text()

    def setPattern(self, pattern):
        self._patternLE.setText(pattern)

    def unvalidPatternDefinition(self, pattern, error):
        """Overwrite NameFilter.unvalidPatternDefinition"""
        title = "regular expression %s is invalid" % pattern
        mess = qt.QMessageBox(
            qt.QMessageBox.warning, title, parent=self, text=str(error)
        )
        mess.setModal(False)
        mess.show()

    def setActiveFilter(self, filter_):
        valid_fiters = ("regular expression", "unix file name pattern")
        if filter_ not in valid_fiters:
            raise ValueError(
                f"filter is expected to be one of {valid_fiters}. Not {filter_}"
            )
        self._sandBoxPB.setVisible(filter_ == "regular expression")
        self._filterTypeCB.setCurrentText(filter_)

    def getActiveFilter(self):
        return self._filterTypeCB.currentText()

    def invertFilterAction(self):
        return self._invertCB.isChecked()

# coding: utf-8
from __future__ import annotations

from silx.gui import qt


class InputDialogWithCache(qt.QDialog):
    """
    Input dialog for get missing information for nxtomomill translation
    Identical to a default QInputDialog adding a CheckBox to store answer.
    """

    def __init__(self, parent, scan, title="", desc="", cache_answer=True):
        qt.QDialog.__init__(self, parent)
        self.setWindowFlags(qt.Qt.MSWindowsFixedSizeDialogHint)

        self.setWindowTitle(title)
        self.setLayout(qt.QGridLayout())

        # entry
        self.layout().addWidget(qt.QLabel("entry:", self), 0, 0, 1, 1)
        self._entryQLE = qt.QLineEdit(scan.entry if scan else "", self)
        self._entryQLE.setReadOnly(True)
        self.layout().addWidget(self._entryQLE, 0, 1, 1, 1)

        # file name
        self.layout().addWidget(qt.QLabel("file:", self), 1, 0, 1, 1)
        self._fileQLE = qt.QLineEdit(scan.master_file if scan else "", self)
        self._fileQLE.setReadOnly(True)
        self.layout().addWidget(self._fileQLE, 1, 1, 1, 1)

        # label message
        self._label = qt.QLabel(desc, self)
        self.layout().addWidget(self._label, 2, 0, 1, 2)

        # input QLineEdit
        self._input = qt.QLineEdit("", self)
        self.layout().addWidget(self._input, 3, 0, 1, 2)

        # cache combobox
        self._cacheAnswerCB = qt.QCheckBox("keep answer in cache", self)
        self._cacheAnswerCB.setToolTip(
            "Will keep in memory the answer for the"
            " 'current cycle'. A cycle starts when "
            "you press 'send all' or "
            "'send selected' and ends when the last"
            " scan as been converted. The cache is "
            "reset after each cycle"
        )
        font = self._cacheAnswerCB.font()
        font.setPixelSize(10)
        self._cacheAnswerCB.setFont(font)
        self.layout().addWidget(self._cacheAnswerCB, 4, 0, 1, 1)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 5, 0, 1, 1)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel
        self._buttons.setStandardButtons(types)

        self.layout().addWidget(self._buttons, 4, 0, 1, 2)

        # set up
        self._cacheAnswerCB.setChecked(cache_answer)

        # connect signal / slot
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.Cancel).clicked.connect(self.reject)

    def setLabelText(self, txt):
        self._label.setText(txt)

    def getText(self):
        return self._input.text()

    def setScan(self, entry, file_path):
        self._entryQLE.setText(entry)
        self._fileQLE.setText(file_path)

    def cache_answer(self):
        return self._cacheAnswerCB.isChecked()

    def setBlissScan(self, entry, file_path):
        self._fileQLE.setText(file_path)
        self._entryQLE.setText(entry)

    def clear(self):
        self.setWindowTitle("")
        self._label.setText("")
        self._input.setText("")


class NXTomomillInput:
    """
    callback provided to nxtomomill if an entry is missing.
    The goal is to ask the user the missing informations

    :param entry: name of the entry missing
    :param desc: description of the entry
    :return: user input or None
    """

    def __init__(self, parent=None, scan=None):
        self._dialog = InputDialogWithCache(parent=None, scan=scan)
        self._cache = {}
        """Cache to be used the user want to uase back answer for some question
        """

    def exec_(self, field, desc):
        self._dialog.clear()
        self._dialog.setWindowTitle(field)
        self._dialog.setLabelText(desc)

        if field in self._cache:
            return self._cache[field]
        else:
            if self._dialog.exec():
                answer = self._dialog.getText()
                if self._dialog.cache_answer():
                    self._cache[field] = answer
                return answer
            else:
                return None

    def setBlissScan(self, entry, file_path):
        self._dialog.setScan(entry=entry, file_path=file_path)

    __call__ = exec_


class OverwriteMessage(qt.QDialog):
    def __init__(self, parent, message=""):
        qt.QDialog.__init__(self, parent)
        self.setLayout(qt.QGridLayout())
        self._label = qt.QLabel(message, self)
        self.layout().addWidget(self._label, 0, 0, 1, 2)

        self._canOverwriteAllCB = qt.QCheckBox("overwrite all", self)
        self._canOverwriteAllCB.setToolTip(
            "Will keep in memory the right to overwrite nxtomomill output "
            "files for the 'current cycle'. A cycle starts when you press "
            "'send all' or 'send selected' and ends when the last scan as been"
            " converted. The cache is reset after each cycle"
        )
        font = self._canOverwriteAllCB.font()
        font.setPixelSize(10)
        self._canOverwriteAllCB.setFont(font)
        self.layout().addWidget(self._canOverwriteAllCB, 2, 0, 1, 1)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 3, 0, 1, 1)

        types = qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.No
        self._buttons = qt.QDialogButtonBox(self)
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons, 8, 0, 1, 1)

        # signal / slot connection
        self._buttons.button(qt.QDialogButtonBox.Ok).clicked.connect(self.accept)
        self._buttons.button(qt.QDialogButtonBox.No).clicked.connect(self.reject)

    def setText(self, msg):
        self._label.setText(msg)

    def canOverwriteAll(self):
        return self._canOverwriteAllCB.isChecked()

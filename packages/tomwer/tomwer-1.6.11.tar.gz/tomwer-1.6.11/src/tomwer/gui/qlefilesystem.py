"""contains QLFileSystem class. Specific implementation of the QLineEdit to select a file path."""

from __future__ import annotations


from silx.gui import qt


class QLFileSystem(qt.QLineEdit):
    """
    QLineEdit with a completer using a QDirModel
    """

    def __init__(self, text, parent, filters=None, **kwargs):
        super().__init__(parent=parent, **kwargs)
        self.completer = create_completer(filters=filters)
        self.setCompleter(self.completer)
        if text is not None:
            self.setText(text)


def create_completer(filters=None) -> qt.QCompleter:
    completer = qt.QCompleter()
    if qt.BINDING in ("PyQt5", "PySide2"):
        # note: should work with PyQt5 but we get some troubles with it on esrf deployment
        # see https://gitlab.esrf.fr/XRD/darfix/-/issues/174
        model = qt.QDirModel(completer)
    else:
        completer.setCompletionRole(qt.QFileSystemModel.FilePathRole)
        model = qt.QFileSystemModel(completer)
        model.setRootPath(qt.QDir.currentPath())
        model.setOption(qt.QFileSystemModel.DontWatchForChanges)
    if filters is not None:
        model.setFilter(filters)
    completer.setModel(model)

    return completer

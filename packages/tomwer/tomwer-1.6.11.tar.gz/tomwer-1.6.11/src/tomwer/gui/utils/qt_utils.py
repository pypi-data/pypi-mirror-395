from contextlib import contextmanager

from silx.gui import qt

if qt.BINDING == "PyQt5":
    from PyQt5.QtTest import QSignalSpy  # pylint: disable=E0401,E0611
elif qt.BINDING == "PySide6":
    from PySide6.QtTest import QSignalSpy  # pylint: disable=E0401,E0611
elif qt.BINDING == "PyQt6":
    from PyQt6.QtTest import QSignalSpy  # pylint: disable=E0401,E0611
else:
    QSignalSpy = None


@contextmanager
def block_signals(*objs):
    """Context manager blocking signals of QObjects.

    It restores previous state when leaving.

    :param qt.QObject objs: QObjects for which to block signals
    """
    blocked = [(obj, obj.blockSignals(True)) for obj in objs]
    try:
        yield
    finally:
        for obj, previous in blocked:
            obj.blockSignals(previous)

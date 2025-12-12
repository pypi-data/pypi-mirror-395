from __future__ import annotations

from silx.gui import qt
from contextlib import contextmanager


@contextmanager
def qitem_model_resetter(model: qt.QAbstractItemModel):
    """Context manager for resetting a QAbstractItemModel.

    Make sure `beginResetModel()` is emit at the beginning and endResetModel() at the end.
    """
    model.beginResetModel()
    try:
        yield
    finally:
        model.endResetModel()

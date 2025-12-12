# coding: utf-8

from __future__ import annotations

import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.saaxis.params import SAAxisParams

logger = logging.getLogger(__name__)


class QSAAxisParams(SAAxisParams, qt.QObject):
    sigChanged = qt.Signal()
    """Signal emitted when at least one element of the dictionary change"""

    sigAxisUrlChanged = qt.Signal()
    """Signal emitted when the axis url change"""

    def __init__(self):
        qt.QObject.__init__(self)
        SAAxisParams.__init__(self)

    def changed(self):
        self.sigChanged.emit()

    def axis_urls_changed(self):
        self.sigAxisUrlChanged.emit()

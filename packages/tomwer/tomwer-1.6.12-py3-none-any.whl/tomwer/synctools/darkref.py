# coding: utf-8
from __future__ import annotations


import logging

from silx.gui import qt

from tomwer.core.process.reconstruction.darkref import params as dkrf

logger = logging.getLogger(__name__)


class QDKRFRP(dkrf.DKRFRP, qt.QObject):
    sigChanged = qt.Signal()
    """Signal emitted when at least one element of the dictionary change"""

    def __init__(self):
        qt.QObject.__init__(self)
        dkrf.DKRFRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()

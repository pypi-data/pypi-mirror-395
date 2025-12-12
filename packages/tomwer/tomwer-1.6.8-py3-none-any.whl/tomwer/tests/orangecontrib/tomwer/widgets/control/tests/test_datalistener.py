# coding: utf-8
from __future__ import annotations


import gc

import pickle

from silx.gui import qt

from tomwer.tests.conftest import qtapp  # noqa F401
from orangecontrib.tomwer.widgets.deprecated.DataListenerOW import DataListenerOW
from orangecanvas.scheme.readwrite import literal_dumps


def test_DataListenerOW(
    qtapp,  # noqa F811
):

    widget = DataListenerOW(host_discovery=False)

    pickle.dumps(widget.get_configuration())
    literal_dumps(widget.get_configuration())

    widget.setAttribute(qt.Qt.WA_DeleteOnClose)
    widget.close()

    gc.collect()

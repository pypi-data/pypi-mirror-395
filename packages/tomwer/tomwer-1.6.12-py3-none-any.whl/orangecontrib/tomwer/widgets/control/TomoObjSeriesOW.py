# coding: utf-8
from __future__ import annotations

import logging

from orangewidget import gui
from orangewidget.widget import Input, Output, OWBaseWidget
from tomoscan.series import Series

import tomwer.core.process.control.tomoobjseries
from tomwer.core.tomwer_object import TomwerObject
from tomwer.gui.control.series.seriescreator import SeriesWidgetDialog

logger = logging.getLogger(__name__)


class TomoObjSeriesOW(OWBaseWidget, openclass=True):
    name = "series of objects"
    id = "orange.widgets.tomwer.tomoobjseriesow"
    description = "Allow user define a series of object that will be defined as a Series (grouped together and can be used within a purpose like stitching)"
    icon = "icons/tomoobjseries.svg"
    priority = 55
    keywords = ["tomography", "selection", "tomwer", "series", "group"]

    ewokstaskclass = tomwer.core.process.control.tomoobjseries._TomoobjseriesPlaceHolder

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        tomo_obj = Input(name="tomo obj", type=TomwerObject, multiple=True)

    class Outputs:
        series = Output(name="series", type=Series)

    def __init__(self, parent=None):
        """ """
        super().__init__(parent)
        layout = gui.vBox(self.mainArea, self.name).layout()

        self._widget = SeriesWidgetDialog(self)
        layout.addWidget(self._widget)

        # connect signal / slot
        self._widget.sigSeriesSelected.connect(self._send_series)

    @Inputs.tomo_obj
    def addTomoObj(self, tomo_obj, *args, **kwargs):
        if tomo_obj is not None:
            self._widget.add(tomo_obj)

    def _send_series(self, series: Series):
        if not isinstance(series, Series):
            raise TypeError(
                f"series is expected to be an instance of {Series}. Not {type(series)}"
            )
        self.Outputs.series.send(series)

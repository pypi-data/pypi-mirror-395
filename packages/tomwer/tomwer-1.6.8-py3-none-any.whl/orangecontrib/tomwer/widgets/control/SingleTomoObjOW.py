# coding: utf-8
from __future__ import annotations

import logging

import tomoscan.esrf.scan.utils
from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Input, Output, OWBaseWidget

import tomwer.core.process.control.singletomoobj
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.volumefactory import VolumeFactory
from tomwer.gui.control.singletomoobj import SingleTomoObj

_logger = logging.getLogger(__name__)


class SingleTomoObjOW(OWBaseWidget, openclass=True):
    name = "single tomo obj"
    id = "orange.widgets.tomwer.control.SingleScanOW.SingleScanOW"
    description = "Definition of a single dataset"
    icon = "icons/single_tomo_obj.svg"
    priority = 51
    keywords = ["tomography", "NXtomo", "tomwer", "folder", "scan"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    ewokstaskclass = tomwer.core.process.control.singletomoobj.SingleTomoObjProcess

    _tomo_obj_setting = Setting(str())

    class Inputs:
        tomo_obj = Input(name="tomo_obj", type=TomwerObject)

    class Outputs:
        tomo_obj = Output(
            name="tomo_obj", type=TomwerObject, doc="one object to be process"
        )
        reduced_darks = Output(
            name="reduced dark(s)",
            type=dict,
            doc="Reduced darks as a dict",
        )
        reduced_flats = Output(
            name="reduced flat(s)",
            type=dict,
            doc="Reduced flats as a dict",
        )
        relative_reduced_darks = Output(
            name="relative reduced dark(s)",
            type=dict,
            doc="Reduced darks as a dict. Indexes are provided as relative so in [0.0, 1.0[",
        )
        relative_reduced_flats = Output(
            name="relative reduced flat(s)",
            type=dict,
            doc="Reduced flats as a dict. Indexes are provided as relative so in [0.0, 1.0[",
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        self._latest_received_scan = None
        # small work around to keep in scan processing cache and avoid recomputing it if not necessary
        self.widget = SingleTomoObj(parent=self)
        self.widget.sigTomoObjChanged.connect(self._updateSettings)
        self.widget.sigTomoObjChanged.connect(self._triggerObjDownstream)

        self._loadSettings()
        layout = gui.vBox(self.mainArea, self.name).layout()
        layout.addWidget(self.widget)

    @Inputs.tomo_obj
    def add(self, tomo_obj):
        if tomo_obj is None:
            return
        self.widget.setTomoObject(tomo_obj)

    def _loadSettings(self):
        if self._tomo_obj_setting != str():
            self.widget.setTomoObject(self._tomo_obj_setting)

    def _updateSettings(self):
        self._tomo_obj_setting = self.widget.getTomoObjIdentifier()

    def _triggerObjDownstream(self):
        obj_identifier = self.widget.getTomoObjIdentifier()
        if (
            self._latest_received_scan is not None
            and self._latest_received_scan.get_identifier() == obj_identifier
        ):
            data = self._latest_received_scan
        else:
            try:
                data = VolumeFactory.create_tomo_object_from_identifier(obj_identifier)
            except:  # noqa E722
                try:
                    data = ScanFactory.create_tomo_object_from_identifier(
                        obj_identifier
                    )
                except:  # noqa E722
                    _logger.warning(
                        f"Unable to find an obj with {obj_identifier} as identifier"
                    )
                    return

        self.Outputs.tomo_obj.send(data)
        # if the data is a scan then provide also access to the reduced frames. Can be convenient
        if isinstance(data, TomwerScanBase):
            if data.reduced_darks not in (None, {}):
                reduced_darks = data.reduced_darks
                self.Outputs.reduced_darks.send(reduced_darks)

                # we want to send those in relative position to have something generic. This is a convention for now
                reduced_darks = (
                    tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                        reduced_frames=data.reduced_darks, scan=data
                    )
                )
                reduced_darks["reduce_frames_name"] = (
                    f"darks from {data.get_identifier().short_description()}"
                )
                self.Outputs.relative_reduced_darks.send(reduced_darks)

            if data.reduced_flats not in (None, {}):
                reduced_flats = data.reduced_flats
                self.Outputs.reduced_flats.send(reduced_flats)

                # we want to send those in relative position to have something generic. This is a convention for now
                reduced_flats = (
                    tomoscan.esrf.scan.utils.from_absolute_reduced_frames_to_relative(
                        reduced_frames=data.reduced_flats, scan=data
                    )
                )
                reduced_flats["reduce_frames_name"] = (
                    f"flats from {data.get_identifier().short_description()}"
                )
                self.Outputs.relative_reduced_flats.send(reduced_flats)

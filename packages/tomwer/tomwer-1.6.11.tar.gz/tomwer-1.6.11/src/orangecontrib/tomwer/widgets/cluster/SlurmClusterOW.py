from __future__ import annotations

import logging

from silx.gui import qt

from orangewidget import gui
from orangewidget.settings import Setting
from orangewidget.widget import Output, OWBaseWidget

from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.gui.cluster.slurm import SlurmSettingsWindow
from tomwer.core.settings import SlurmSettingsMode

_logger = logging.getLogger(__name__)


class SlurmClusterOW(OWBaseWidget, openclass=True):
    """
    Orange widget to define a slurm cluster as input of other
    widgets (based on nabu for now)
    """

    name = "slurm cluster"
    id = "orange.widgets.tomwer.cluster.SlurmClusterOW.SlurmClusterOW"
    description = "Let the user configure the cluster to be used."
    icon = "icons/slurm.svg"
    priority = 20
    keywords = ["tomography", "tomwer", "slurm", "cluster", "configuration"]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    _ewoks_default_inputs = Setting(dict())
    slurm_mode_name = Setting(SlurmSettingsMode.GENERIC.name)

    class Outputs:
        config_out = Output(name="cluster_config", type=SlurmClusterConfiguration)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._widget = SlurmSettingsWindow(parent=self)
        self._widget.setWindowFlags(qt.Qt.Widget)
        layout.addWidget(self._widget)

        if self._ewoks_default_inputs != {}:
            self._widget.setConfiguration(self._ewoks_default_inputs)

        try:
            mode = SlurmSettingsMode[self.slurm_mode_name]
            self._widget.setMode(mode)
        except Exception:
            _logger.exception(
                f"Could not restore saved SlurmSettingsMode {self.slurm_mode_name!r}"
            )

        # trigger the signal to avoid any user request
        self.Outputs.config_out.send(self.getConfiguration())

        # connect signal / slot
        self._widget.sigConfigChanged.connect(self._configurationChanged)

    def __new__(cls, *args, **kwargs):
        # ensure backward compatibility with 'static_input'
        static_input = kwargs.get("stored_settings", {}).get("_static_input", None)
        if static_input not in (None, {}):
            _logger.warning(
                "static_input has been deprecated. Will be replaced by _ewoks_default_inputs in the workflow file. Please save the workflow to apply modifications"
            )
            kwargs["stored_settings"]["_ewoks_default_inputs"] = static_input
        return super().__new__(cls, *args, **kwargs)

    def _configurationChanged(self):
        slurmClusterconfiguration = self.getConfiguration()
        self.Outputs.config_out.send(slurmClusterconfiguration)
        self._ewoks_default_inputs = slurmClusterconfiguration.to_dict()
        self.slurm_mode_name = self._widget.mode().name

    def getConfiguration(self):
        return self._widget.getSlurmClusterConfiguration()

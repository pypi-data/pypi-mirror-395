import logging

from orangewidget.settings import Setting
from orangewidget.widget import Input, Output

from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack

from tomwer.core.process.stitching.nabustitcher import StitcherTask
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject

_logger = logging.getLogger(__name__)


class StitcherOW(
    TomwerWithStackStack,
    ewokstaskclass=StitcherTask,
):
    """
    Widget to apply stitching
    """

    name = "stitcher"
    id = "orange.widgets.tomwer.stitching.StitcherOW.StitcherOW"
    description = "Interface to trigger stitching"
    icon = "icons/stitcher_icon.svg"
    priority = 52
    keywords = [
        "hdf5",
        "tomwer",
        "NXTomo",
        "stitcher",
        "stitching",
        "z-stitching",
        "z-serie",
        "zserie",
    ]

    want_main_area = True
    resizing_enabled = True
    want_control_area = False

    _ewoks_default_inputs = Setting(
        {"stitching_config": dict(), "cluster_config": dict()}
    )

    class Inputs:
        stitching_config = Input(
            name="stitching configuration",
            type=dict,
            doc="configuration to stitch together tomo object as a dictionary",
            default=True,
            multiple=False,
        )

        cluster_config = Input(
            name="cluster_config",
            type=SlurmClusterConfiguration,
            doc="slurm cluster to be used",
            multiple=False,
        )

    class Outputs:
        data = Output(name="data", type=TomwerScanBase, doc="one scan to be process")
        volume = Output(name="volume", type=TomwerVolumeBase, doc="raw volume")
        future_tomo_obj = Output(
            name="future_tomo_obj",
            type=FutureTomwerObject,
            doc="future object (process remotely)",
        )

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

    def _get_task_arguments(self):
        adict = super()._get_task_arguments()
        # pop progress as does not fully exists on the orange-widget-base
        adict.pop("progress", None)
        return adict

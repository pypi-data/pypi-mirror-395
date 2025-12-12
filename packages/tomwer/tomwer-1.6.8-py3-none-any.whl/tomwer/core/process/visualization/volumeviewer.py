# coding: utf-8
from ewokscore.task import Task as EwoksTask


class _VolumeViewerPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to plot a (reconstructed) volume
    """

    def run(self):
        pass

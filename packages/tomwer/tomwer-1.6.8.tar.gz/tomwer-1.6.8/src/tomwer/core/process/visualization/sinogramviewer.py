# coding: utf-8

from ewokscore.task import Task as EwoksTask


class _SinogramViewerPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to display a sinogram
    """

    def run(self):
        pass

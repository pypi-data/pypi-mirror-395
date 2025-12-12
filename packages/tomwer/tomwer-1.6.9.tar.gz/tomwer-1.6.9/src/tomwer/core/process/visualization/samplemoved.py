# coding: utf-8

from ewokscore.task import Task as EwoksTask


class _SampleMovedPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to check if a sample has moved along time / projections
    """

    def run(self):
        pass

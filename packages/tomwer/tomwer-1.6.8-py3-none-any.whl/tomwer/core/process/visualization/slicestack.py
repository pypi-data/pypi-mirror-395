# coding: utf-8

from ewokscore.task import Task as EwoksTask


class _SliceStackPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to aggregate reconstructed slices of several scans and allow users to along them
    """

    def run(self):
        pass

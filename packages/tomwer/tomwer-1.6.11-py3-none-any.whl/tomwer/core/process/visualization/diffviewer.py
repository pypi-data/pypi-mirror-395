# coding: utf-8
from __future__ import annotations


from ewokscore.task import Task as EwoksTask


class _DiffViewerPlaceHolder(EwoksTask, input_names=("data",)):
    """
    task to compare frames (between one or several dataset)
    """

    def run(self):
        pass

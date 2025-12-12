# coding: utf-8
from __future__ import annotations


from ewokscore.task import Task as EwoksTask


class _DataViewerPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to browse a scan and associated processing (display raw frames, normalized projections, recosntructed slices...)
    """

    def run(self):
        pass

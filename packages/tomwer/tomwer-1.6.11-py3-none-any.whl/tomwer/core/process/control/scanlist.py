# coding: utf-8

"""
This module is used to define a set of folders to be emitted to the next box.
"""

import logging

from tomwer.core.process.task import Task
from tomwer.core.utils.scanutils import data_identifier_to_scan

logger = logging.getLogger(__name__)


class _ScanListPlaceHolder(
    Task, optional_input_names=("data",), output_names=("data",)
):
    """For now data can only be a single element and not a list.
    This must be looked at.
    Also when part of an ewoks graph 'data' is mandatory which is not the class
    when part of a orange workflow. Those can be added interactively"""

    def run(self):
        self.outputs.data = data_identifier_to_scan(self.inputs.data)

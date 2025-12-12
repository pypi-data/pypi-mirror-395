"""
Define the tomwer Task class.
Insure connection with ewoks.
All instances of tomwer Tasks should avoid gui import (as qt).
"""

from __future__ import annotations

import logging
from collections import namedtuple

from ewokscore.task import Task as _EwoksTask
from ewokscore.taskwithprogress import TaskWithProgress as _EwoksTaskWithProgress


_logger = logging.getLogger(__name__)

_process_desc = namedtuple(
    "_process_desc", ["process_order", "configuration", "results"]
)


class BaseProcessInfo:
    """Tomwer base process class"""

    def __init__(self, inputs=None):
        """
        :param return_dict: if True serialize (to_dict / from_dict functions) between each task
        """

        self._scheme_title = (
            "scheme_title"  # TODO: have a look, this must be get somewhere and reused ?
        )

        """should the return type of the handler should be TomoBase instance
        objects or dict"""
        self._settings = {}
        self._cancelled = False
        # a useful variable that can be set to True if the task has been cancelled

    @staticmethod
    def properties_help():
        """

        :return: display the list of all managed keys and possible values
        """
        # TODO: use argsparse instead of this dict ?
        raise NotImplementedError("BaseProcess is an abstract class")

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        raise NotImplementedError("Base class")

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        raise NotImplementedError("Base class")

    @staticmethod
    def definition():
        """definition of the process"""
        raise NotImplementedError("Base class")

    def get_configuration(self) -> dict | None:
        """

        :return: configuration of the process
        """
        if self._settings is None:
            return None
        if len(self._settings) > 0:
            return self._settings
        else:
            return None

    def set_configuration(self, configuration: dict) -> None:
        self._settings = configuration


class TaskWithProgress(_EwoksTaskWithProgress, BaseProcessInfo):
    """Class from which all tomwer process should inherit

    :param logger: the logger used by the class
    """

    def __init__(
        self,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
        progress=None,
    ):
        BaseProcessInfo.__init__(self, inputs=inputs)
        _EwoksTaskWithProgress.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
            progress=progress,
        )


class Task(_EwoksTask, BaseProcessInfo):
    """Class from which all tomwer process should inherit

    :param logger: the logger used by the class
    """

    def __init__(
        self,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        BaseProcessInfo.__init__(self, inputs=inputs)
        _EwoksTask.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )

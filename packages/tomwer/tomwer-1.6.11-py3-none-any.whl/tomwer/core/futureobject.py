"""contains 'FutureTomwerObject'. Class used when computation is done asynchronously (when submitted to slurm for example)"""

from __future__ import annotations

import datetime
import logging
from typing import Iterable

from sluurp.job import get_job_status, cancel_slurm_job

from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.tomwer_object import TomwerObject

_logger = logging.getLogger(__name__)


class FutureTomwerObject:
    """Container for an existing TomwerScanBase with some future object
    (like slice reconstruction on slurm...)

    :param scan: scan at the origin of the FutureTomwerScan
    :param futures: tuple of Future
    :param start_time: start_time of the FutureTomwerScan. If not provided
                       this will be set to the date of creation of the object.
    :param process_requester_id: process of the id requesting future
                                     processing. This is useful to keep a trace on
                                     the source of the computation. To display
                                     supervisor 'request' for example.
    """

    def __init__(
        self,
        tomo_obj: TomwerObject,
        futures: tuple | list | None,
        start_time: datetime.time | None = None,
        process_requester_id: int | None = None,
    ):
        if not isinstance(tomo_obj, TomwerObject):
            raise TypeError(
                f"tomo_obj is expected to be an instance of {TomwerObject} not {type(tomo_obj)}"
            )
        self._job_id = None
        self._tomo_obj = tomo_obj
        self._start_time = (
            start_time if start_time is not None else datetime.datetime.now()
        )
        self._process_requester_id = process_requester_id
        # handle futures
        if futures is None:
            self._futures = None
        elif not isinstance(futures, (tuple, list)):
            raise TypeError(
                f"futures is expected to be a tuple or a list not {type(futures)}"
            )
        else:
            self._futures = list(futures)

    @property
    def job_id(self) -> int | None:
        return self._job_id

    @property
    def status(self) -> str | None:
        all_status = [
            get_job_status(fut.job_id) if hasattr(fut, "job_id") else "unknown"
            for fut in self._futures
        ]
        # small hack to get a common status for a list of future.
        # if at least one running we can wait for all to be processed
        # Then after this condition it means all jobs are finished
        # and we can check if there is an error
        # otherwise everything is "green"
        for status in (
            "pending",
            "running",
            "error",
            "cancelled",
            "finished",
            "completed",
        ):
            if status in all_status:
                return status
        return "finished"

    @property
    def logs(self) -> str:
        new_line = "\n"
        return "\n".join(
            [
                f"~~~~~~ job id = {fut.job_id} ~~~~~{new_line}{f'{new_line}'.join(fut.collect_logs() or ['',])}"
                for fut in self._futures
            ]
        )

    @property
    def start_time(self) -> datetime.time | None:
        return self._start_time

    @property
    def tomo_obj(self) -> TomwerScanBase:
        # TODO: replace the scan by the DatasetIdentifier
        return self._tomo_obj

    @property
    def futures(self) -> tuple | None:
        if self._futures is None:
            return None
        else:
            return tuple(self._futures)

    def extend_futures(self, futures: Iterable) -> None:
        if not isinstance(futures, Iterable):
            raise TypeError(f"futures should be an Iterable not {type(futures)}")
        if self._futures is None:
            self._futures = []
        self._futures.extend(futures)

    @property
    def process_requester_id(self) -> int | None:
        return self._process_requester_id

    def results(self) -> TomwerScanBase:
        """Force future and callback synchronization"""
        results = []
        [results.append(fut.result()) for fut in self._futures]
        return results

    def cancelled(self):
        cancelled = False
        for future in self.futures:
            cancelled = cancelled and future.cancelled()
        return cancelled

    def done(self):
        done = True
        for future in self.futures:
            done = done and future.done()
        return done

    def exceptions(self) -> dict | None:
        """
        Return exception with future as key and exception as value
        """
        exceptions = {}
        for future in self.futures:
            if future.exception():
                exceptions[future] = future.exception()

        if len(exceptions) == 0:
            return None
        else:
            return exceptions

    def cancel(self):
        for future in self.futures:
            if hasattr(future, "job_id"):
                print("cancel ", future.job_id)
                cancel_slurm_job(future.job_id)

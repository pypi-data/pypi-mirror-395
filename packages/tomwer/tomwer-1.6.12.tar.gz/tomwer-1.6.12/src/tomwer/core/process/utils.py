# coding: utf-8
from __future__ import annotations

import datetime
import logging
from collections import OrderedDict

import h5py
from silx.io.url import DataUrl
from silx.io.utils import h5py_read_dataset

from tomwer.core.process.reconstruction.scores import ComputedScore
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanbase import TomwerScanBase

_logger = logging.getLogger(__name__)


class LastReceivedScansDict(OrderedDict):
    """List the received scan from the first received to the last received"""

    def __init__(self, limit=None):
        """Simple structure in order to store the received last elements and
        the time of acquisition
        """
        assert limit is None or (type(limit) is int and limit > 0)
        OrderedDict.__init__(self)
        self.limit = limit

    def add(self, scan):
        assert isinstance(scan, (TomwerScanBase, BlissScan))
        self[str(scan)] = datetime.datetime.now()
        if self.limit is not None and len(self) > self.limit:
            self.pop(list(self.keys())[0])


class IgnoreProcess:
    """Simple util class to ignore a processing when using ewoks"""

    def process(self, scan):
        return scan

    __call__ = process


def get_scores(node: h5py.Group) -> dict | None:
    """read all the score from the 'results' sub group. Read the url
    and computed scores

    :return: a dictionary with (url, ComputedScore) for each node
    """
    if "results" not in node:
        _logger.warning(f"no results found in {node}")
        return None
    else:
        res_node = node["results"]
        scores = {}
        for res_item in res_node:
            score_node = res_node[res_item]
            try:
                float(res_item)
            except Exception:
                is_a_score = False
            else:
                is_a_score = True

            if not is_a_score:
                continue

            try:
                url = DataUrl(
                    file_path=node.file.filename,
                    data_path="/".join((score_node.name, "reconstructed_slice")),
                    scheme="silx",
                )
                score = ComputedScore(
                    tv=h5py_read_dataset(score_node["total variation"]),
                    std=h5py_read_dataset(score_node["standard deviation"]),
                )
                scores[float(res_item)] = (url, score)
            except Exception as e:
                _logger.warning(f"Unable to load {score_node.name}. Reason is {e}")
        scores = dict(sorted(scores.items(), key=lambda item: item[0]))

        return scores

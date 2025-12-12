from __future__ import annotations

from tomwer.core.scan.scanbase import TomwerScanBase
from collections import OrderedDict

_CACHE: {str, tuple[float | None, dict | None]} = OrderedDict()
"""
In the case we want to reprocess a scan we (might) need to know the cor and the nabu reconstruction parameters (for nabu slice and volume reconstructions)
But we are not keeping all those object during the full 'orange canvas' lifecycle, it would be too heavy.
As a consequence we cache those (small) values (and only those) of the last n scans (n==30) in case users want to reprocess some of those.
n value is an arbitrary value.
"""
_CACHE_SIZE = 30


def save_reconstruction_parameters_to_cache(scan: TomwerScanBase):
    # pop if exists. Will move this item as 'last-in'
    _CACHE.pop(scan.get_identifier().to_str(), None)
    _CACHE[scan.get_identifier().to_str()] = (
        None if scan.axis_params is None else scan.axis_params.relative_cor_value,
        None if scan.nabu_recons_params is None else scan.nabu_recons_params,
    )
    if len(_CACHE) > _CACHE_SIZE:
        _CACHE.popitem(last=False)


def load_reconstruction_parameters_from_cache(scan: TomwerScanBase):
    cor, nabu_recons_params = _CACHE.get(scan.get_identifier().to_str(), (None, None))
    if cor is not None and scan.axis_params is not None:
        scan.axis_params.set_relative_value(cor)
    if nabu_recons_params is not None:
        scan.nabu_recons_params = nabu_recons_params


def clear_reconstruction_parameters_cache():
    _CACHE.clear()

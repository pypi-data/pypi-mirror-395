# coding: utf-8
from __future__ import annotations

import pathlib
from datetime import datetime
from urllib.parse import urlparse

from processview.core.dataset import Dataset, DatasetIdentifier
from tomoscan.esrf.identifier.rawidentifier import (
    RawVolumeIdentifier as _RawVolumeIdentifier,
)
from tomoscan.esrf.identifier.url_utils import split_path
from tomoscan.esrf.volume.rawvolume import RawVolume as _RawVolume

from tomwer.core.volume.volumebase import TomwerVolumeBase


class RawVolumeIdentifier(_RawVolumeIdentifier, DatasetIdentifier):
    """Identifier specific to .vol volume"""

    def __init__(self, object, file_path, metadata=None):
        super().__init__(object, file_path)
        DatasetIdentifier.__init__(self, RawVolume.from_identifier, metadata=metadata)

    @staticmethod
    def from_str(identifier):
        info = urlparse(identifier)
        paths = split_path(info.path)
        if len(paths) == 1:
            vol_file = paths[0]
            tomo_type = None
        elif len(paths) == 2:
            tomo_type, vol_file = paths
        else:
            raise ValueError("Failed to parse path string:", info.path)
        if tomo_type is not None and tomo_type != RawVolumeIdentifier.TOMO_TYPE:
            raise TypeError(
                f"provided identifier fits {tomo_type} and not {RawVolumeIdentifier.TOMO_TYPE}"
            )
        return RawVolumeIdentifier(object=RawVolume, file_path=vol_file)

    def long_description(self) -> str:
        """used for processview header tooltip for now"""
        return self.to_str()


class RawVolume(_RawVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, RawVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {RawVolumeIdentifier}"
            )
        return RawVolume(
            file_path=identifier.file_path,
        )

    def get_identifier(self) -> RawVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")

        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return RawVolumeIdentifier(
            object=self,
            file_path=self.url.file_path(),
            metadata={
                "name": self.url.file_path(),
                "creation_time": (
                    datetime.fromtimestamp(stat.st_ctime) if stat else None
                ),
                "modification_time": (
                    datetime.fromtimestamp(stat.st_ctime) if stat else None
                ),
            },
        )

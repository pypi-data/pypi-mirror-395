# coding: utf-8
from __future__ import annotations


import pathlib
from datetime import datetime
from processview.core.dataset import Dataset, DatasetIdentifier
from tomoscan.esrf.identifier.jp2kidentifier import (
    JP2KVolumeIdentifier as _JP2KVolumeIdentifier,
)
from tomoscan.esrf.volume.jp2kvolume import JP2KVolume as _JP2KVolume

from tomwer.core.volume.volumebase import TomwerVolumeBase


class JP2KVolumeIdentifier(_JP2KVolumeIdentifier, DatasetIdentifier):
    """Identifier specific to JP2K volume"""

    def __init__(self, object, folder, file_prefix, metadata=None):
        super().__init__(object, folder, file_prefix)
        DatasetIdentifier.__init__(self, JP2KVolume.from_identifier, metadata=metadata)

    @staticmethod
    def from_str(identifier):
        return _JP2KVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=JP2KVolumeIdentifier,
            ObjClass=JP2KVolume,
        )

    def long_description(self) -> str:
        """used for processview header tooltip for now"""
        return self.to_str()


class JP2KVolume(_JP2KVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, JP2KVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {JP2KVolumeIdentifier}"
            )
        return JP2KVolume(
            folder=identifier.folder,
            volume_basename=identifier.file_prefix,
        )

    def get_identifier(self) -> JP2KVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")

        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return JP2KVolumeIdentifier(
            object=self,
            folder=self.url.file_path(),
            file_prefix=self._volume_basename,
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

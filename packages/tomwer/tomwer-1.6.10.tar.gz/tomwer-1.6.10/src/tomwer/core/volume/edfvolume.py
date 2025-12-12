# coding: utf-8
from __future__ import annotations

import pathlib
from datetime import datetime
from processview.core.dataset import Dataset, DatasetIdentifier
from tomoscan.esrf.identifier.edfidentifier import (
    EDFVolumeIdentifier as _EDFVolumeIdentifier,
)
from tomoscan.esrf.volume.edfvolume import EDFVolume as _EDFVolume

from tomwer.core.volume.volumebase import TomwerVolumeBase


class EDFVolumeIdentifier(_EDFVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, folder, file_prefix, metadata=None):
        super().__init__(object, folder, file_prefix)
        DatasetIdentifier.__init__(
            self, data_builder=EDFVolume.from_identifier, metadata=metadata
        )

    @staticmethod
    def from_str(identifier):
        return _EDFVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=EDFVolumeIdentifier,
            ObjClass=EDFVolume,
        )

    def long_description(self) -> str:
        """used for processview header tooltip for now"""
        return self.to_str()


class EDFVolume(_EDFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, EDFVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {EDFVolumeIdentifier} and not {type(identifier)}"
            )
        return EDFVolume(
            folder=identifier.folder,
            volume_basename=identifier.file_prefix,
        )

    def get_identifier(self) -> EDFVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return EDFVolumeIdentifier(
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

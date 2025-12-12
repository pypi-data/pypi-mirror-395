# coding: utf-8
from __future__ import annotations

import os
import pathlib
from datetime import datetime

from processview.core.dataset import Dataset, DatasetIdentifier
from tomoscan.esrf.identifier.tiffidentifier import (
    MultiTiffVolumeIdentifier as _MultiTiffVolumeIdentifier,
)
from tomoscan.esrf.identifier.tiffidentifier import (
    TIFFVolumeIdentifier as _TIFFVolumeIdentifier,
)
from tomoscan.esrf.volume.tiffvolume import MultiTIFFVolume as _MultiTIFFVolume
from tomoscan.esrf.volume.tiffvolume import TIFFVolume as _TIFFVolume

from tomwer.core.volume.volumebase import TomwerVolumeBase


class TIFFVolumeIdentifier(_TIFFVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, folder, file_prefix, metadata=None):
        super().__init__(object, folder, file_prefix)
        DatasetIdentifier.__init__(self, TIFFVolume.from_identifier, metadata=metadata)

    @staticmethod
    def from_str(identifier):
        return _TIFFVolumeIdentifier._from_str_to_single_frame_identifier(
            identifier=identifier,
            SingleFrameIdentifierClass=TIFFVolumeIdentifier,
            ObjClass=TIFFVolume,
        )

    def long_description(self) -> str:
        """used for processview header tooltip for now"""
        return self.to_str()


class MultiTiffVolumeIdentifier(_MultiTiffVolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, tiff_file, metadata=None):
        super().__init__(object, tiff_file)
        DatasetIdentifier.__init__(self, TIFFVolume.from_identifier, metadata=metadata)

    @staticmethod
    def from_str(identifier):
        identifier_no_scheme = identifier.split(":")[-1]
        tiff_file = identifier_no_scheme
        return MultiTiffVolumeIdentifier(object=TIFFVolume, tiff_file=tiff_file)


class TIFFVolume(_TIFFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, TIFFVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {TIFFVolumeIdentifier} not {type(identifier)}"
            )
        return TIFFVolume(
            folder=identifier.folder,
            volume_basename=identifier.file_prefix,
        )

    def get_identifier(self) -> TIFFVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")

        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return TIFFVolumeIdentifier(
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

    def volume_data_parent_folder(self):
        if self.data_url is None:
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())


class MultiTIFFVolume(_MultiTIFFVolume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, MultiTiffVolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {MultiTiffVolumeIdentifier}"
            )
        return MultiTIFFVolume(
            file_path=identifier.file_path,
        )

    def get_identifier(self) -> MultiTiffVolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")

        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return MultiTiffVolumeIdentifier(
            object=self,
            tiff_file=self.url.file_path(),
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

    def volume_data_parent_folder(self):
        if self.data_url is None:
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())

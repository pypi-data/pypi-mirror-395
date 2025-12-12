# coding: utf-8
from __future__ import annotations

import pathlib
import logging
from datetime import datetime
from urllib.parse import urlparse

from processview.core.dataset import Dataset, DatasetIdentifier
from tomoscan.esrf.identifier.hdf5Identifier import (
    HDF5VolumeIdentifier as _HDF5VolumeIdentifier,
)
from tomoscan.esrf.identifier.url_utils import UrlSettings, split_path, split_query
from tomoscan.esrf.volume.hdf5volume import HDF5Volume as _HDF5Volume
from tomoscan.esrf.scan.utils import get_data

from tomwer.core.volume.volumebase import TomwerVolumeBase
from silx.io.url import DataUrl

_logger = logging.getLogger(__name__)


class HDF5VolumeIdentifier(_HDF5VolumeIdentifier, DatasetIdentifier):
    def __init__(self, object, hdf5_file, entry, **args):
        super().__init__(object, hdf5_file, entry)
        DatasetIdentifier.__init__(
            self, data_builder=HDF5Volume.from_identifier, **args
        )

    @staticmethod
    def from_str(identifier):
        info = urlparse(identifier)
        paths = split_path(info.path)
        if len(paths) == 1:
            hdf5_file = paths[0]
            tomo_type = None
        elif len(paths) == 2:
            tomo_type, hdf5_file = paths
        else:
            raise ValueError("Failed to parse path string:", info.path)
        if tomo_type is not None and tomo_type != HDF5VolumeIdentifier.TOMO_TYPE:
            raise TypeError(
                f"provided identifier fits {tomo_type} and not {HDF5VolumeIdentifier.TOMO_TYPE}"
            )

        queries = split_query(info.query)
        entry = queries.get(UrlSettings.DATA_PATH_KEY, None)
        if entry is None:
            raise ValueError("expects to get a data_path")
        return HDF5VolumeIdentifier(object=HDF5Volume, hdf5_file=hdf5_file, entry=entry)

    def long_description(self) -> str:
        """used for processview header tooltip for now"""
        return self.to_str()


class HDF5Volume(_HDF5Volume, TomwerVolumeBase, Dataset):
    @staticmethod
    def from_identifier(identifier):
        """Return the Dataset from a identifier"""
        if not isinstance(identifier, HDF5VolumeIdentifier):
            raise TypeError(
                f"identifier should be an instance of {HDF5VolumeIdentifier}"
            )
        return HDF5Volume(
            file_path=identifier.file_path,
            data_path=identifier.data_path,
        )

    def get_identifier(self) -> HDF5VolumeIdentifier:
        if self.url is None:
            raise ValueError("no file_path provided. Cannot provide an identifier")
        try:
            stat = pathlib.Path(self.url.file_path()).stat()
        except Exception:
            stat = None

        return HDF5VolumeIdentifier(
            object=self,
            hdf5_file=self.url.file_path(),
            entry=self.url.data_path(),
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

    def load_metadata(self, url: DataUrl | None = None, store: bool = True) -> dict:
        # nabu stores software version outside the expected metadata dict (depends on the version).
        # But we need those as part of the metadata to notify the user. So this section will try to read it when outside the
        # expected metadata dict.
        metadata = super().load_metadata(url=url, store=store)
        # software version
        url = url or self.metadata_url
        if url.scheme() != "silx":
            return metadata

        data_path = url.data_path()
        if data_path is None or len(data_path.split("/")) == 1:
            return metadata

        version_data_path = "/".join(
            list(data_path.split("/")[:-1])
            + [
                "version",
            ]
        )
        version_url = DataUrl(
            file_path=url.file_path(),
            data_path=version_data_path,
            scheme=url.scheme(),
        )
        try:
            version = get_data(version_url)
        except Exception:
            pass
        else:
            metadata["version"] = version
        if store:
            self.metadata = metadata
        return metadata

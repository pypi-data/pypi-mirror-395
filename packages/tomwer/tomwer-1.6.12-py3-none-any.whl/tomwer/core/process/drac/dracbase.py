from __future__ import annotations

import os
import numpy
import logging
import pathlib
from PIL import Image
from silx.io.url import DataUrl

from .binning import Binning
from .output import OutputFormat

from tomoscan.utils.io import filter_esrf_mounting_points
from tomoscan.esrf.scan.utils import get_data, from_bliss_original_file_to_raw

from tomwer.core.process.drac.output import DATASET_GALLERY_DIR_NAME
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase


_logger = logging.getLogger(__name__)

__all__ = [
    "DracDatasetBase",
]


class DracDatasetBase:
    """
    Abstract class for a drac dataset (that should be publish to the data portal).
    A drac dataset is defined by the following elements:
    * a directory
    * metadata
    """

    def __init__(self, data_dir: str, tomo_obj: TomwerObject) -> None:
        """
        :param data_dir: directory containing processed data
        :param tomo_obj: tomwer object referee for the processing
        """
        data_dir = pathlib.Path(data_dir).resolve()
        self._data_dir = filter_esrf_mounting_points(str(data_dir))
        self._tomo_obj = tomo_obj
        self._gallery_file_binning = Binning.FOUR_BY_FOUR
        self._gallery_output_format = OutputFormat.PNG
        self._gallery_overwrite = True

    @property
    def gallery_output_binning(self) -> Binning:
        "Binning factor to be used when saving gallery images"
        return self._gallery_file_binning

    @gallery_output_binning.setter
    def gallery_output_binning(self, binning: Binning):
        binning = Binning(binning)
        self._gallery_file_binning = binning

    @property
    def gallery_output_format(self) -> OutputFormat:
        "Output format of the images stored in the gallery"
        return self._gallery_output_format

    @gallery_output_format.setter
    def gallery_output_format(self, format: OutputFormat):
        format = OutputFormat(format)
        self._gallery_output_format = format

    @property
    def gallery_overwrite(self) -> bool:
        return self._gallery_overwrite

    @gallery_overwrite.setter
    def gallery_overwrite(self, overwrite: bool) -> None:
        self._gallery_overwrite = overwrite

    @property
    def dataset_name(self) -> str:
        """
        Return the name of the dataset to be given to the drac dataset.
        A drac dataset is store according to a (dataset_path, dataset_name). By default if several are pushed with the same key,
        only the most recent one will be stored
        """
        raise NotImplementedError("Base class")

    def get_gallery_dir(self) -> str:
        return os.path.join(self.data_dir, DATASET_GALLERY_DIR_NAME)

    def build_gallery(self):
        """callback to build the drac-dataset gallery"""
        pass

    @property
    def data_dir(self):
        return self._data_dir

    @property
    def tomo_obj(self):
        return self._tomo_obj

    @property
    def metadata(self) -> dict:
        raise NotImplementedError("Base class")

    @property
    def bliss_raw_datasets(self) -> tuple[str]:
        raise NotImplementedError("Base class")

    @staticmethod
    def from_scan_to_raws(scan: TomwerScanBase) -> tuple[str]:
        assert isinstance(
            scan, TomwerScanBase
        ), f"scan should be an instance of {TomwerScanBase}. Got {type(scan)}"
        bliss_original_files = scan.get_bliss_original_files()
        if bliss_original_files is None:
            bliss_original_files = ()
        return tuple(
            [
                from_bliss_original_file_to_raw(bliss_original_file)
                for bliss_original_file in bliss_original_files
            ]
        )

    def to_dict(self):
        return {
            "output_dir": self.data_dir,
            "drac_metadata": self.metadata,
        }

    def save_to_gallery(
        self,
        output_file_name: str,
        image: numpy.ndarray | DataUrl,
        lower_bound: float | None = None,
        upper_bound: float | None = None,
    ) -> None:
        format = self.gallery_output_format
        overwrite = self.gallery_overwrite
        binning = self.gallery_output_binning

        gallery_dir = self.get_gallery_dir()
        os.makedirs(gallery_dir, exist_ok=True)

        if isinstance(image, DataUrl):
            image = get_data(image)

        if image.ndim == 3 and image.shape[0] == 1:
            image = image.reshape(image.shape[1:])
        elif image.ndim != 2:
            raise ValueError(f"Only 2D grayscale images are handled. Got {image.shape}")

        # If both bounds are provided, apply clamping and normalization
        # If not it will use the min/max of each image
        if lower_bound is not None and upper_bound is not None:
            image = numpy.clip(image, lower_bound, upper_bound)
            image = image - lower_bound
            image *= 255.0 / (upper_bound - lower_bound)
        else:
            min_val, max_val = image.min(), image.max()
            image = image - min_val
            if max_val > min_val:  # Avoid division by zero if image is constant
                image *= 255.0 / (max_val - min_val)

        # Binning the data if required
        image = Binning._bin_data(data=image, binning=binning)

        # Convert to a PIL Image and save
        img = Image.fromarray(image.astype(numpy.uint8), mode="L")
        if not output_file_name.endswith(f".{format.value}"):
            output_file_name = output_file_name + f".{format.value}"
        if not overwrite and os.path.exists(output_file_name):
            raise OSError(f"File already exists ({output_file_name})")
        img.save(output_file_name)

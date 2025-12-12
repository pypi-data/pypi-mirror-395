from __future__ import annotations

import os
import numpy
from .dracbase import DracDatasetBase
from tomoscan.esrf.volume.singleframebase import VolumeSingleFrameBase
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.process.reconstruction.nabu.plane import NabuPlane
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_VOLUMES,
)
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_CAST_VOLUME,
)


__all__ = ["DracReconstructedVolumeDataset"]


class DracReconstructedVolumeDataset(DracDatasetBase):
    """
    Class to associate reconstructed volume(s) to an drac (processed) dataset
    """

    def __init__(self, tomo_obj: TomwerVolumeBase, source_scan: TomwerScanBase) -> None:
        if not isinstance(tomo_obj, TomwerVolumeBase):
            raise TypeError(
                f"tomo_obj should be an instance of {TomwerVolumeBase}. Got {type(tomo_obj)}"
            )

        super().__init__(tomo_obj=tomo_obj, data_dir=tomo_obj.icat_data_dir)
        self._n_slices_per_axis = 3
        self.__source_scan = source_scan
        self.__bliss_raw_dataset = self.from_scan_to_raws(scan=self.__source_scan)

    @staticmethod
    def make_serializable(obj):
        """
        Recursively convert numpy arrays to lists and replace string "None" with None in a given object.
        """
        if isinstance(obj, dict):
            return {
                key: DracReconstructedVolumeDataset.make_serializable(value)
                for key, value in obj.items()
            }
        elif isinstance(obj, (list, tuple)):
            return [
                DracReconstructedVolumeDataset.make_serializable(item) for item in obj
            ]
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return obj

    @property
    def metadata(self) -> dict:
        assert isinstance(self.tomo_obj, TomwerVolumeBase)
        metadata = self.tomo_obj.build_drac_metadata()
        metadata["Sample_name"] = self.source_scan.sample_name
        return metadata

    @property
    def dataset_name(self) -> str:
        """name to give to the drac (processed) dataset."""
        return PROCESS_FOLDER_RECONSTRUCTED_VOLUMES

    @property
    def source_scan(self) -> TomwerScanBase:
        return self.__source_scan

    @property
    def bliss_raw_datasets(self) -> tuple[str]:
        return self.__bliss_raw_dataset

    @property
    def n_slices_per_axis(self) -> int:
        "number of slices to sample per axis"
        return self._n_slices_per_axis

    @n_slices_per_axis.setter
    def n_slices_per_axis(self, n: int) -> None:
        self._n_slices_per_axis = n

    def get_slices_to_extract(self) -> tuple[tuple[int, tuple[int]]]:
        """
        Compute the slices to be retrieve along each dimension according to 'n_slices_per_axis'

        return tuple (A) is a two elements tuple. First element if the axis (B).
        Second is the tuple of indices to extract along the axis (B)
        indices are equally spaced in each dimensions
        """
        result: list[tuple[int, tuple[int]]] = []
        volume = self.tomo_obj
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"Volume is expected to be an instance of {TomwerVolumeBase}. Got {type(volume)}"
            )
        volume_shape = volume.get_volume_shape()
        for axis, axis_len in enumerate(volume_shape):
            for slice_index in numpy.linspace(
                0, axis_len, endpoint=False, num=self.n_slices_per_axis + 1
            )[1:]:
                result.append((axis, numpy.round(slice_index).astype(numpy.uint16)))
        return tuple(result)

    def build_gallery(self):
        gallery_dir = self.get_gallery_dir()
        volume = self.tomo_obj
        slices = volume.get_slices(slices=self.get_slices_to_extract())

        # Stack all slices into a single array to compute the global percentiles
        all_slices = numpy.concatenate([slice_ for slice_ in slices.values()])
        lower_bound = numpy.percentile(all_slices, 0)
        upper_bound = numpy.percentile(all_slices, 100)

        for (axis, slice_index), slice_ in slices.items():
            self.save_to_gallery(
                output_file_name=self.get_output_file_name(
                    output_dir=gallery_dir,
                    axis=axis,
                    slice_index=slice_index,
                    volume=volume,
                ),
                image=slice_,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )

    @staticmethod
    def get_output_file_name(
        output_dir: str, axis: int, slice_index: int, volume: TomwerVolumeBase
    ) -> str:
        axis = NabuPlane.from_value(axis)
        if isinstance(volume, VolumeSingleFrameBase):
            basename = volume.get_volume_basename()
        else:
            basename = os.path.splitext(os.path.basename(volume.data_url.file_path()))[
                0
            ]
        axis_folder = os.path.join(
            os.path.abspath(output_dir),
            str(axis.value),
        )
        os.makedirs(axis_folder, exist_ok=True)
        # warning: for ordering drac needs to have the axis in a dedicated folder
        return os.path.join(
            axis_folder,
            f"{basename}_capture_{axis.value}_{str(slice_index).zfill(6)}",
        )


class DracCastReconstructedVolume(DracReconstructedVolumeDataset):
    """
    Class to associate casted - reconstructed volume(s) to an drac (processed) dataset
    """

    @property
    def dataset_name(self) -> str:
        """name to give to the drac (processed) dataset."""
        return PROCESS_FOLDER_CAST_VOLUME

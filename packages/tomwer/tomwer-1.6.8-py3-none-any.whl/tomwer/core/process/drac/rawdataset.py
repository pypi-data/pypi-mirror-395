from __future__ import annotations

import numpy
import os
import shutil

from .dracbase import DracDatasetBase
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.hdf5scan import HDF5TomoScan
from tomoscan.esrf.scan.utils import from_bliss_original_file_to_raw
from tomwer.core.utils.dictutils import concatenate_dict
from tomwer.io.utils.raw_and_processed_data import to_raw_data_path

__all__ = [
    "DracRawDataset",
]


class DracRawDataset(DracDatasetBase):
    """
    Class to associate a raw dataset (TomwerScanBase) to an icat (raw) dataset
    """

    def __init__(
        self,
        tomo_obj: TomwerScanBase,
        raw_darks_required: bool = True,
        raw_flats_required: bool = True,
        raw_projections_required: bool = True,
        raw_projections_each: float = 90,
    ) -> None:
        if not isinstance(tomo_obj, TomwerScanBase):
            raise TypeError(
                f"tomo_obj should be an instance of {TomwerScanBase}. Got {type(tomo_obj)}"
            )
        data_dir = DracRawDataset.get_data_dir(scan=tomo_obj)
        super().__init__(data_dir=data_dir, tomo_obj=tomo_obj)
        self.__raw_darks_required = raw_darks_required
        self.__raw_flats_required = raw_flats_required
        self.__raw_projections_each = raw_projections_each
        self.__raw_projections_required = raw_projections_required

    @property
    def metadata(self) -> dict:
        scan = self.tomo_obj
        assert isinstance(scan, TomwerScanBase)
        if scan is not None:
            return scan.build_drac_metadata()
        else:
            return {}

    @property
    def bliss_raw_datasets(self) -> tuple[str]:
        return super().from_scan_to_raws(scan=self.tomo_obj)

    @property
    def raw_darks_required(self) -> bool:
        return self.__raw_darks_required

    @property
    def raw_flats_required(self) -> bool:
        return self.__raw_flats_required

    @property
    def raw_projections_each(self) -> float:
        return self.__raw_projections_each

    @property
    def raw_projections_required(self) -> bool:
        return self.__raw_projections_required

    def build_gallery(self):
        if os.path.exists(self.get_gallery_dir()):
            if self.gallery_overwrite:
                shutil.rmtree(self.get_gallery_dir())
            else:
                raise RuntimeError(
                    f"Gallery output dir ({self.get_gallery_dir()} already exists and cannot overwrite it.)"
                )
        scan = self.tomo_obj
        # collect all the data to be saved
        data_to_save: dict[str, numpy.ndarray] = {}
        if self.raw_darks_required and len(scan.darks) > 0:
            data_to_save["dark"] = next(iter(scan.darks.values()))
        if self.raw_flats_required and len(scan.flats) > 0:
            data_to_save["flat"] = next(iter(scan.flats.values()))
        if self.raw_projections_required:
            projections = scan.projections_with_angle()
            picked_angles = DracRawDataset.select_angles(
                angles_list=sorted(projections.keys()),
                each_angle=self.raw_projections_each,
            )
            data_to_save = concatenate_dict(
                data_to_save,
                {
                    f"projection_{angle:.1f}": projections[angle]
                    for angle in picked_angles
                },
            )

        # dump to disk
        for img_name, img_data in data_to_save.items():
            self.save_to_gallery(
                output_file_name=os.path.join(self.get_gallery_dir(), img_name),
                image=img_data,
            )

    @staticmethod
    def select_angles(angles_list: tuple, each_angle: int) -> tuple:
        angles_list = sorted(angles_list)
        if len(angles_list) > 0:
            start_angle = angles_list[0]
            stop_angle = angles_list[-1]
            picked_angle = numpy.arange(start_angle, stop_angle + 1, step=each_angle)
            return tuple(
                [
                    DracRawDataset.get_closest_projection(angle, angles_list)
                    for angle in picked_angle
                ]
            )
        else:
            return tuple()

    @staticmethod
    def get_closest_projection(angle, angles_list):
        idx_closest = numpy.argmin(numpy.abs(angles_list - angle))
        return angles_list[idx_closest]

    @staticmethod
    def get_data_dir(scan: HDF5TomoScan) -> str | None:
        """Deduce (bliss) data directory from a scan.
        If the scan can get the information from 'get_bliss_original_files' then we use it as this is most reliable information.
        Else we use the nxtomo location as a fallback (in case the data doesn't comes from bliss for example).
        """
        # the most reliable way is to get it from 'get_bliss_original_files' as this is set during conversion
        # else
        raw_data_file = scan.get_bliss_original_files()
        if scan.master_file is None:
            return None
        else:
            raw_data_file = to_raw_data_path(scan.master_file)
        return from_bliss_original_file_to_raw(os.path.dirname(raw_data_file))

from __future__ import annotations

import io
import json
import logging
import os
from glob import glob
import functools
import pathlib
from typing import Iterable

import numpy
from silx.io.url import DataUrl
from enum import Enum as _Enum
from pathlib import Path

from tomoscan.identifier import VolumeIdentifier
from tomoscan.normalization import IntensityNormalization
from tomoscan.volumebase import VolumeBase
from tomoscan.identifier import BaseIdentifier
from tomoscan.esrf.volume.utils import guess_volumes
from tomoscan.utils.io import filter_esrf_mounting_points

from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.utils.ftseriesutils import orderFileByLastLastModification
from tomwer.io.utils.raw_and_processed_data import (
    to_raw_data_path,
    to_processed_data_path,
)

logger = logging.getLogger(__name__)


class TomwerScanBase(TomwerObject):
    """
    Interface to extend tomoscan.TomoScanBase with custom functionality.
    ..warning:: All classes inheriting from this interface must also inherit from a child class of tomoscan.TomoScanBase
    """

    _DICT_DARK_REF_KEYS = "dark_ref_params"

    _DICT_NABU_RP_KEY = "nabu_params"

    _DICT_AXIS_KEYS = "axis_params"

    _DICT_SA_AXIS_KEYS = "sa_axis_params"

    _DICT_SA_DELTA_BETA_KEYS = "sa_delta_beta_params"

    _DICT_NORMALIZATION_KEY = "norm_params"

    VALID_RECONS_EXTENSION = ".edf", ".npy", ".npz", ".hdf5", ".tiff", ".jp2", ".vol"

    def __init__(self, overwrite_proc_file=False):
        super().__init__()
        self._stitching_metadata = None
        self._reconstructions = []

        self._nabu_params = None
        """nabu reconstruction parameters"""
        self._axis_params = None
        """Axis parameters"""
        self._saaxis_params = None
        """Information relative to saaxis"""
        self._sa_delta_beta_params = None
        """Information regarding sa_delta_beta_params"""
        self._dark_ref_params = None
        """Information regarding dark - ref reconstruction"""
        self._cache_proj_urls = None
        """cache for the projection urls"""
        self._cache_radio_axis = {}
        """cache for the radio axis. Key is tuple (mode, nearest), value is
        (url1, url2)"""
        self._notify_ffc_rsc_missing = True
        """Should we notify the user if ffc fails because cannot find dark or
        flat. Used to avoid several warnings. Only display one"""
        self._latest_reconstructions = []
        "list of url related to latest slice reconstruction from nabu"
        self._latest_vol_reconstructions = []
        """list of url related to latest volume reconstruction from nabu"""
        self._reconstruction_paths = set()
        """set of paths containing reconstructions of the scan. Make sure we have an entry point for it"""
        self._proposal_name = None

    def _clear_heavy_cache(self):
        """For scan for now we don't want to remove any information from the cache.
        Mor eusefull for volume use case
        """
        pass

    @property
    def resolved_path(self) -> str | None:
        """
        return tomoscan 'path' with link resolved
        """
        if self.path is None:  # pylint: disable=E1101
            return None
        return filter_esrf_mounting_points(
            str(Path(self.path).resolve())  # pylint: disable=E1101
        )

    @property
    def working_directory(self) -> Path | None:
        """
        working directory once all links have been solved (required for submitting jobs to slurm)
        """
        if self.working_directory is None:
            return None
        return pathlib.Path(self.working_directory)

    def clear_cache(self):
        self._cache_proj_urls = None
        self._notify_ffc_rsc_missing = True
        super().clear_cache()

    def _flat_field_correction(
        self,
        data,
        index_proj: int | None,
        dark,
        flat1,
        flat2,
        index_flat1: int,
        index_flat2: int,
    ):
        """
        compute flat field correction for a provided data from is index
        one dark and two flats (require also indexes)
        """
        if not isinstance(data, numpy.ndarray):
            raise TypeError("data is expected to be an instance of numpy.ndarray")
        can_process = True

        if dark is None:
            if self._notify_ffc_rsc_missing:
                logger.warning("cannot make flat field correction, dark not found")
            can_process = False

        if dark is not None and dark.ndim != 2:
            logger.error(
                "cannot make flat field correction, dark should be of " "dimension 2"
            )
            can_process = False

        if flat1 is None:
            if self._notify_ffc_rsc_missing:
                logger.warning("cannot make flat field correction, flat not found")
            can_process = False
        elif not isinstance(flat1, numpy.ndarray):
            raise TypeError("flat1 is expected to be an instance of numpy.ndarray")
        else:
            if flat1.ndim != 2:
                logger.error(
                    "cannot make flat field correction, flat should be of "
                    "dimension 2"
                )
                can_process = False
            if flat2 is not None and flat1.shape != flat2.shape:
                logger.error("the tow flats provided have different shapes.")
                can_process = False

        if dark is not None and flat1 is not None and dark.shape != flat1.shape:
            logger.error("Given dark and flat have incoherent dimension")
            can_process = False

        if dark is not None and data.shape != dark.shape:
            logger.error(
                "Image has invalid shape. Cannot apply flat field" "correction it"
            )
            can_process = False

        if can_process is False:
            self._notify_ffc_rsc_missing = False
            return data

        if flat2 is None:
            flat_value = flat1
        else:
            # compute weight and clip it if necessary
            if index_proj is None:
                w = 0.5
            else:
                w = (index_proj - index_flat1) / (index_flat2 - index_flat1)
                w = min(1, w)
                w = max(0, w)
            flat_value = flat1 * w + flat2 * (1 - w)

        div = flat_value - dark
        div[div == 0] = 1
        return (data - dark) / div

    @property
    def reconstructions(self):
        """list of reconstruction files"""
        return self._reconstructions

    @reconstructions.setter
    def reconstructions(self, reconstructions):
        self._reconstructions = reconstructions

    @property
    def reconstruction_paths(self):
        return self._reconstruction_paths

    def add_reconstruction_path(self, path: str):
        self._reconstruction_paths.add(path)

    @property
    def nabu_recons_params(self):
        return self._nabu_params

    @nabu_recons_params.setter
    def nabu_recons_params(self, recons_params):
        self._nabu_params = recons_params

    @property
    def axis_params(self):
        return self._axis_params

    @axis_params.setter
    def axis_params(self, parameters):
        self._axis_params = parameters

    @property
    def saaxis_params(self):
        return self._saaxis_params

    @saaxis_params.setter
    def saaxis_params(self, saaxis_params):
        self._saaxis_params = saaxis_params

    @property
    def sa_delta_beta_params(self):
        return self._sa_delta_beta_params

    @sa_delta_beta_params.setter
    def sa_delta_beta_params(self, sa_delta_beta_params):
        self._sa_delta_beta_params = sa_delta_beta_params

    # TODO: change name. Should be generalized to return Dataurl
    def getReconstructedFilesFromParFile(self, with_index):
        raise NotImplementedError("Base class")

    def projections_with_angle(self):
        raise NotImplementedError("Base class")

    def scan_dir_name(self) -> str | None:
        """return name of the directory containing the acquisition"""
        raise NotImplementedError("Base class")

    def scan_basename(self) -> str | None:
        """return basename of the directory containing the acquisition"""
        raise NotImplementedError("Base class")

    def scan_parent_dir_basename(self) -> str | None:
        """return parent basename of the directory containing the acquisition"""
        raise NotImplementedError("Base class")

    @functools.lru_cache(maxsize=3)
    def get_opposite_projections(self, mode) -> tuple:
        """
        Return the two best opposite projections for the required mode.
        """
        radios_with_angle = self.projections_with_angle()
        angles = (
            numpy.array(
                tuple(
                    filter(
                        lambda a: numpy.issubdtype(type(a), numpy.number),
                        radios_with_angle.keys(),
                    )
                )
            )
            % 360
        )

        from tomwer.core.process.reconstruction.axis.anglemode import CorAngleMode
        from ..process.reconstruction.axis.params import (
            AxisResource,
        )  # avoid cyclic import

        mode = CorAngleMode.from_value(mode)

        if len(angles) < 2:
            logger.warning("less than two angles found. Unable to get opposite angles")
            return None, None

        initial_angle = angles[0] % 360
        if mode in (CorAngleMode.use_0_180, CorAngleMode.manual_selection):
            couples = (initial_angle, (initial_angle + 180.0) % 360)
        elif mode is CorAngleMode.use_90_270:
            couples = ((initial_angle + 90.0) % 360, (initial_angle + 270.0) % 360)
        else:
            raise ValueError(f"{mode} is not handle")

        def find_nearest(angles: numpy.ndarray, angle: float):
            if len(angles) == 0:
                return None
            dist = numpy.abs(angles % 360 - angle)
            idx = dist.argmin()
            if isinstance(idx, numpy.ndarray):
                idx = idx[0]
            return angles[idx]

        nearest_c1 = find_nearest(angles=angles, angle=couples[0])
        nearest_c2 = find_nearest(angles=angles, angle=couples[1])
        if nearest_c1 is not None and nearest_c2 is not None:
            return (
                AxisResource(radios_with_angle[nearest_c1], angle=nearest_c1),
                AxisResource(radios_with_angle[nearest_c2], angle=nearest_c2),
            )
        else:
            return None, None

    def data_flat_field_correction(
        self, data: numpy.ndarray, index: int | None = None
    ) -> numpy.ndarray:
        """Apply flat field correction on the given data

        :param data: the data to apply correction on
        :param index: index of the data in the acquisition
                                      sequence
        :return: corrected data
        """
        raise NotImplementedError("Base class")

    def to_dict(self):
        res = {}
        # nabu reconstruction parameters
        if self._nabu_params:
            res[self._DICT_NABU_RP_KEY] = (
                self.nabu_recons_params
                if isinstance(self.nabu_recons_params, dict)
                else self.nabu_recons_params.to_dict()
            )
        else:
            res[self._DICT_NABU_RP_KEY] = None
        # axis reconstruction parameters
        if self.axis_params is None:
            res[self._DICT_AXIS_KEYS] = None
        else:
            res[self._DICT_AXIS_KEYS] = self.axis_params.to_dict()
        # saaxis reconstruction parameters
        if self.saaxis_params is None:
            res[self._DICT_SA_AXIS_KEYS] = None
        else:
            res[self._DICT_SA_AXIS_KEYS] = self.saaxis_params.to_dict()
        # sa delta-beta reconstruction parameters
        if self._sa_delta_beta_params is None:
            res[self._DICT_SA_DELTA_BETA_KEYS] = None
        else:
            res[self._DICT_SA_DELTA_BETA_KEYS] = self.sa_delta_beta_params.to_dict()
        # dark ref
        if self._dark_ref_params is None:
            res[self._DICT_DARK_REF_KEYS] = None
        else:
            res[self._DICT_DARK_REF_KEYS] = self._dark_ref_params.to_dict()
        # normalization
        if self.intensity_normalization is None:
            res[self._DICT_NORMALIZATION_KEY] = None
        else:
            res[self._DICT_NORMALIZATION_KEY] = self.intensity_normalization.to_dict()

        return res

    def load_from_dict(self, desc):
        from tomwer.core.process.reconstruction.axis.params import (
            AxisRP,
        )  # avoid cyclic import

        if isinstance(desc, io.TextIOWrapper):
            data = json.load(desc)
        else:
            data = desc
        if not (
            self.DICT_PATH_KEY in data  # pylint: disable=E1101
            and data[self.DICT_TYPE_KEY] == self._TYPE  # pylint: disable=E1101
        ):
            raise ValueError("Description is not an EDFScan json description")

        assert self.DICT_PATH_KEY in data  # pylint: disable=E1101
        # load axis reconstruction parameters
        axis_params = data.get(self._DICT_AXIS_KEYS, None)
        if axis_params is not None:
            self.axis_params = AxisRP.from_dict(axis_params)
        # load nabu reconstruction parameters
        if self._DICT_NABU_RP_KEY in data:
            self._nabu_params = data[self._DICT_NABU_RP_KEY]
        # load dark-ref parameters
        dark_ref_params = data.get(self._DICT_DARK_REF_KEYS, None)
        if dark_ref_params is not None:
            from tomwer.core.process.reconstruction.darkref.params import DKRFRP

            self._dark_ref_params = DKRFRP.from_dict(dark_ref_params)
        # load normalization
        intensity_normalization = data.get(self._DICT_NORMALIZATION_KEY, None)
        if intensity_normalization is not None:
            self.intensity_normalization = IntensityNormalization.from_dict(
                intensity_normalization
            )
        # load saaxis parameters
        saaxis_params = data.get(self._DICT_SA_AXIS_KEYS, None)
        if saaxis_params is not None:
            from tomwer.core.process.reconstruction.saaxis.params import SAAxisParams

            self._saaxis_params = SAAxisParams.from_dict(saaxis_params)
        # load sa delta beta parameters
        sa_delta_beta_params = data.get(self._DICT_SA_DELTA_BETA_KEYS, None)
        if sa_delta_beta_params is not None:
            from tomwer.core.process.reconstruction.sadeltabeta.params import (
                SADeltaBetaParams,
            )

            self._sa_delta_beta_params = SADeltaBetaParams.from_dict(
                sa_delta_beta_params
            )

    def equal(self, other):
        """

        :param other: instance to compare with
        :return: True if instance are equivalent

        :note: we cannot use the __eq__ function because this object need to be picklable
        """
        return (
            isinstance(other, self.__class__)
            or isinstance(self, other.__class__)
            and self.type == other.type  # pylint: disable=E1101
            and self.nabu_recons_params == other.nabu_recons_params
            and self.path == other.path  # pylint: disable=E1101
        )

    def get_sinogram(
        self, line: int, subsampling: int = 1, norm_method=None, **kwargs
    ) -> numpy.ndarray:
        """
        extract the sinogram from projections

        :param line: which sinogram we want
        :param subsampling: subsampling to apply on the sinogram
        :return: sinogram from the radio lines
        """
        raise NotImplementedError("Base class")

    def get_normed_sinogram(self, line: int, subsampling: int = 1) -> numpy.ndarray:
        """
        Util to get the sinogram normed with settings currently defined
        on the 'intensity_normalization' property

        :param line:
        :param subsampling:
        :return:
        """
        return self.get_sinogram(
            line=line,
            subsampling=subsampling,
            norm_method=self.intensity_normalization.method,
            **self.intensity_normalization.get_extra_infos(),
        )

    def __str__(self):
        raise NotImplementedError("Base class")

    @staticmethod
    def get_pyhst_recons_file(scanID):
        """Return the .par file used for the current reconstruction if any.
        Otherwise return None"""
        if scanID == "":
            return None

        if scanID is None:
            raise RuntimeError("No current acquisition to validate")
        assert type(scanID) is str
        assert os.path.isdir(scanID)
        folderID = os.path.basename(scanID)
        # look for fasttomo files ending by slice.par
        parFiles = glob(os.path.join(scanID + folderID) + "*_slice.par")
        if len(parFiles) > 0:
            return orderFileByLastLastModification(scanID, parFiles)[-1]
        else:
            return None

    def _deduce_transfert_scan(self, output_dir):
        """
        Create the scan that will be generated if this scan is
        copy to the output_dir

        :param output_dir:
        """
        raise NotImplementedError("Base class")

    def get_proj_angle_url(
        self, use_cache: bool = True, *args, **kwargs
    ) -> dict[int | str, DataUrl]:
        """
        retrieve the url for each projections (including the alignment /
        return one) and associate to each (if possible) the angle.
        Alignment angle are set as angle (1) to specify that this is an
        alignment one.
        :param use_cache:
        :return: dictionary with angle (str or int) as key and url as value
        """
        raise NotImplementedError("Base class")

    def get_reconstructed_slices(self) -> set[str]:
        """
        Return a set of all the reconstructed **slices** that can be discovered for the scan (it will only look for reconstructed slices and not the volumes!!!!)
        slices are given as a string representing volume identifier
        """
        from tomwer.core.process.reconstruction.output import (
            PROCESS_FOLDER_RECONSTRUCTED_SLICES,
        )  # avoid cyclic import

        all_recons_ids = set()
        recons_paths = self.reconstruction_paths
        # extend set reconstruction paths to some 'default' paths.
        if self.working_directory is not None:
            # default output folder if using working directory
            working_dir_output_folder = os.path.join(
                str(self.working_directory),
                PROCESS_FOLDER_RECONSTRUCTED_SLICES,
            )
            # add possible output folder: in raw_data (deprecated)
            raw_data_output_folder = to_raw_data_path(working_dir_output_folder)
            recons_paths.add(raw_data_output_folder)
            # add expected output folder: in processed data
            processed_data_output_folder = to_processed_data_path(
                working_dir_output_folder
            )
            recons_paths.add(processed_data_output_folder)

        for path in recons_paths:
            all_recons_ids.update(self.get_reconstructed_slices_from_path(path))
        return all_recons_ids

    def get_reconstructed_slices_from_path(self, path, check_url=False) -> set[str]:
        """
        Look for some reconstructed slices at a specific position
        slices are given as a string representing volume identifier
        """
        if path is None or not os.path.exists(path):
            return set()

        volumes = guess_volumes(path) or ()
        # note: guess_volumes will find a volume only if the path fits a volume location
        # like a hdf5 file containing a volume or a top level EDF volume folder.
        # In the case path = xxx/reconstructed_slices for example it returns an empty set.
        if len(volumes) > 0:
            return set(
                [volume.get_identifier().to_str() for volume in guess_volumes(path)]
            )
        elif os.path.isdir(path):
            # in the case the location is a folder and doesn't fit any volume
            # we want to look into sub folders
            from tomwer.core.process.reconstruction.saaxis.saaxis import (
                DEFAULT_RECONS_FOLDER as MULTI_COR_DEFAULT_FOLDER,
            )
            from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
                DEFAULT_RECONS_FOLDER as MULTI_DB_DEFAULT_FOLDER,
            )
            from tomwer.core.process.reconstruction.nabu.settings import (
                NABU_CFG_FILE_FOLDER,
            )

            res = set()
            filtered_name = (
                "steps_file_basename_nabu_sinogram_save_step",
                MULTI_COR_DEFAULT_FOLDER,
                MULTI_DB_DEFAULT_FOLDER,
                NABU_CFG_FILE_FOLDER,
            )
            # filter files that we already know they won't contain any reconstructed volume
            sub_files = filter(
                lambda name: name not in filtered_name,
                os.listdir(path),
            )
            for f in sub_files:
                current_path = os.path.join(path, f)
                res.update(
                    self.get_reconstructed_slices_from_path(
                        path=current_path, check_url=check_url
                    )
                )
            return res
        return set()

    @property
    def latest_reconstructions(self):
        """List of latest slices reconstructions (as VolumeIdentifier) - single slice volume"""
        return self._latest_reconstructions

    @property
    def latest_vol_reconstructions(self):
        """List of latest volume reconstructions (as VolumeIdentifier)"""
        return self._latest_vol_reconstructions

    def clear_latest_reconstructions(self):
        self._latest_reconstructions = []

    def set_latest_reconstructions(self, urls: Iterable):
        if urls is None:
            self._latest_reconstructions = None
        else:
            self._latest_reconstructions = list(
                [self._process_volume_url(url) for url in urls]
            )

    def add_latest_reconstructions(self, urls: Iterable):
        self._latest_reconstructions.extend(urls)

    def clear_latest_vol_reconstructions(self):
        self._latest_vol_reconstructions = []

    @staticmethod
    def _process_volume_url(url):
        if isinstance(url, str):
            return VolumeIdentifier.from_str(url)
        elif isinstance(url, VolumeIdentifier):
            return url
        elif isinstance(url, VolumeBase):
            return url.get_identifier()
        else:
            raise TypeError(
                f"url should be a {VolumeIdentifier} or a string reprenseting a {VolumeIdentifier}. {type(url)} provided instead"
            )

    def set_latest_vol_reconstructions(self, volume_identifiers: Iterable | None):
        volume_identifiers = volume_identifiers or tuple()
        self._latest_vol_reconstructions = list(
            [self._process_volume_url(url) for url in volume_identifiers]
        )

    def add_latest_vol_reconstructions(self, volume_identifiers: tuple):
        assert isinstance(
            volume_identifiers, tuple
        ), "volume_identifiers is expected to be a tuple"
        self._latest_vol_reconstructions.extend(
            self._process_volume_url(volume_identifier)
            for volume_identifier in volume_identifiers
        )

    def _update_latest_recons_identifiers(self, old_path, new_path):
        def update_identifier(identifier):
            assert isinstance(
                identifier, BaseIdentifier
            ), f"identifier is expected to be an instance of {BaseIdentifier}"
            # small hack as this is not much used: simply try to replace a path by another. this is only used by the data transfer and EDF / SPEC
            # this time is almost over
            # FIXME: correct way to do this would be to recreate the volume, modify file or folder path and
            # recreate the new identifier
            identifier.replace(old_path, new_path, 1)

        self._latest_reconstructions = [
            update_identifier(identifier=identifier)
            for identifier in self._latest_reconstructions
        ]

        self._latest_vol_reconstructions = [
            update_identifier(identifier=identifier)
            for identifier in self._latest_vol_reconstructions
        ]

    def get_url_proj_index(self, url):
        """Return the index in the acquisition from the url"""

        def invert_dict(ddict):
            res = {}
            if ddict is not None:
                for key, value in ddict.items():
                    assert isinstance(value, DataUrl)
                    res[value.path()] = key
            return res

        proj_inv_url_to_index = invert_dict(self.projections)  # pylint: disable=E1101
        alig_inv_url_to_index = invert_dict(
            self.alignment_projections  # pylint: disable=E1101
        )
        if url.path() in proj_inv_url_to_index:
            return proj_inv_url_to_index[url.path()]
        elif url.path() in alig_inv_url_to_index:
            return alig_inv_url_to_index[url.path()]
        else:
            return None

    def get_nabu_dataset_info(self, binning=1, binning_z=1, proj_subsampling=1) -> dict:
        """

        :return: nabu dataset descriptor
        """
        raise NotImplementedError("Base class")

    def to_nabu_dataset_analyser(self):
        """Return the equivalent DatasetAnalyzer for nabu"""
        raise NotImplementedError("Base class")

    def get_proposal_name(self) -> str | None:
        return self._proposal_name

    def set_proposal_name(self, proposal_name: str) -> None:
        self._proposal_name = proposal_name


class _TomwerBaseDock(object):
    """
    Internal class to make difference between a simple TomoBase output and
    an output for a different processing (like scanvalidator.UpdateReconsParam)
    """

    def __init__(self, tomo_instance):
        self.__instance = tomo_instance

    @property
    def instance(self):
        return self.__instance


def _containsDigits(input_):
    return any(char.isdigit() for char in input_)


class NormMethod(_Enum):
    MANUAL_ROI = "manual ROI"
    AUTO_ROI = "automatic ROI"
    DATASET = "from dataset"

"""
This module provides global definitions and functions to manage dark and flat fields
especially for tomo experiments and workflows
"""

from __future__ import annotations

import logging
import os
from queue import Queue

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from tomwer.core.utils.deprecation import deprecated_warning

from tomoscan.framereducer.target import REDUCER_TARGET
from tomoscan.framereducer.method import ReduceMethod

import tomwer.version
from tomwer.core import settings
from tomwer.core.utils.lbsram import is_low_on_memory
from tomwer.core.process.task import Task
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.utils import docstring

from . import params as dkrf_reconsparams

logger = logging.getLogger(__name__)


class DarkRefsTask(
    Task,
    SuperviseProcess,
    Queue,  # TODO: fixme: this does not make much sense for a task
    input_names=("data",),
    output_names=("data",),
    optional_input_names=("serialize_output_data",),
):
    """Compute median/mean dark and ref from originals (dark and ref files)"""

    WHAT_REF = "refs"
    WHAT_DARK = "dark"

    VALID_WHAT = (WHAT_REF, WHAT_DARK)
    """Tuple of valid option for What"""

    info_suffix = ".info"

    TOMO_N = "TOMO_N"

    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        """

        :param file_ext:
        :param reconsparams: reconstruction parameters
        """
        Task.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        SuperviseProcess.__init__(self, process_id=process_id)
        Queue.__init__(self)

        if inputs is None:
            inputs = {}
        if "recons_params" in inputs or "reconsparams" in inputs:
            raise ValueError(
                "wrong key: recons_params / reconsparams use dark_ref_params instead"
            )
        self._recons_params = inputs.get("dark_ref_params", None)
        if self._recons_params is None:
            self._recons_params = dkrf_reconsparams.DKRFRP()
        elif isinstance(self._recons_params, dict):
            self._recons_params = dkrf_reconsparams.DKRFRP.from_dict(
                self._recons_params
            )
        if not isinstance(self._recons_params, dkrf_reconsparams.DKRFRP):
            raise TypeError(
                f"'reconsparams' should be an instance of {dkrf_reconsparams.DKRFRP} or {dict}. Not {type(self._recons_params)}"
            )
        self._file_ext = inputs.get("file_ext", ".edf")
        if not type(self._file_ext) is str:
            raise TypeError("'file_ext' is expected to be a string")

        self._forceSync = inputs.get("force_sync", False)
        self.__new_hdf5_entry_created = False
        "used to know if the process has generated a new entry or not"

    @property
    def recons_params(self):
        return self._recons_params

    def set_recons_params(self, recons_params):
        if isinstance(recons_params, dkrf_reconsparams.DKRFRP):
            self._recons_params = recons_params
        else:
            raise TypeError(
                "recons_params should be an instance of " "ReconsParams or DKRFRP"
            )

    def setPatternRecons(self, pattern):
        self._patternReconsFile = pattern

    def setForceSync(self, b):
        self._forceSync = True

    @staticmethod
    def getRefHSTFiles(directory, prefix, file_ext=".edf"):
        """

        :return: the list of existing refs files in the directory according to
                 the file pattern.
        """
        assert isinstance(directory, str)
        res = []
        if os.path.isdir(directory) is False:
            logger.error(
                directory + " is not a directory. Cannot extract " "RefHST files"
            )
            return res

        for file in os.listdir(directory):
            if file.startswith(prefix) and file.endswith(file_ext):
                res.append(os.path.join(directory, file))
                assert os.path.isfile(res[-1])
        return res

    @staticmethod
    def getDarkHSTFiles(directory, prefix, file_ext=".edf"):
        """

        :return: the list of existing refs files in the directory according to
                 the file pattern.
        """
        res = []
        if os.path.isdir(directory) is False:
            logger.error(
                directory + " is not a directory. Cannot extract " "DarkHST files"
            )
            return res
        for file in os.listdir(directory):
            _prefix = prefix
            if prefix.endswith(file_ext):
                _prefix = prefix.rstrip(file_ext)
            if file.startswith(_prefix) and file.endswith(file_ext):
                _file = file.lstrip(_prefix).rstrip(file_ext)
                if _file == "" or _file.isnumeric() is True:
                    res.append(os.path.join(directory, file))
                    assert os.path.isfile(res[-1])
        return res

    @staticmethod
    def getDarkPatternTooltip():
        return (
            "define the pattern to find, using the python `re` library.\n"
            "For example: \n"
            "   - `.*conti_dark.*` to filter files containing `conti_dark` sentence\n"
            "   - `darkend[0-9]{3,4}` to filter files named `darkend` followed by three or four digit characters (and having the .edf extension)"
        )

    @staticmethod
    def getRefPatternTooltip():
        return (
            "define the pattern to find, using the python `re` library.\n"
            "For example: \n"
            "   - `.*conti_ref.*` for files containing `conti_dark` sentence\n"
            "   - `ref*.*[0-9]{3,4}_[0-9]{3,4}` to filter files named `ref` followed by any character and ending by X_Y where X and Y are groups of three or four digit characters."
        )

    @staticmethod
    def properties_help():
        return """
        - refs: 'None', 'Median', 'Average', 'First', 'Last' \n
        - dark: 'None', 'Median', 'Average', 'First', 'Last' \n
        """

    def set_configuration(self, properties):
        # No properties stored for now
        if "dark" in properties:
            self._recons_params.dark_calc_method = properties["dark"]
        if "refs" in properties:
            self._recons_params.flat_calc_method = properties["refs"]
        if "_rpSetting" in properties:
            self._recons_params.load_from_dict(properties["_rpSetting"])
        else:
            self._recons_params.load_from_dict(properties)

    def run(self):
        if isinstance(self.inputs.data, str):
            try:
                scan = data_identifier_to_scan(self.inputs.data)
            except ValueError:
                # in the case fails to cast str to identifier (data can be a simple folder in the case of dark ref)
                scan = self.inputs.data
        else:
            scan = self.inputs.data

        if scan is None:
            self.outputs.data = None
            return

        if type(scan) is str:
            assert os.path.exists(scan)
            scan = ScanFactory.create_scan_object(scan_path=scan)
        elif isinstance(scan, TomwerScanBase):
            pass
        elif isinstance(scan, dict):
            scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            raise TypeError(
                "scan should be an instance of TomoBase or path to " "scan dircetory"
            )
        assert isinstance(self._recons_params, dkrf_reconsparams.DKRFRP)
        assert self._recons_params is not None

        ProcessManager().notify_dataset_state(
            dataset=scan,
            process=self,
            state=DatasetState.ON_GOING,
        )
        logger.processStarted(f"start dark and ref for {scan}")
        if (
            settings.isOnLbsram(scan)
            and is_low_on_memory(settings.get_lbsram_path()) is True
        ):
            mess = (
                "low memory, do compute dark and flat field mean/median "
                "for %s" % scan.path
            )
            logger.processSkipped(mess)
            ProcessManager().notify_dataset_state(
                dataset=scan,
                process=self,
                state=DatasetState.SKIPPED,
                details=mess,
            )
            self.outputs.data = None
            return

        if not (scan and os.path.exists(scan.path)):
            mess = f"folder {scan.folder} is not existing"
            logger.warning(mess)
            ProcessManager().notify_dataset_state(
                dataset=scan, process=self, state=DatasetState.FAILED, details=mess
            )

            self.outputs.data = None
            return
        whats = (DarkRefsTask.WHAT_REF, DarkRefsTask.WHAT_DARK)
        overwrites = (
            self.recons_params.overwrite_flat,
            self.recons_params.overwrite_dark,
        )
        modes = (
            self.recons_params.flat_calc_method,
            self.recons_params.dark_calc_method,
        )
        has_reduced = (
            scan.reduced_flats not in (None, {}),
            scan.reduced_darks not in (None, {}),
        )

        for what, mode, overwrite, exists in zip(whats, modes, overwrites, has_reduced):
            # if reduced already exists and user didn't asked for overwritting it
            if exists and not overwrite:
                continue
            logger.debug(f"compute {what} using mode {mode} for {scan}")
            try:
                self.compute(scan=scan, target=what, method=mode, overwrite=True)
            except Exception as e:
                info = f"Fail computing dark and flat for {scan}. Reason is {e}"
                self.notify_to_state_to_managed(
                    dataset=scan, state=DatasetState.FAILED, details=info
                )
                logger.processFailed(info)
                self.outputs.data = None
                return
        results = {}
        interpretations = {}
        if (
            self.recons_params.dark_calc_method
            is not dkrf_reconsparams.ReduceMethod.NONE
            and scan.reduced_darks is not None
        ):
            # cast darks and flats keys from int (index) to str
            o_darks = scan.reduced_darks
            o_darks_infos = scan.reduced_darks_infos
            f_darks = {}
            for index, data in o_darks.items():
                f_darks[str(index)] = data
                interpretations["/".join(("darks", str(index)))] = "image"
            results["darks"] = f_darks

            scan.save_reduced_darks(f_darks, darks_infos=o_darks_infos, overwrite=True)
        if (
            self.recons_params.flat_calc_method
            is not dkrf_reconsparams.ReduceMethod.NONE
            and scan.reduced_flats is not None
        ):
            results["flats"] = scan.reduced_flats
            o_flats = scan.reduced_flats
            o_flats_infos = scan.reduced_flats_infos
            f_flats = {}
            for index, data in o_flats.items():
                f_flats[str(index)] = data
                interpretations["/".join(("flats", str(index)))] = "image"
            results["flats"] = f_flats

            scan.save_reduced_flats(f_flats, flats_infos=o_flats_infos, overwrite=True)

        logger.processSucceed(f"Dark and flat reduction succeeded for {scan}")
        self.notify_to_state_to_managed(
            dataset=scan, state=DatasetState.SUCCEED, details=None
        )

        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = scan.to_dict()
        else:
            self.outputs.data = scan

    @staticmethod
    def _target_to_reducer_target(target):
        """
        util to insure connection between 'historical' tomwer dark / ref and latest tomoscan FrameReducer
        """
        if target == "refs":
            return REDUCER_TARGET.FLATS
        elif target == "dark":
            return REDUCER_TARGET.DARKS
        return REDUCER_TARGET(target)

    def compute(
        self, scan, target: REDUCER_TARGET, method: ReduceMethod, overwrite: bool
    ):
        target = self._target_to_reducer_target(target)
        method = ReduceMethod(method)
        if target is REDUCER_TARGET.DARKS:
            reduced_darks, metadata = scan.compute_reduced_darks(
                reduced_method=method,
                overwrite=overwrite,
                return_info=True,
            )
            scan.set_reduced_darks(darks=reduced_darks, darks_infos=metadata)

            try:
                scan.save_reduced_darks(
                    darks=reduced_darks, darks_infos=metadata, overwrite=True
                )
            except Exception as e:
                logger.error(f"Fail to save reduced darks. Error is {e}")
        elif target is REDUCER_TARGET.FLATS:
            reduced_flats, metadata = scan.compute_reduced_flats(
                reduced_method=method,
                overwrite=overwrite,
                return_info=True,
            )
            scan.set_reduced_flats(flats=reduced_flats, flats_infos=metadata)

            try:
                scan.save_reduced_flats(
                    flats=reduced_flats, flats_infos=metadata, overwrite=True
                )
            except Exception as e:
                logger.error(f"Fail to save reduced flats. Error is {e}")
        else:
            raise RuntimeError(f"{target} not handled")

    @docstring(Task.program_name)
    @staticmethod
    def program_name():
        return "tomwer_dark_refs"

    @docstring(Task.program_version)
    @staticmethod
    def program_version():
        return tomwer.version.version

    @docstring(Task.definition)
    @staticmethod
    def definition():
        return "Compute mean or median dark and refs per each series"


def requires_reduced_dark_and_flat(
    scan: TomwerScanBase, logger_: logging.Logger | None = None
) -> tuple:
    r"""helper function: If no dark / flat are computed yet then will pick the first
    dark and the first flat.

    Expected usage: for tomwer application which requires some time and flat and to avoid some warnings
    within standalones.

    :params scan: scan for which we want to get quick dark and flat
    :params logger\_: if provided will add some warning when attempt to get reduced flat / dark.
    :returns: tuple of what was missing and has been computed
    """
    computed = []
    if scan.reduced_flats in (None, {}):
        # set the first flat found
        recons_params = dkrf_reconsparams.DKRFRP()
        recons_params.overwrite_dark = False
        recons_params.overwrite_flat = False
        recons_params.dark_calc_method = dkrf_reconsparams.ReduceMethod.NONE
        recons_params.flat_calc_method = dkrf_reconsparams.ReduceMethod.FIRST

        drp = DarkRefsTask(
            inputs={
                "data": scan,
                "dark_ref_params": recons_params,
                "serialize_output_data": False,
            }
        )
        if logger_ is not None:
            logger.warning(
                "No 'reduced' flat found. Will try to pick the first flat found as the `calculated` flat."
            )
        drp.run()
        computed.append("flat")

    if scan.reduced_darks in (None, {}):
        # set the first dark found
        recons_params = dkrf_reconsparams.DKRFRP()
        recons_params.overwrite_dark = False
        recons_params.overwrite_flat = False
        recons_params.dark_calc_method = dkrf_reconsparams.ReduceMethod.FIRST
        recons_params.flat_calc_method = dkrf_reconsparams.ReduceMethod.NONE

        drp = DarkRefsTask(
            inputs={
                "data": scan,
                "dark_ref_params": recons_params,
                "serialize_output_data": False,
            }
        )
        if logger_ is not None:
            logger.warning(
                "No 'reduced' dark found. Will try to pick the first flat found as the `calculated` dark."
            )
        drp.run()
        computed.append("dark")

    return tuple(computed)


class DarkRefs(DarkRefsTask):
    def __init__(
        self,
        process_id=None,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        deprecated_warning(
            name="tomwer.core.process.reconstruction.darkref.darkref.DarkRefs",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="DarkRefsTask",
        )
        super().__init__(process_id, varinfo, inputs, node_id, node_attrs, execinfo)

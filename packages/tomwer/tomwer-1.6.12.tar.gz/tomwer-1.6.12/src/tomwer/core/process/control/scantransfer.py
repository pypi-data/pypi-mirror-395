from __future__ import annotations

import fnmatch
import logging
import os
import shutil

from tomoscan.esrf.scan.utils import get_unique_files_linked
import tomwer.version
from tomwer.core.utils.deprecation import deprecated_warning
from tomwer.core.process.reconstruction.nabu.settings import NABU_CFG_FILE_FOLDER
from tomwer.core.process.reconstruction.nabu.utils import update_cfg_file_after_transfer
from tomwer.core.process.task import Task
from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.settings import get_dest_path, get_lbsram_path
from tomwer.core.signal import Signal
from tomwer.core.utils import logconfig
from tomwer.core.utils.spec import rebaseParFile
from tomwer.core.utils.scanutils import data_identifier_to_scan
from tomwer.io.utils import get_linked_files_with_entry
from tomwer.core.process.reconstruction.saaxis.saaxis import (
    DEFAULT_RECONS_FOLDER as MULTI_COR_DEFAULT_FOLDER,
)
from tomwer.core.process.reconstruction.sadeltabeta.sadeltabeta import (
    DEFAULT_RECONS_FOLDER as MULTI_DB_DEFAULT_FOLDER,
)

logger = logging.getLogger(__name__)

try:
    from tomwer.synctools.rsyncmanager import RSyncManager
except ImportError:
    logger.warning("rsyncmanager not available")
    has_rsync = False
else:
    has_rsync = True


class ScanTransferTask(
    Task,
    input_names=("data",),
    optional_input_names=(
        "serialize_output_data",
        "copying",
        "block",
        "turn_off_print",
        "dest_dir",
        "move",
        "noRsync",
        "overwrite",
    ),
    output_names=("data",),
):
    """Manage the copy of scan.

    .. warning : the destination directory is find out from the file system
                 if /lbsramxxx exists for example...
                 In the case we couldn't found the output directory then we
                 will ask for the user to set it.
    """

    scanready = Signal(TomwerScanBase)
    """emit when scan ready"""

    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        super().__init__(
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
        self.turn_off_print = inputs.get("turn_off_print", False)
        self._destDir = inputs.get("dest_dir", None)
        """
        output directory if forced. By default based by the env variable
        'TARGET_OUTPUT_FOLDER' if exists, else set to '/data/visitor'
         """
        self._copying = inputs.get("copying", False)
        force_sync = inputs.get("force_sync", None)
        if force_sync is not None:
            from tomwer.core.utils.deprecation import deprecated_warning

            deprecated_warning(
                type_="Parameter",
                name="force_sync",
                reason="Two parameters for the same option",
                replacement="block",
            )
        else:
            force_sync = False

        self._block = self.get_input_value("block", force_sync)

        self._move = self.get_input_value("move", False)
        if not isinstance(self._move, bool):
            raise TypeError("move is expected to be a boolean")

        self._overwrite = self.get_input_value("overwrite", False)
        if not isinstance(self._overwrite, bool):
            raise TypeError("move is expected to be a boolean")

        self._noRsync = self.get_input_value(
            "noRsync", False
        )  # TODO: rename noRsync to no_rsync
        if not isinstance(self._noRsync, bool):
            raise TypeError("move is expected to be a boolean")

    def set_configuration(self, properties):
        # No properties stored for now
        if "dest_dir" in properties:
            self.setDestDir(properties["dest_dir"])

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "data transfer"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        return "transfer data from a folder to another"

    @staticmethod
    def getDefaultOutputDir():
        """Return the default output dir based on the computer setup"""
        if "TARGET_OUTPUT_FOLDER" in os.environ:
            return os.environ["TARGET_OUTPUT_FOLDER"]

        if os.path.isdir("/data/visitor"):
            return "/data/visitor"

        return ""

    def _process_edf_scan(self, scan, move=False, overwrite=True, noRsync=False):
        if not isinstance(scan, EDFTomoScan):
            raise TypeError(f"{scan} is expected to be an instance of {EDFTomoScan}")
        outputdir = self.getDestinationDir(scan.path)
        if outputdir is None:
            return

        self._pretransfertOperations(scan.path, outputdir)
        # as we are in the workflow we want this function to be bloking.
        # so we will not used a thread for folder synchronization
        # for now rsync is not delaing with overwrite option
        if not has_rsync or noRsync is True or RSyncManager().has_rsync() is False:
            logger.info("Can't use rsync, copying files")
            try:
                if move is True:
                    self._moveFiles(
                        scanPath=scan.path,
                        outputdir=os.path.dirname(outputdir),
                        overwrite=overwrite,
                    )
                else:
                    self._copyFiles(
                        scanPath=scan.path, outputdir=outputdir, overwrite=overwrite
                    )
            except shutil.Error as e:
                raise e
            else:
                output_scan = scan._deduce_transfert_scan(outputdir)
                try:
                    output_scan._update_latest_recons_identifiers(
                        old_path=scan.path, new_path=output_scan.path
                    )
                except Exception as e:
                    logger.warning(
                        "Fail to convert url of latest reconstruction. Reason is:" + e
                    )
                    output_scan.clear_latest_reconstructions()
                self.__noticeTransfertSuccess(input_scan=scan, output_scan=output_scan)
        else:
            source = scan.path
            if not source.endswith(os.path.sep):
                source = source + os.path.sep
            target = outputdir

            if not target.endswith(os.path.sep):
                target = target + os.path.sep

            self._signalCopying(scanID=source, outputdir=target)
            output_scan = scan._deduce_transfert_scan(outputdir)
            try:
                output_scan._update_latest_recons_identifiers(
                    old_path=scan.path, new_path=output_scan.path
                )
            except Exception as e:
                logger.warning(
                    "Fail to convert url of latest reconstruction. Reason is:" + e
                )
                output_scan.clear_latest_reconstructions()
            RSyncManager().sync_file(
                source=source,
                target=target,
                wait=self._block,
                delete=True,
                callback=self.__noticeTransfertSuccess,
                callback_parameters=(scan, output_scan),
                rights=777,
            )
        return output_scan

    def _get_hdf5_dst_scan(self, bliss_scan_folder_path):
        if self._destDir is not None:
            rel_path = os.path.join(*bliss_scan_folder_path.split(os.sep)[-2:])
            return os.path.dirname(os.path.join(self._destDir, rel_path))
        # try to get outputdir from spec
        scanIDPath = os.path.abspath(bliss_scan_folder_path)
        return self._getOutputDirSpec() or os.path.join(
            *self._getOutputDirLBS(scanIDPath).split(os.sep)[:-1]
        )

    def _get_hdf5_sample_file_or_nx_dst(self, bliss_sample_file):
        bliss_sample_file = os.path.abspath(bliss_sample_file)
        if self._destDir is not None:
            rel_path = os.path.join(*bliss_sample_file.split(os.sep)[-2:])
            return os.path.join(self._destDir, rel_path)
        # try to get outputdir from spec
        bliss_sample_file = os.path.abspath(bliss_sample_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(bliss_sample_file)

    def _get_master_sample_file_dst(self, master_sample_file):
        if self._destDir is not None:
            rel_path = os.path.join(*master_sample_file.split(os.sep)[-2:])
            return os.path.join(self._destDir, rel_path)
        # try to get outputdir from spec
        master_sample_file = os.path.abspath(master_sample_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(master_sample_file)

    def _get_hdf5_proposal_file_dst(self, bliss_proposal_file):
        if self._destDir is not None:
            return os.path.join(self._destDir, os.path.split(bliss_proposal_file)[-1])
        # try to get outputdir from spec
        bliss_sample_file = os.path.abspath(bliss_proposal_file)
        return self._getOutputDirSpec() or self._getOutputDirLBS(bliss_sample_file)

    def _process_hdf5_scan(self, scan) -> TomwerScanBase:
        assert isinstance(scan, NXtomoScan)
        logger.warning(
            "scan transfer for HDF5 is a prototype. Please check transfer is properly executed."
        )

        files_sources = []
        files_dest = []
        delete_opt = []

        associated_files = get_unique_files_linked(url=scan.get_detector_url())
        associated_files = filter(
            lambda file_: os.path.abspath(file_) == os.path.abspath(scan.master_file),
            associated_files,
        )

        # manage .nx file
        if os.path.exists(scan.master_file):
            (
                new_nx_file,
                files_sources_for_nx,
                files_dest_for_nx,
            ) = self.handle_nexus_file(scan.master_file, scan.entry)
            files_sources.extend(files_sources_for_nx)
            files_dest.extend(files_dest_for_nx)
            delete_opt.append([True] * len(files_dest_for_nx))
            files_sources.append(scan.master_file)
            files_dest.append(new_nx_file)
            delete_opt.append(True)
            output_scan = NXtomoScan(scan=new_nx_file, entry=scan.entry)
        else:
            output_scan = None

        # manage files generated (*slice*.h5/edf, *.cfg, *.par...)
        # for reconstructed file, .h5, .edf if there is some conflict at one
        # point I guess we might need to check file entry ? or rename the file
        # according to the entry.

        # manage .par, .cfg and .rec files if any
        patterns = ["*.par", "*.cfg", "*.rec", "*.log"]
        # manage *slice*.hdf5 and *slice*.edf files (reconstructed slice)
        patterns += [
            "*slice*.hdf5",
            "*slice*.h5",
            "*slice*.jpeg",
            "*slice*.jpg",
            "*slice*.tiff",
            "*slice*.tif",
            "*slice*.j2k",
        ]
        # manage *vol files
        patterns += [
            "*_vol",
            "*_vol.hdf5",
        ]
        # manage nabu and tomwer processes files
        patterns += [
            "*tomwer_processes.h5",
            "*nabu_processes.hdf5",
            "steps_file_basename_nabu_sinogram_save_step.hdf5",
        ]
        # manage new dark and flat files
        patterns += [
            "*dark.hdf5",
            "*darks.hdf5",
            "*flats.hdf5",
        ]

        def match_pattern(file_name):
            file_name = file_name.lower()
            for pattern in patterns:
                if fnmatch.fnmatch(file_name, pattern):
                    return True
            return False

        dir_name = os.path.dirname(scan.master_file)
        for file_ in os.listdir(dir_name):
            if match_pattern(file_name=file_):
                full_file_path = os.path.join(dir_name, file_)
                files_sources.append(full_file_path)
                files_dest.append(self._get_hdf5_sample_file_or_nx_dst(full_file_path))
                delete_opt.append(True)

        # manage folders
        patterns = [
            NABU_CFG_FILE_FOLDER,
            "*slice*",
            MULTI_COR_DEFAULT_FOLDER,
            MULTI_DB_DEFAULT_FOLDER,
            "steps_file_basename_nabu_sinogram_save_step",
        ]
        for folder_ in os.listdir(dir_name):
            if match_pattern(file_name=folder_):
                full_file_path = os.path.join(dir_name, folder_)
                files_sources.append(full_file_path)
                # don't know why we need this os.sep ? call another get dest ?
                # os.path.join(os.sep, self._get_hdf5_dst_scan(full_file_path), folder_)
                dest = os.path.join(os.sep, self._get_hdf5_dst_scan(full_file_path))
                files_dest.append(dest)
                delete_opt.append(True)

        RSyncManager().sync_files(
            sources=files_sources,
            targets=files_dest,
            wait=self._block,
            delete=delete_opt,
            callback=self.__noticeTransfertSuccess,
            callback_parameters=(scan, output_scan),
        )
        return output_scan

    def handle_nexus_file(self, src_nexus_file: str, entry: str) -> tuple:
        """
        Return a tuple of three elemts:
        src_nexus_file, files_sources_for_nx, files_dest_for_nx

        :param src_nexus_file: source file to treat
        :return: (dst_nexus_file, files_sources_for_nx, files_dest_for_nx)
                * dst_nexus_file: str -> output nexus file that will be created by the transfer
                * list files_sources_for_nx: list of relative files connected to source nexus file
                * files_dest_for_nx: list of creating files from files_sources_for_nx once transfer is accomplish
        """
        dst_nx_file = self._get_hdf5_sample_file_or_nx_dst(src_nexus_file)
        linked_datasets_src = get_linked_files_with_entry(
            hdf5_file=src_nexus_file, entry=entry
        )
        linked_files_src = list(map(lambda x: x[0], linked_datasets_src))
        relative_linked_files_src = list(
            filter(lambda file_path: not os.path.isabs(file_path), linked_files_src)
        )
        relative_linked_files_dst = [
            os.path.normpath(os.path.join(os.path.dirname(dst_nx_file), file_path))
            for file_path in relative_linked_files_src
        ]
        relative_linked_files_src = [
            os.path.normpath(os.path.join(os.path.dirname(src_nexus_file), file_path))
            for file_path in relative_linked_files_src
        ]
        return dst_nx_file, relative_linked_files_src, relative_linked_files_dst

    def run(self):
        """Launch the process process

        :param scan: the path to the file we want to move/process
        :param move: if True, directly move the files. Otherwise copy the files
        :param overwrite: if True then force the copy even if the file/folder already
            exists
        :param noRSync: True if we wan't do sue shutil instead of rsync.
        """
        scan = data_identifier_to_scan(self.inputs.data)
        if scan is None:
            raise ValueError("'scan' should be provided")

        if scan is None:
            self.outputs.data = None

        _scan = scan
        if type(_scan) is dict:
            _scan = ScanFactory.create_scan_object_frm_dict(scan)

        assert isinstance(_scan, TomwerScanBase)

        logger.info("synchronisation with scanPath")
        if isinstance(scan, EDFTomoScan):
            output_scan = self._process_edf_scan(
                scan=scan,
                move=self._move,
                overwrite=self.get_input_value("overwrite", True),
                noRsync=self._noRsync,
            )
        elif isinstance(scan, NXtomoScan):
            if self._move is True:
                raise NotImplementedError("move option not implemented")
            if self._noRsync is True:
                raise NotImplementedError("noRsync option not implemented")
            output_scan = self._process_hdf5_scan(scan=scan)
        else:
            raise TypeError("Other scan than EDF or HDF5 are not managed")
        if self.get_input_value("serialize_output_data", True):
            self.outputs.data = output_scan.to_dict()
        else:
            self.outputs.data = output_scan

    def _pretransfertOperations(self, scanfolder, outputdir):
        """Operation to be run before making the transfert of the scan"""
        self._updateParFiles(scanfolder, outputdir)
        self._updateNabuConfigFiles(scanfolder, outputdir)

    def _updateNabuConfigFiles(self, scanfolder, outputdir):
        nabu_cfg_folder = os.path.join(scanfolder, NABU_CFG_FILE_FOLDER)
        if os.path.exists(nabu_cfg_folder):
            for _file in os.listdir(nabu_cfg_folder):
                try:
                    update_cfg_file_after_transfer(
                        config_file_path=os.path.join(nabu_cfg_folder, _file),
                        old_path=scanfolder,
                        new_path=outputdir,
                    )
                except Exception:
                    pass

    def _updateParFiles(self, scanfolder, outputdir):
        """Update all path contained in the .par files to fit the new outpudir"""
        if not os.path.exists(scanfolder):
            return
        for _file in os.listdir(scanfolder):
            if _file.lower().endswith(".par"):
                rebaseParFile(
                    os.path.join(scanfolder, _file),
                    oldfolder=scanfolder,
                    newfolder=outputdir,
                )

    def __noticeTransfertSuccess(self, input_scan, output_scan):
        self._signalCopySucceed()

        logger.processSucceed(
            f"transfer succeed of {input_scan} to {output_scan}",
            extra={
                logconfig.DOC_TITLE: self._scheme_title,
                logconfig.FROM: str(input_scan),
                logconfig.TO: str(output_scan),
            },
        )
        self.signalTransfertOk(input_scan=input_scan, output_scan=output_scan)

    def signalTransfertOk(self, input_scan, output_scan):
        if input_scan is None or output_scan is None:
            return
        assert isinstance(input_scan, TomwerScanBase)
        assert isinstance(output_scan, TomwerScanBase)
        self.scanready.emit(output_scan)

    def _copyFiles(self, scanPath, outputdir, overwrite):
        """Copying files and removing them"""
        assert type(scanPath) is str
        assert type(outputdir) is str
        assert os.path.isdir(scanPath)
        # create the destination dir
        if not os.path.isdir(outputdir):

            def createDirAndTopDir(_dir):
                if not os.path.isdir(os.path.dirname(_dir)):
                    createDirAndTopDir(os.path.dirname(_dir))
                os.makedirs(_dir)

            createDirAndTopDir(outputdir)
        # we can't copy directly the top folder because he is already existing
        for f in os.listdir(scanPath):
            file = os.path.join(scanPath, f)
            fileDest = os.path.join(outputdir, f)
            if overwrite is True:
                if os.path.isdir(fileDest):
                    shutil.rmtree(fileDest)
                if os.path.isfile(fileDest):
                    os.remove(fileDest)
            if os.path.exists(fileDest):
                raise FileExistsError(fileDest, "already exists")
            if os.path.isdir(file):
                shutil.copytree(src=file, dst=fileDest)
            else:
                shutil.copy2(src=file, dst=fileDest)

        info = "Removing directory at %s" % scanPath
        logger.info(info)
        shutil.rmtree(scanPath)
        info = "sucessfuly removed file at %s !!!" % scanPath
        logger.info(info)

    def _moveFiles(self, scanPath, outputdir, overwrite):
        """Function simply moving files"""
        assert os.path.isdir(scanPath)

        logger.debug(
            "synchronisation with scanPath",
            extra={logconfig.DOC_TITLE: self._scheme_title},
        )

        target = os.path.join(outputdir, os.path.basename(scanPath))
        if overwrite is True and os.path.isdir(target):
            shutil.rmtree(target)
        shutil.move(scanPath, outputdir)

    def _requestFolder(self):
        out = None
        while out is None:
            out = input("please give the output directory : \n")
            if not os.path.isdir(out):
                warning = "given path " + out
                warning += " is not a directory, please give a valid directory"
                logger.warning(warning)
                out = None
        return out

    def _getOutputDirSpec(self):
        return None

    def _getOutputDirLBS(self, scanPath):
        if scanPath.startswith(get_lbsram_path()):
            return scanPath.replace(get_lbsram_path(), get_dest_path(), 1)
        else:
            return None

    def getDestinationDir(self, scanPath, ask_for_output=True):
        """Return the destination directory. The destination directory is the
        root directory"""
        if self._destDir is not None:
            return os.path.join(self._destDir, os.path.basename(scanPath))

        # try to get outputdir from spec
        scanIDPath = os.path.abspath(scanPath)

        outputdir = self._getOutputDirSpec() or self._getOutputDirLBS(scanIDPath)
        if outputdir is None and ask_for_output:
            outputdir = self._requestFolder()

        return outputdir

    def setDestDir(self, dist):
        """Force the outpudir to dist.

        :param dist: path to the folder. If None remove overwrite behavior
        """
        self._destDir = dist
        if self._destDir is not None and os.path.isdir(self._destDir):
            logger.warning("Given path %s is not a directory" % self._destDir)

    # some function to print the output in the terminal #

    def _signalCopying(self, scanID, outputdir):
        self._copying = True
        if self.turn_off_print is False:
            print("######################################")
            print("###")
            print("###")
            print("### copying files ", scanID, " to ", outputdir)
            print("### ...")

        info = f"start moving folder from {scanID} to {outputdir}"
        logger.processStarted(info, extra={logconfig.DOC_TITLE: self._scheme_title})

    def _signalCopyFailed(self):
        self._copying = False
        if self.turn_off_print is False:
            print("###")
            print("### copy failed")
            print("###")
            print("######################################")

    def _signalCopySucceed(self):
        self._copying = False
        if self.turn_off_print is False:
            print("###")
            print("### copy succeeded")
            print("###")
            print("######################################")

    def isCopying(self):
        """

        :return: True if the folder transfert is actually doing a copy
        """
        return self._copying

    def setForceSync(self, b):
        """

        :param b: if True then folderTransfert will wait until transfert
            is done to be released. Otherwise will launch a 'free' thread wich
            will notice transfert end later.
        """
        self._block = b

    def getOutput(self, scan):
        """

        :param scan:
        :return:
        """
        return os.path.join(self.getDestinationDir(scan), os.path.basename(scan))


class ScanTransfer(ScanTransferTask):
    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        deprecated_warning(
            name="tomwer.core.process.control.scantransfer.ScanTransfer",
            type_="class",
            reason="improve readibility",
            since_version="1.2",
            replacement="ScanTransferTask",
        )
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)

# coding: utf-8
"""
Utils to mock scans
"""

from __future__ import annotations

import glob
import os
import shutil

from silx.io.url import DataUrl
from enum import Enum as _Enum

from tomwer.core.scan.edfscan import EDFTomoScan
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.synctools.rsyncmanager import RSyncManager


class ScanStages:
    """
    Util class to copy all the files of scan to a destination dir until
    a define advancement of the acquisition.

    :param scan: scan to copy.
    """

    class AcquisitionStage(_Enum):
        ACQUI_NOT_STARTED = (0,)
        ACQUI_STARTED = (1,)
        ACQUI_ON_GOING = (2,)
        ACQUI_ENDED = (3,)
        RECONSTRUCTION_ADDED = (4,)
        COMPLETE = (99,)

        def get_command_name(self):
            """Return the name of the AcquisitionStage to give by a command
            option"""
            return self.name.lower().replace("_", "-")

        @staticmethod
        def get_command_names():
            return [stage.get_command_name() for stage in ScanStages.AcquisitionStage]

        @staticmethod
        def from_command_name(name):
            """Return the AcquisitionStage fitting a command option"""
            name_ = name.replace("-", "_").upper()
            return getattr(ScanStages.AcquisitionStage, name_)

    def __init__(self, scan: TomwerScanBase):
        assert isinstance(scan, TomwerScanBase)
        self.scan = scan

    def rsync_until(self, stage: AcquisitionStage, dest_dir: str) -> None:
        """

        :param stage:
        :param dest_dir:
        """
        stage = ScanStages.AcquisitionStage(stage)
        if not dest_dir.endswith(os.path.basename(self.scan.path)):
            dest_dir = os.path.join(dest_dir, os.path.basename(self.scan.path))
        for t_stage in ScanStages.AcquisitionStage:
            if t_stage.value <= stage.value:
                self._rsync_stage(t_stage, dest_dir=dest_dir)

    def _rsync_stage(self, stage: AcquisitionStage, dest_dir: str) -> None:
        """
        Synchronize a specific stage of scan to the given destination directory

        :param stage: stage to copy
        :param dest_dir:
        """
        if not dest_dir.endswith(os.path.basename(self.scan.path)):
            dest_dir = os.path.join(dest_dir, os.path.basename(self.scan.path))
        stage = ScanStages.AcquisitionStage(stage)
        if stage is ScanStages.AcquisitionStage.ACQUI_NOT_STARTED:
            return
        elif stage is ScanStages.AcquisitionStage.ACQUI_STARTED:
            if isinstance(self.scan, EDFTomoScan):
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                info_file = self.scan.get_info_file(self.scan.path)
                if info_file is not None:
                    file_info_dest = os.path.join(dest_dir, os.path.basename(info_file))
                    RSyncManager().sync_file(
                        source=info_file, target=file_info_dest, wait=True
                    )
            elif isinstance(self.scan, NXtomoScan):
                raise NotImplementedError()
        elif stage is ScanStages.AcquisitionStage.ACQUI_ON_GOING:
            # copy half of the acquisition file
            if isinstance(self.scan, EDFTomoScan):
                urls = self.scan.projections
                n_url = len(urls) // 2
                keys = list(urls.keys())
                while n_url > 0:
                    n_url -= 1
                    self._copy_url_file(url=urls[keys[n_url]], dest_dir=dest_dir)

            elif isinstance(self.scan, NXtomoScan):
                raise NotImplementedError()
        elif stage is ScanStages.AcquisitionStage.ACQUI_ENDED:
            if isinstance(self.scan, EDFTomoScan):
                for _, url in self.scan.projections.items():
                    file_target = url.file_path().replace(self.scan.path, dest_dir)
                    if not os.path.exists(file_target):
                        self._copy_url_file(url=url, dest_dir=dest_dir)
                xml_file = os.path.join(
                    self.scan.path, os.path.basename(self.scan.path) + ".xml"
                )
                xml_dest = os.path.join(dest_dir, os.path.basename(xml_file))
                RSyncManager().sync_file(source=xml_file, target=xml_dest, wait=True)
            elif isinstance(self.scan, NXtomoScan):
                raise NotImplementedError()
        elif stage is ScanStages.AcquisitionStage.RECONSTRUCTION_ADDED:
            # copy reconstruction
            if isinstance(self.scan, EDFTomoScan):
                pyhst_files = EDFTomoScan.get_pyhst_recons_file(scanID=self.scan.path)
                if pyhst_files:
                    for par_file in pyhst_files:
                        par_file_dst = os.path.join(
                            dest_dir, os.path.basename(par_file)
                        )
                        RSyncManager().sync_file(
                            source=par_file, target=par_file_dst, wait=True
                        )
                for reconstructed_file in EDFTomoScan.get_reconstructions_paths(
                    scanID=self.scan.path
                ):
                    assert os.path.isfile(reconstructed_file)
                    recons_file_dest = os.path.join(
                        dest_dir, os.path.basename(reconstructed_file)
                    )
                    RSyncManager().sync_file(
                        source=reconstructed_file, target=recons_file_dest, wait=True
                    )

                for par_file in glob.glob(os.path.join(self.scan.path, "*.par")):
                    par_file_src = os.path.join(self.scan.path, par_file)
                    par_file_dst = os.path.join(dest_dir, os.path.basename(par_file))
                    RSyncManager().sync_file(
                        source=par_file_src, target=par_file_dst, wait=True
                    )
                # copy some info file that can came from .vol files
                for info_file in glob.glob(os.path.join(self.scan.path, "*.info")):
                    info_file_src = os.path.join(self.scan.path, info_file)
                    info_file_dst = os.path.join(dest_dir, os.path.basename(info_file))
                    RSyncManager().sync_file(
                        source=info_file_src, target=info_file_dst, wait=True
                    )
                # copy some xml file that can came from pyhst
                xml_files = glob.glob(os.path.join(self.scan.path, "*.xml"))
                for xml_file in xml_files:
                    _xml_file = os.path.join(self.scan.path, xml_file)
                    xml_dest = os.path.join(dest_dir, os.path.basename(_xml_file))
                    RSyncManager().sync_file(
                        source=_xml_file, target=xml_dest, wait=True
                    )
            elif isinstance(self.scan, NXtomoScan):
                raise NotImplementedError()
        elif stage is ScanStages.AcquisitionStage.COMPLETE:
            if isinstance(self.scan, EDFTomoScan):
                for file_ in os.listdir(self.scan.path):
                    file_fp = os.path.join(self.scan.path, file_)
                    RSyncManager().sync_file(source=file_fp, target=dest_dir, wait=True)
            elif isinstance(self.scan, NXtomoScan):
                raise NotImplementedError()
        else:
            raise ValueError("given stage is not recognized", stage)

    def _copy_url_file(self, url, dest_dir):
        assert isinstance(url, DataUrl)
        file_target = url.file_path().replace(self.scan.path, dest_dir)
        if not os.path.exists(file_target):
            shutil.copyfile(src=url.file_path(), dst=file_target)

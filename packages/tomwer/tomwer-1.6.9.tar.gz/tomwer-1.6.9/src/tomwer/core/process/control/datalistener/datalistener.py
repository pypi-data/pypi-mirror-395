# coding: utf-8
from __future__ import annotations


import logging
import os
import socket
import time

from ewokscore.task import Task as EwoksTask
from nxtomomill import converter as nxtomomill_converter
from nxtomomill.models.h52nx import H52nxModel
from silx.io.utils import open as open_hdf5

import tomwer.version
from tomwer.core import settings
from tomwer.core.process.task import BaseProcessInfo
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.nxtomoscan import NXtomoScan

from .rpcserver import DataListenerThread


_logger = logging.getLogger(__name__)


def nxtomomill_input_callback(entry, desc):
    """note: for the data listener we want to avoid any user interaction.
    In order to avoid any time lost"""
    if entry == "energy":
        default_energy = 19.0
        _logger.warning(f"Energy is missing. Set it to default to {default_energy}")
        return default_energy
    else:
        _logger.warning(f"missing {entry}. Won't be set")
        return None


class _DataListenerTaskPlaceHolder(EwoksTask, output_names=["data"]):
    pass


class DataListener(BaseProcessInfo):
    # TODO: update this, DataListener is not properly a task
    """
    class able to connect with a redis database.
    During an acquisition at esrf the redis database expose the scan under
    acquisition. This allow use to know when a scan is finished.

    In order to insure connection the machine need to know where is located
    the 'bacon server'
    (see https://bliss.gitlab-pages.esrf.fr/bliss/master/bliss_data_life.html).
    This is why the 'BEACON_HOST' environment variable should be defined.

    For example for id19 - lbs 191 we have:
    export BEACON_HOST="europa"
    On id19 - europa we would have
    export BEACON_HOST="localhost"
    """

    TIMOUT_READ_FILE = 30
    "When the event 'scan_ended' is received all data might not have been write" " yet"

    SWMR_MODE = None
    """The bliss writer is not using the swmr mode. This class has independent behavior regarding the tomoscan / nxotmo get_swmr_mode which is
    dedicated to the internal tomotools behavior
    """

    def __init__(self):
        super().__init__()
        self._rpc_host = settings.JSON_RPC_HOST
        # if host is None then use hostname
        if self._rpc_host is None:
            self._rpc_host = socket.gethostname()
        self._rpc_port = settings.JSON_RPC_PORT
        self._listening_thread = None

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        return "scan listener"

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        return tomwer.version.version

    @staticmethod
    def definition():
        """definition of the process"""
        "convert bliss sequence with a proposal to a NXTomo nexus file"

    @property
    def port(self):
        return self._rpc_port

    @property
    def host(self):
        return self._rpc_host

    def get_listening_thread(self):
        """
        return the listening thread to ear at tango server
        """
        if self._listening_thread is None:
            self._listening_thread = self.create_listening_thread()
        return self._listening_thread

    def create_listening_thread(self):
        """
        Procedure to create the listening thread
        :return: listening thread
        """
        return DataListenerThread(host=self.host, port=self.port)

    def delete_listening_thread(self):
        """
        Procedure to delete the listening thread
        """
        if hasattr(self, "_listening_thread"):
            if self._listening_thread is not None:
                self._listening_thread.stop()
                self._listening_thread.join(5)
            del self._listening_thread
        self._listening_thread = None

    def set_configuration(self, properties):
        # for now the NXProcess cannot be tune
        if isinstance(properties, H52nxModel):
            self._settings = properties.to_dict()
        elif isinstance(properties, dict):
            self._settings = properties
        else:
            raise TypeError(f"invalid type: {type(properties)}")

    def run(self):
        pass

    def process_sample_file(
        self,
        sample_file: str,
        entry: str,
        proposal_file: str,
        master_sample_file: str | None,
    ) -> tuple:
        """

        :param sample_file: file to be converted
        :param entry: entry in the tango .h5 file to be converter
        :return: tuple scan succeeded.
        """
        if not os.path.isfile(sample_file):
            raise ValueError(f"Given file {sample_file} does not exists.")
        scans = []
        for mf_emf in self.convert(bliss_file=sample_file, entry=entry):
            master_file, entry_master_file = mf_emf
            if master_file is not None and entry_master_file is not None:
                scan = NXtomoScan(scan=master_file, entry=entry_master_file)
                self._signal_scan_ready(scan)
                scans.append(scan)
        return tuple(scans)

    def convert(self, bliss_file: str, entry: str) -> tuple:
        """

        :param bliss_file: file to be converted
        :param entry: entry in the tango .h5 file to be converter
        :return: tuple (output file, output file entry). Both are set to None
                 if conversion fails.
        """
        from tomwer.core.process.control.nxtomomill import (
            H5ToNxProcess as NxTomomillProcess,
        )

        conf = self.get_configuration()
        if conf is None:
            conf = {}
        configuration = H52nxModel.from_dict(conf)
        if configuration.output_file is None:
            output_file_path = NxTomomillProcess.deduce_output_file_path(
                bliss_file,
                output_dir=None,
                scan=BlissScan(
                    master_file=bliss_file, entry=entry, proposal_file=bliss_file
                ),
            )
        else:
            output_file_path = configuration.output_file

        if os.path.exists(output_file_path):
            if not self._ask_user_for_overwritting(output_file_path):
                return ((None, None),)

        if entry.startswith("/"):
            entries = (entry,)
        else:
            entries = ("/" + entry,)

        # work around: we need to wait a bit before converting the file
        # otherwise it looks like the file might not be ended to be
        # write
        def sequence_is_finished():
            try:
                with open_hdf5(bliss_file) as h5f:
                    end_scan_path = "/".join((entry, "end_time"))
                    return end_scan_path in h5f
            except Exception:
                return False

        timeout = self.TIMOUT_READ_FILE

        while timeout > 0 and not sequence_is_finished():
            timeout -= 0.2
            time.sleep(0.2)

        if timeout <= 0:
            _logger.error(f"unable to access {entry}@{bliss_file}. (Write never ended)")
            return ((None, None),)
        # one more delay to insure we can read it. Some frame might need more time to be dump from lima.
        time.sleep(4)

        # force some parameters
        configuration.input_file = bliss_file
        configuration.output_file = output_file_path
        configuration.entries = entries
        configuration.single_file = False
        configuration.overwrite = True
        configuration.request_input = True
        configuration.file_extension = ".nx"

        try:
            convs = nxtomomill_converter.from_h5_to_nx(
                configuration=configuration,
                input_callback=nxtomomill_input_callback,
                progress=None,
            )
        except Exception as e:
            _logger.error(
                f"Fail to convert from tango file: {bliss_file} to NXTomo. Error is: {e}"
            )
            return ((None, None),)
        else:
            return convs

    def _ask_user_for_overwritting(self, file_path):
        res = None
        while res not in ("Y", "n"):
            res = input(
                "The process will overwrite %s. Do you agree ? (Y/n)" "" % file_path
            )

        return res == "Y"

    def _signal_scan_ready(self, scan):
        assert isinstance(scan, NXtomoScan)
        pass

    def activate(self, is_using_rpc: bool, activate=True):
        """
        activate or deactivate the thread. When deactivate call join and
        delete the thread

        :param activate:
        """
        if activate:
            if self._listening_thread is not None:
                _logger.info("listening is already activate")
            else:
                assert isinstance(self, DataListener)
                if is_using_rpc and not self.is_port_available():
                    raise OSError(
                        f"Port {self._rpc_host}:{self._rpc_port} already used"
                    )
                if self.get_listening_thread() is not None:
                    self.get_listening_thread().start()
        else:
            if self._listening_thread is None:
                return
            else:
                self.delete_listening_thread()

    def is_active(self):
        if self._listening_thread is None:
            return False
        else:
            return True

    def is_port_available(self):
        """

        :return: True if the port is available else False
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return not s.connect_ex((self._rpc_host, self._rpc_port)) == 0

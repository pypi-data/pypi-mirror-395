from __future__ import annotations

import psutil
import logging
from psutil import process_iter
import getpass


_logger = logging.getLogger(__name__)


def send_signal_to_local_rpc_servers(signal, port: int, extended_find: bool = True):
    """
    :param signal: signal to be emit
    :param port: port to check
    :param extended_find: if True then will try to find a process that occupy the port
        even if this is not a process launched by the user and launched by tomwer.
    """

    found = False
    for proc in process_iter():
        # try to find a process we can handle
        if proc.username() == getpass.getuser():
            try:
                for conns in proc.connections():
                    # make sure we will kill the correct process
                    if conns.laddr.port == port and proc.name() in (
                        "tomwer",
                        "orange-canvas",
                    ):
                        _logger.warning(f"send {signal} signal to pid {proc.pid}")
                        proc.send_signal(signal)
                        found = True
                        return
            except (PermissionError, psutil.AccessDenied):
                pass
    if not extended_find:
        return
    # if process not found try to find one to inform the user
    if not found:
        for proc in process_iter():
            try:
                for conns in proc.connections():
                    # make sure we will kill the correct process
                    if conns.laddr.port == port:
                        _logger.warning(
                            f"process pid: {proc.pid} - {proc.name()} seems to be one occupying port {port}"
                        )
                        return
            except (PermissionError, psutil.AccessDenied):
                pass

from __future__ import annotations

import logging
import socket
from contextlib import contextmanager
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

from silx.gui import qt
from tomwer.core.settings import TOMO_BEAMLINES

_logger = logging.getLogger(__name__)


class _PingHosts(qt.QThread):
    def __init__(self, *args, hosts_to_ping: tuple[str], port: int, **kwargs):
        super().__init__(*args, **kwargs)
        self._hosts_to_ping = hosts_to_ping
        self._port = port
        self._accessibility: dict[str, bool] = {}

    @staticmethod
    def can_ping_host(host_name: str, port: int, timeout_s: float = 0.5) -> bool:
        """
        Checks if a host is reachable on a specific TCP port.
        Returns True if reachable, False otherwise.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout_s)
        try:
            sock.connect((host_name, port))
        except (socket.timeout, socket.error):
            return False
        else:
            return True
        finally:
            sock.close()

    def run(self):
        pool = ThreadPool(processes=min(cpu_count(), 4))
        result = pool.map(
            lambda host: self.can_ping_host(host_name=host, port=self._port),
            self._hosts_to_ping,
        )
        pool.close()
        pool.join()
        self._accessibility = {
            host: accessibility
            for host, accessibility in zip(self._hosts_to_ping, result)
        }

    def getHostsAccessibility(self) -> dict[str, bool]:
        return self._accessibility


class RightIconDelegate(qt.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Set the decorationPosition to Right
        option.decorationPosition = qt.QStyleOptionViewItem.Right
        # Call the base class's paint method to draw the item with the modified option
        super().paint(painter, option, index)


class HostEditor(qt.QComboBox):
    """
    An editable QCombobox that proposes some beamline in order to select an host.

    Use case: blissdata listener
    """

    def __init__(
        self,
        *args,
        hosts: tuple[str] = TOMO_BEAMLINES,
        name: str | None,
        port: int = 25000,
        enable_host_pinging: bool = True,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not isinstance(port, int):
            raise TypeError(f"port is expected to be an int. Got {type(port)}")
        self.__hosts = hosts
        self.__port = port
        self.__pingerThread = None
        # thread to check which host are accessible
        self.__enable_host_pinging = enable_host_pinging
        self.addItems(hosts)
        self.setPlaceholderText("id00 or 192.0.2.1")
        # let user use another name or an ip directly
        self.setEditable(True)
        self._updateIcons()

        # set up
        if name:
            self.setCurrentText(name)

        self.__delegate = RightIconDelegate()
        self.setItemDelegate(self.__delegate)

    def _getPingerThread(self):
        return self.__pingerThread

    def setCurrentText(self, *args, **kwargs):
        super().setCurrentText(*args, **kwargs)

    def setCurrentIndex(self, index):
        return super().setCurrentIndex(index)

    def setPort(self, port: int):
        """Defines the port to be used for checking host accessibility"""
        if port != self.__port:
            self.__port = port
            self._updateIcons()

    def __setAccessibleHost(self, host_accessibility: dict[str, bool]):
        """
        Set icons of the ComBox according to the host accessibility.
        Red: cannot reach it, green can.
        """
        with _keepCurrentText(self):
            # for some reason the current text is modified by this section...
            style = qt.QApplication.style()
            accessible_icon = style.standardIcon(qt.QStyle.SP_DialogYesButton)
            not_accessible_icon = style.standardIcon(qt.QStyle.SP_DialogNoButton)
            for host_name, can_be_access in host_accessibility.items():
                idx = self.findText(host_name)
                if idx >= 0:
                    icon = accessible_icon if can_be_access else not_accessible_icon
                    self.setItemIcon(idx, icon)
                else:
                    _logger.error(f"Cannot find host name {host_name}.")
        self.__pingerThread = None

    def _updateIcons(self):
        if not self.__enable_host_pinging:
            return

        if self.__pingerThread is not None:
            _logger.warning("Updating icons is already on-going")
            return

        self.__pingerThread = _PingHosts(
            hosts_to_ping=self.__hosts, port=self.__port, parent=self
        )
        self.__pingerThread.finished.connect(
            lambda: self.__setAccessibleHost(
                self.__pingerThread.getHostsAccessibility()
            )
        )
        self.__pingerThread.start()

    def close(self):
        if self.__pingerThread is not None:
            self.__pingerThread.wait()
        return super().close()


@contextmanager
def _keepCurrentText(w: qt.QComboBox):
    old = w.currentText()
    try:
        yield
    finally:
        w.setCurrentText(old)

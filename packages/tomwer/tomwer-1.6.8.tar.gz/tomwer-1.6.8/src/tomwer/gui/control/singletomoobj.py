import logging
import os

from silx.gui import qt
from tomoscan.esrf.volume.utils import guess_volumes

from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.volume.edfvolume import EDFVolume, EDFVolumeIdentifier
from tomwer.core.volume.hdf5volume import HDF5Volume, HDF5VolumeIdentifier
from tomwer.core.volume.jp2kvolume import JP2KVolume, JP2KVolumeIdentifier
from tomwer.core.volume.rawvolume import RawVolume, RawVolumeIdentifier
from tomwer.core.volume.tiffvolume import (
    MultiTIFFVolume,
    MultiTiffVolumeIdentifier,
    TIFFVolume,
    TIFFVolumeIdentifier,
)
from tomwer.gui.dialog.QDataDialog import QDataDialog
from tomwer.gui.qlefilesystem import QLFileSystem

_logger = logging.getLogger(__name__)


class SingleTomoObj(qt.QWidget):
    sigTomoObjChanged = qt.Signal(str)
    """signal emit when the tomo object changed. Parameter is the identifier"""

    def __init__(self, parent=None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setLayout(qt.QHBoxLayout())

        self._tomoObjIdentifierLineQLE = _TomoObjQLE("", self)
        self._tomoObjIdentifierLineQLE.setPlaceholderText(
            "scheme:obj_type:path?queries"
        )
        self.layout().addWidget(self._tomoObjIdentifierLineQLE)

        self._selectScanPB = qt.QPushButton("select", self)
        self.layout().addWidget(self._selectScanPB)

        self.setToolTip(
            "Define a Tomo object. You can also copy / paster folder or files to use the automatic detection. Each time it changed if fit a valid scan then this scan will be triggered"
        )

        # signal / slot connect
        self._tomoObjIdentifierLineQLE.editingFinished.connect(self._scanChanged)
        self._selectScanPB.released.connect(self._selectObject)

    def getTomoObjIdentifier(self) -> str:
        return self._tomoObjIdentifierLineQLE.text()

    def _selectObject(self, *args, **kwargs):  # pragma: no cover
        dialog = QDataDialog(self, multiSelection=True)
        dialog.setNameFilters(
            [
                "HDF5 files (*.h5 *.hdf5 *.nx *.nxs *.nexus)",
                "Nexus files (*.nx *.nxs *.nexus)",
                "Any files (*)",
            ]
        )

        if not dialog.exec():
            dialog.close()
            return
        added_tomo_objs = []
        for path in dialog.selectedFiles():
            try:
                objs = self.guessTomoObj(path=path)
            except Exception as e:  # noqa E722
                _logger.error(f"Fail to create tomo object from {path}. Error is {e}")
            else:
                if objs is not None:
                    added_tomo_objs.extend(objs)
        if len(added_tomo_objs) > 0:
            self.setTomoObject(added_tomo_objs[0])

    def _scanChanged(self):
        obj_identifier = self.getTomoObjIdentifier()
        # if the identifier fullill a path then this is not an identifier but
        # we must find the tomo obj associated
        if os.path.exists(obj_identifier):
            path = obj_identifier
            try:
                objs = self.guessTomoObj(path=path)
            except Exception as e:  # noqa E722
                _logger.error(f"Fail to create tomo object from {path}. Error is {e}")
            else:
                if objs is not None and len(objs) > 0:
                    old = self._tomoObjIdentifierLineQLE.blockSignals(True)
                    self._tomoObjIdentifierLineQLE.setText(
                        objs[0].get_identifier().to_str()
                    )
                    self._tomoObjIdentifierLineQLE.blockSignals(old)

        self.sigTomoObjChanged.emit(self.getTomoObjIdentifier())

    def setTomoObject(self, scan):
        if isinstance(scan, TomwerObject):
            text = scan.get_identifier().to_str()
        else:
            text = scan
        self._tomoObjIdentifierLineQLE.setText(text)
        self.sigTomoObjChanged.emit(self.getTomoObjIdentifier())

    def guessTomoObj(self, path):
        path = os.path.abspath(path)

        try:
            scans = ScanFactory.create_scan_objects(path)
            if scans is None or len(scans) == 0:
                raise ValueError
        except:  # noqa E722
            try:
                volumes = guess_volumes(
                    path,
                    scheme_to_vol={
                        EDFVolumeIdentifier.scheme: EDFVolume,
                        HDF5VolumeIdentifier.scheme: HDF5Volume,
                        TIFFVolumeIdentifier.scheme: TIFFVolume,
                        MultiTiffVolumeIdentifier.scheme: MultiTIFFVolume,
                        JP2KVolumeIdentifier.scheme: JP2KVolume,
                        RawVolumeIdentifier.scheme: RawVolume,
                    },
                )
            except:  # noqa E722
                pass
                return None
            else:
                # filter potential 'nabu histogram'
                if volumes is not None:

                    def is_not_histogram(vol_identifier):
                        return not (
                            hasattr(vol_identifier, "data_path")
                            and vol_identifier.data_path.endswith("histogram")
                        )

                    volumes = tuple(filter(is_not_histogram, volumes))
                return volumes
        else:
            return scans


class _TomoObjQLE(QLFileSystem):
    """QLineEdit that try to get a Tomo object identifier once dropped"""

    def supportedDropActions(self):
        """Inherited method to redefine supported drop actions."""
        return qt.Qt.CopyAction | qt.Qt.MoveAction

    def dropEvent(self, a0) -> None:
        if hasattr(a0, "mimeData") and a0.mimeData().hasFormat("text/uri-list"):
            for url in a0.mimeData().urls():
                try:
                    new_objs = self.parent().guessTomoObj(url.path())
                except:  # noqa E722
                    pass
                else:
                    if new_objs is not None and len(new_objs) > 0:
                        self.setText(new_objs[0].get_identifier().to_str())
            a0.accept()
            self.editingFinished.emit()
        else:
            return super().dropEvent(a0)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.accept()
            event.setDropAction(qt.Qt.CopyAction)
        else:
            qt.QListWidget.dragEnterEvent(self, event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list"):
            event.setDropAction(qt.Qt.CopyAction)
            event.accept()
        else:
            qt.QListWidget.dragMoveEvent(self, event)

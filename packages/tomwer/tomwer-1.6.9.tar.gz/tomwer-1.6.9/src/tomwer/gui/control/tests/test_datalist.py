from tomwer.tests.conftest import qtapp  # noqa F401
import tempfile

import pytest
from silx.gui import qt

from tomwer.core.utils.scanutils import MockEDF
from tomwer.gui.control.datalist import GenericScanListDialog, VolumeList
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_DataListTest(
    qtapp,  # noqa F811
    tmp_path,
):
    widget = GenericScanListDialog(parent=None)
    widget._callbackRemoveAllFolders()
    widget.clear()
    folders = []
    for _ in range(5):
        folders.append(tempfile.mkdtemp())
        MockEDF.mockScan(scanID=folders[-1], nRadio=5, nRecons=5, nPagRecons=0, dim=10)

    for _folder in folders:
        widget.add(_folder)

    assert widget.n_scan() == len(folders)
    widget.remove(folders[0])
    assert widget.n_scan() == (len(folders) - 1)
    assert folders[0] not in widget.datalist._myitems
    widget.selectAll()
    widget._removeSelected()
    assert widget.n_scan() == 0

    widget.setAttribute(qt.Qt.WA_DeleteOnClose)
    widget.close()


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
def test_VolumeList(
    qtapp,  # noqa F811
    tmp_path,
):
    """Test VolumeList behave as expected"""

    VolumeList(parent=None)

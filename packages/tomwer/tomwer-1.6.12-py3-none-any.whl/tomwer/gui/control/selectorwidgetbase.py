import logging

from silx.gui import qt

from tomwer.gui.utils.qt_utils import block_signals
from tomwer.gui.control.actions import TomoObjDisplayModeToolButton
from tomwer.gui.control.tomoobjdisplaymode import DisplayMode

_logger = logging.getLogger(__name__)


class _SelectorWidget(qt.QMainWindow):
    """widget used to select a dataset on a list (a scan or a volume for now)"""

    sigSelectionChanged = qt.Signal(list)
    """Signal emitted when the selection changed. List elements are tomo object identifier as str"""

    sigUpdated = qt.Signal()
    """signal emitted when the scan list change"""

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        # widget
        self._mainWidget = qt.QWidget(self)
        self._mainWidget.setLayout(qt.QVBoxLayout())
        self.dataList = self._buildDataList()
        self.dataList.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self._mainWidget.layout().addWidget(self.dataList)
        self._mainWidget.layout().addWidget(self._getAddAndRmButtons())
        self._mainWidget.layout().addWidget(self._getSendButtons())
        self._mainWidget.setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.setCentralWidget(self._mainWidget)

        # toolbar
        toolbar = qt.QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)

        tomoObjDisplayAction = TomoObjDisplayModeToolButton(self)
        toolbar.addWidget(tomoObjDisplayAction)

        # set up
        self.setDisplayMode(DisplayMode.SHORT)

        # connect signal / slot
        # for drag / drop we need to have an indirect call to the sigUpdated
        self.dataList.listChanged.connect(self._updatedFromDragDrop)
        tomoObjDisplayAction.sigDisplayModeChanged.connect(self.setDisplayMode)

    def setDisplayMode(self, *args, **kwargs):
        self.dataList.setDisplayMode(*args, **kwargs)

    def _updatedFromDragDrop(self, *args, **kwargs):
        self.sigUpdated.emit()

    def add(self, scan):
        added_scans = self.dataList.add(scan)
        self.sigUpdated.emit()
        return added_scans

    def remove(self, scan):
        self.dataList.remove(scan)
        self.sigUpdated.emit()

    def n_data(self) -> int:
        return len(self.dataList.items)

    def _buildDataList(self):
        raise NotImplementedError("Base class")

    def _getAddAndRmButtons(self):
        lLayout = qt.QHBoxLayout()
        w = qt.QWidget(self)
        w.setLayout(lLayout)
        self._addButton = qt.QPushButton("Add")
        self._addButton.clicked.connect(self._callbackAddData)
        self._rmButton = qt.QPushButton("Remove")
        self._rmButton.clicked.connect(self._callbackRemoveSelectedDatasets)

        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        lLayout.addWidget(spacer)
        lLayout.addWidget(self._addButton)
        lLayout.addWidget(self._rmButton)

        return w

    def _getSendButtons(self):
        layout = qt.QHBoxLayout()
        widget = qt.QWidget(self)
        widget.setLayout(layout)

        # select all button
        self._selectAllButton = qt.QPushButton("Select all")
        self._selectAllButton.setToolTip("Select all scan. (shortcut: Ctrl + A)")
        self._selectAllButton.clicked.connect(self.selectAll)
        layout.addWidget(self._selectAllButton)

        # horizontal spacer
        h_spacer = qt.QWidget(self)
        h_spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(h_spacer)

        # send selected button
        self._sendButton = qt.QPushButton("Send selected")
        self._sendButton.clicked.connect(self._sendSelected)
        layout.addWidget(self._sendButton)

        return widget

    def selectAll(self):
        self.dataList.selectAll()

    def setMySelection(self, selection: tuple):
        self.dataList.setMySelection(selection)

    def _callbackAddData(self):
        raise NotImplementedError("Base class")

    def _sendSelected(self):
        sItem = self.dataList.selectedItems()
        if sItem and len(sItem) >= 1:
            selection = [
                _item.data(qt.Qt.UserRole).get_identifier().to_str() for _item in sItem
            ]
            self.sigSelectionChanged.emit(list(selection))
        else:
            _logger.warning("No active scan detected")

    def _sendAll(self):
        allItems = list(self.dataList._myitems.keys())
        if len(allItems) > 0:
            self.sigSelectionChanged.emit(allItems)

    def _callbackRemoveSelectedDatasets(self):
        """ """
        selected_items = self.dataList.selectedItems()
        tomwer_objs_to_remove = [
            item.data(qt.Qt.UserRole).get_identifier().to_str()
            for item in selected_items
        ]
        for tomwer_obj in tomwer_objs_to_remove:
            self.remove(tomwer_obj)
        self.sigUpdated.emit()

    def setActiveData(self, data):
        """
        set the given scan as the active one

        :param scan: the scan to set active
        """
        data_id = data
        self.dataList.setCurrentItem(self.dataList.items[data_id])

    def removeSelectedDatasets(self):
        sItem = self.dataList.selectedItems()
        selection = [
            _item.data(qt.Qt.UserRole).get_identifier().to_str() for _item in sItem
        ]

        with block_signals(self):
            # make sure sigUpdated is called only once.
            for identifier in selection:
                self.remove(identifier)
        self.sigUpdated.emit()

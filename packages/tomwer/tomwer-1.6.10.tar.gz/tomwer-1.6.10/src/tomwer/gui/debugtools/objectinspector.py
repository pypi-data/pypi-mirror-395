# coding: utf-8
from __future__ import annotations


import sys

from silx.gui import qt


class ObjectInspector(qt.QWidget):
    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())

        self.__model = qt.QStandardItemModel()

        self._treeInspectorView = qt.QTreeView(self)
        self._treeInspectorView.setModel(self.__model)
        self.layout().addWidget(self._treeInspectorView)

    def setObject(self, object):
        self.__model.clear()
        root_item = qt.QStandardItem(f"{str(object)}")
        size_item = qt.QStandardItem(f"{sys.getsizeof(object) * 10e-6} (M bytes)")
        self.__model.invisibleRootItem().appendRow((root_item, size_item))

        def add_sub_elmts(parent_item, python_obj):
            if hasattr(python_obj, "__dict__"):
                for i_elmt, elmt in enumerate(python_obj.__dict__):
                    if hasattr(object, elmt):
                        children_obj = getattr(object, elmt)
                        # TODO: check if is a property or is a function
                        item = qt.QStandardItem(f"{elmt}")
                        # TODO: add size
                        size_item = qt.QStandardItem(
                            f"{sys.getsizeof(children_obj) * 10e-6} (M bytes)"
                        )
                        parent_item.appendRow((item, size_item))

                        # TODO: add children
                        add_sub_elmts(parent_item=item, python_obj=children_obj)

        add_sub_elmts(parent_item=root_item, python_obj=object)

from silx.gui import qt

from tomwer.gui.edit.nxtomoeditor import NXtomoEditor as _NXtomoEditor


class NXtomoMetadataViewer(_NXtomoEditor):
    """
    class to display metadata of a NXtomo.
    inherit from the `NXtomoEditor` and make sure not edition is possible
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        for widget in self.getEditableWidgets():
            if isinstance(widget, (qt.QComboBox, qt.QCheckBox)):
                widget.setEnabled(False)
            else:
                widget.setReadOnly(True)

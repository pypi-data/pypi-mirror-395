from silx.gui import qt
from silx.gui import icons as silx_icons
from tomwer.gui import icons as tomwer_icons


class LoadConfigurationAction(qt.QAction):
    """Action to trigger load of a stitching configuration"""

    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        if text is not None:
            self.setText(text)
        self.setToolTip("load nabu-stitching configuration")
        load_icon = silx_icons.getQIcon("document-open")
        self.setIcon(load_icon)


class SaveConfigurationAction(qt.QAction):
    """Action to trigger save of a stitching configuration"""

    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        if text is not None:
            self.setText(text)
        self.setToolTip("save nabu-stitching configuration")
        save_icon = silx_icons.getQIcon("document-save")
        self.setIcon(save_icon)


class AddTomoObjectAction(qt.QAction):
    """Action to trigger add a volume to a stitching configuration"""

    def __init__(self, parent=None, text=None):
        super().__init__(parent)
        if text is not None:
            self.setText(text)
        self.setToolTip(
            "Add a NXtomo or a (nabu) reconstructed volume to the stitching"
        )
        add_icon = tomwer_icons.getQIcon("add")
        self.setIcon(add_icon)


class PreviewAction(qt.QAction):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip("Compute preview with current settings (shortcut: F5)")
        update_preview_icon = tomwer_icons.getQIcon("update_stitching_preview")
        self.setIcon(update_preview_icon)

from silx.gui import qt
from tomwer.gui import icons as tomwer_icons


class MinimalisticConfigurationAction(qt.QAction):
    """
    Action to display the 'minimalistic' options only
    """

    def __init__(self, parent):
        self.__icon = tomwer_icons.getQIcon("minimalistic_user")
        qt.QAction.__init__(self, self.__icon, "minimalistic options", parent)
        self.setIconVisibleInMenu(True)
        self.setCheckable(True)
        self.setToolTip(self.tooltip())

    def tooltip(self):
        return "configuration: minimalistic level limit the number of options"

    def icon(self):
        return self.__icon

    def text(self):
        return "Minimalistic configuration"


class BasicConfigurationAction(qt.QAction):
    """
    Action to display the 'basic' options only
    """

    def __init__(self, parent):
        self.__icon = tomwer_icons.getQIcon("basic_user")
        qt.QAction.__init__(self, self.__icon, "basic options", parent)
        self.setIconVisibleInMenu(True)
        self.setCheckable(True)
        self.setToolTip(self.tooltip())

    def tooltip(self):
        return "configuration: basic level limit the number of options"

    def icon(self):
        return self.__icon

    def text(self):
        return "Basic configuration"


class ExpertConfigurationAction(qt.QAction):
    """
    Action to display the 'advanced' / expert options
    """

    def __init__(self, parent):
        self.__icon = tomwer_icons.getQIcon("advanced_user")
        qt.QAction.__init__(self, self.__icon, "advanced options", parent)
        self.setIconVisibleInMenu(True)
        self.setCheckable(True)
        self.setToolTip(self.tooltip())

    def tooltip(self):
        return (
            "configuration: advanced level give user all the possible \n"
            "option to tune the reconstructions"
        )

    def icon(self):
        return self.__icon

    def text(self):
        return "Advanced configuration"


class FilterAction(qt.QAction):
    """
    Action to activate the filtering from the nabu stage
    """

    def __init__(self, parent):
        style = qt.QApplication.style()
        icon = style.standardIcon(qt.QStyle.SP_FileDialogContentsView)

        qt.QAction.__init__(self, icon, "filter configuration", parent)
        self.setToolTip(
            "If activated will only display the configuration"
            "for the active nabu step"
        )
        self.setCheckable(True)
        self.setShortcut(qt.QKeySequence(qt.Qt.Key_F))

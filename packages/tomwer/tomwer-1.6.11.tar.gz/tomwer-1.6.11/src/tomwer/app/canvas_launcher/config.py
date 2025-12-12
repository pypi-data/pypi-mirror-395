# coding: utf-8
from __future__ import annotations

from orangewidget.settings import set_widget_settings_dir_components
from orangewidget.workflow import config
from silx.gui import qt
import logging

import tomwer.version
from tomwer.gui import icons

try:
    from ewoksorange.pkg_meta import entry_points
except ImportError:
    # ewoksorange < 2.0
    from ewoksorange.pkg_meta import iter_entry_points as entry_points
from . import environ
from .splash import getIcon, splash_screen
from .widgetsscheme import WidgetsScheme

_logger = logging.getLogger(__name__)


def version():
    return tomwer.version.version


class TomwerConfig(config.Config):
    """
    Configuration defined for tomwer
    """

    OrganizationDomain = "esrf"
    ApplicationName = "tomwer"
    ApplicationVersion = version()

    def init(self):
        super().init()
        qt.QApplication.setApplicationName(self.ApplicationName)
        qt.QApplication.setOrganizationDomain(self.OrganizationDomain)
        qt.QApplication.setApplicationVersion(self.ApplicationVersion)
        qt.QApplication.setApplicationDisplayName(self.ApplicationName)
        widget_settings_dir_cfg = environ.get_path("widget_settings_dir", "")
        if widget_settings_dir_cfg:
            # widget_settings_dir is configured via config file
            set_widget_settings_dir_components(
                widget_settings_dir_cfg, self.ApplicationVersion
            )

        canvas_settings_dir_cfg = environ.get_path("canvas_settings_dir", "")
        if canvas_settings_dir_cfg:
            # canvas_settings_dir is configured via config file
            qt.QSettings.setPath(
                qt.QSettings.IniFormat, qt.QSettings.UserScope, canvas_settings_dir_cfg
            )

    @staticmethod
    def splash_screen():
        """"""
        return splash_screen()

    @staticmethod
    def core_packages():
        return super().core_packages() + ["tomwer-add-on"]

    @staticmethod
    def application_icon():
        return getIcon()

    @staticmethod
    def workflow_constructor(*args, **kwargs):
        return WidgetsScheme(*args, **kwargs)

    @staticmethod
    def widgets_entry_points():
        """
        Return an `EntryPoint` iterator for all 'orange.widget' entry
        points.
        """
        # Ensure the 'this' distribution's ep is the first. iter_entry_points
        # yields them in unspecified order.
        WIDGETS_ENTRY = "orange.widgets"

        def accept_extension(entry):
            # safer to ignore some extension like ewoks demo
            return entry.name.lower() not in ("ewoks demo",)

        try:
            all_eps = filter(accept_extension, entry_points(group=WIDGETS_ENTRY))
        except Exception as e:
            _logger.error(f"fail to find add-ons. Error is {e}")
        return iter(all_eps)

    @staticmethod
    def addon_entry_points():
        return TomwerConfig.widgets_entry_points()

    APPLICATION_URLS = {
        #: Submit a bug report action in the Help menu
        "Bug Report": "https://gitlab.esrf.fr/tomotools/tomwer/-/issues",
        #: A url quick tour/getting started url
        "Quick Start": "https://www.youtube.com/playlist?list=PLddRXwP6Z6F9KOu1V5o6H24KPH5Ikuk2f",
        #: The 'full' documentation, should be something like current /docs/
        #: but specific for 'Visual Programing' only
        "Documentation": "https://tomotools.gitlab-pages.esrf.fr/tomwer/index.html",
        #: YouTube tutorials
        "Screencasts": "https://www.youtube.com/@tomotools",
    }


class TomwerSplashScreen(qt.QSplashScreen):
    def __init__(
        self,
        parent=None,
        pixmap=None,
        textRect=None,
        textFormat=qt.Qt.PlainText,
        **kwargs,
    ):
        super(TomwerSplashScreen, self).__init__(pixmap=icons.getQPixmap("tomwer"))

    def showMessage(self, message, alignment=qt.Qt.AlignLeft, color=qt.Qt.black):
        version = f"tomwer version {tomwer.version.version}"
        super().showMessage(version, qt.Qt.AlignLeft | qt.Qt.AlignBottom, qt.Qt.white)

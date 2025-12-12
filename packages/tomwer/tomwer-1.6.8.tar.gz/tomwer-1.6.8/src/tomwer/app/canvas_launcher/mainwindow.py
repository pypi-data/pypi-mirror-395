from __future__ import annotations

import argparse
import logging
import os
import shutil
import signal
import sys
import pkg_resources

import silx
from contextlib import closing
from logging.handlers import RotatingFileHandler
from xml.sax.saxutils import escape

import pyqtgraph
from orangecanvas.application.canvasmain import DockWidget
from orangecanvas.application.outputview import (
    ExceptHook,
    TerminalTextDocument,
    TextStream,
)
from orangecanvas.document.usagestatistics import UsageStatistics
from orangecanvas.main import Main as ocMain
from orangewidget.workflow import config
from orangewidget.workflow.config import data_dir_base
from orangewidget.workflow.errorreporting import handle_exception
from orangewidget.workflow.mainwindow import OWCanvasMainWindow as _MainWindow
from processview.gui.processmanager import ProcessManagerWindow
from silx.gui import qt

import tomwer.version
from orangecanvas.preview import previewdialog, previewmodel
from orangecanvas.application import examples as orange_examples
import tomoscan.version

from .config import TomwerConfig, TomwerSplashScreen

from tomwer.core.log.processlog import (
    PROCESS_ENDED_NAME,
    PROCESS_FAILED_NAME,
    PROCESS_INFORM_NAME,
    PROCESS_SKIPPED_NAME,
    PROCESS_STARTED_NAME,
    PROCESS_SUCCEED_NAME,
)

try:
    import nabu
except ImportError:
    has_nabu = False
else:
    has_nabu = True
try:
    import nxtomomill.version
except ImportError:
    has_nxtomomill = False
else:
    has_nxtomomill = True
try:
    import nxtomo
except ImportError:
    has_nxotmo = False
else:
    has_nxotmo = True
try:
    import sluurp
except ImportError:
    has_sluurp = False
else:
    has_sluurp = True

_logger = logging.getLogger(__file__)

MAX_LOG_FILE = 10
"""Maximal log file kepts for orange"""

LOG_FILE_NAME = "tomwer.log"

LOG_FOLDER = "/var/log/tomwer"


# These are the sequences need to get colored ouput
_RESET_SEQ = "\033[0m"

_BLACK = "\033[30m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_BLUE = "\033[34m"
_MAGENTA = "\033[35m"


LOG_COLORS = {
    "WARNING": _MAGENTA,
    "INFO": _BLACK,
    "DEBUG": _BLUE,
    "CRITICAL": _YELLOW,
    "ERROR": _RED,
    PROCESS_SKIPPED_NAME: _MAGENTA,
    PROCESS_ENDED_NAME: _BLACK,
    PROCESS_INFORM_NAME: _BLACK,
    PROCESS_STARTED_NAME: _BLACK,
    PROCESS_FAILED_NAME: _RED,
    PROCESS_SUCCEED_NAME: _GREEN,
}


class MainWindow(_MainWindow):
    HELPDESK_URL = "https://requests.esrf.fr/plugins/servlet/desk/portal/41"

    FORCE_OBJECT_SUPERVISOR_DISPLAY = True
    """If true will always display the processed supervisor at start up. Restore state will be ignored."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_supervisor_dock = DockWidget(
            self.tr("object supervisor"),
            self,
            objectName="processes-dock",
            allowedAreas=qt.Qt.BottomDockWidgetArea,
            visible=self.show_processes_manager_action.isChecked(),
        )

        self.process_supervisor_dock.setWidget(ProcessManagerWindow(parent=None))
        self.process_supervisor_dock.visibilityChanged[bool].connect(
            self.show_processes_manager_action.setChecked
        )
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self.process_supervisor_dock)

    def restoreState(self, state, version=0):
        # for now we always want to display the process supervisor
        restored = super().restoreState(state=state, version=version)
        if self.FORCE_OBJECT_SUPERVISOR_DISPLAY:
            self.show_processes_manager_action.setChecked(True)
            self.process_supervisor_dock.setVisible(True)

        return restored

    def setup_actions(self):
        super().setup_actions()
        # create the action to connect with it
        self.show_processes_manager_action = qt.QAction(
            self.tr("&object supervisor"),
            self,
            toolTip=self.tr("Show object states relative to processes."),
            checkable=True,
            triggered=lambda checked: self.process_supervisor_dock.setVisible(checked),
        )

    def setup_menu(self):
        super().setup_menu()
        self.view_menu.addAction(self.show_processes_manager_action)

        self.simple_example_action = qt.QAction(
            self.tr("simple use cases"),
            self,
            objectName="simple-use-cases",
            toolTip=self.tr("Some simple examples."),
            triggered=self.open_simple_examples,
            menuRole=qt.QAction.AboutRole,
        )

        self.dark_flat_example_action = qt.QAction(
            self.tr("darks and flats manipulations"),
            self,
            objectName="dark-flat-manipulation",
            toolTip=self.tr("Examples around dark and flat."),
            triggered=self.open_dark_flat_examples,
            menuRole=qt.QAction.AboutRole,
        )
        self.slurm_execution_example_action = qt.QAction(
            self.tr("remote processing with slurm"),
            self,
            objectName="execution-on-slurm",
            toolTip=self.tr("Examples of some execution over slurm."),
            triggered=self.open_slurm_execution_example,
            menuRole=qt.QAction.AboutRole,
        )
        self.cor_search_example_action = qt.QAction(
            self.tr("cor search advance example"),
            self,
            objectName="cor-search-example",
            toolTip=self.tr("Examples of ways to search for the Center of rotation."),
            triggered=self.open_cor_search_example,
            menuRole=qt.QAction.AboutRole,
        )
        self.python_script_example_action = qt.QAction(
            self.tr("python script examples"),
            self,
            objectName="python-script-example",
            toolTip=self.tr("Examples of some python script usage."),
            triggered=self.open_python_script_example,
            menuRole=qt.QAction.AboutRole,
        )
        self.python_script_example_action = qt.QAction(
            self.tr("ID16b examples"),
            self,
            objectName="id16b-example",
            toolTip=self.tr("ID16b use case."),
            triggered=self.open_id16b_example,
            menuRole=qt.QAction.AboutRole,
        )
        # Predefined workflows menu.
        self.predefined_workflows_menu = qt.QMenu(
            self.tr("&Examples"),
            self.menuBar(),
            objectName="examples-menu",
        )
        self.predefined_workflows_menu.addActions(
            [
                self.simple_example_action,
                self.cor_search_example_action,
                self.dark_flat_example_action,
                self.slurm_execution_example_action,
                self.python_script_example_action,
            ]
        )

        self.menuBar().addMenu(self.predefined_workflows_menu)

        self._helpdeskButton = qt.QAction(
            self.tr("&Helpdesk"),
            self,
            objectName="helpdeskButton",
            triggered=self._contactUs,
            toolTip="contact esrf data processing helpdesk if you have some troubles with the application",
        )
        self.menuBar().addAction(self._helpdeskButton)

    def _contactUs(self, *args, **kwargs):
        try:
            qt.QDesktopServices.openUrl(qt.QUrl(self.HELPDESK_URL))
        except Exception as e:
            _logger.error(
                f"Failed to launch helpdesk web page ({self.HELPDESK_URL}). Error is {e}"
            )

    def __open_examples(self, examples, filter_names=None):
        """
        filter the existing tutorials by names contained in the file name
        """
        items = [previewmodel.PreviewItem(path=t.abspath()) for t in examples]

        def my_filter(value):
            for filter_name in filter_names:
                if filter_name in value:
                    return True
            return False

        if filter_names is not None:
            items = filter(
                lambda item: my_filter(os.path.basename(item.path())),
                items,
            )
        dialog = previewdialog.PreviewDialog(self)
        model = previewmodel.PreviewModel(dialog, items=items)
        title = self.tr("Example Workflows")
        dialog.setWindowTitle(title)
        template = '<h3 style="font-size: 26px">\n' "{0}\n" "</h3>"

        dialog.setHeading(template.format(title))
        dialog.setModel(model)

        model.delayedScanUpdate()
        status = dialog.exec()
        index = dialog.currentIndex()

        dialog.deleteLater()

        if status == qt.QDialog.Accepted:
            selected = model.item(index)
            self.open_example_scheme(selected.path())
        return status

    def open_about(self):
        dlg = AboutDialog(self)
        dlg.setAttribute(qt.Qt.WA_DeleteOnClose)
        dlg.exec()

    def open_simple_examples(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("simple", "EBS_tomo_listener")
        )

    def open_slurm_execution_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("slurm",)
        )

    def open_dark_flat_examples(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("darks",)
        )

    def open_python_script_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("_script",)
        )

    def open_id16b_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("ID16b",)
        )

    def open_cor_search_example(self):
        return self.__open_examples(
            orange_examples.workflows(), filter_names=("find_cor", "cor_search")
        )


log = logging.getLogger(__name__)


def check_for_updates() -> bool:
    return False


def send_usage_statistics() -> bool:
    return False


def pull_notifications() -> bool:
    return False


def make_sql_logger(level=logging.INFO):
    sql_log = logging.getLogger("sql_log")
    sql_log.setLevel(level)
    handler = RotatingFileHandler(
        os.path.join(config.log_dir(), "sql.log"), maxBytes=1e7, backupCount=2
    )
    sql_log.addHandler(handler)


class _OMain(ocMain):
    DefaultConfig = "tomwer.app.canvas_launcher.launcher.TomwerConfig"

    def run(self, argv):
        # Allow termination with CTRL + C
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # Disable pyqtgraph's atexit and QApplication.aboutToQuit cleanup handlers.
        pyqtgraph.setConfigOption("exitCleanup", False)
        super().run(argv)

    def argument_parser(self) -> argparse.ArgumentParser:
        parser = super().argument_parser()
        parser.add_argument(
            "--use-opengl-plot",
            "--opengl-backend",
            help="Use OpenGL for plots (instead of matplotlib)",
            action="store_true",
            default=False,
        )
        return parser

    def parse_arguments(self, argv: list[str]):
        super().parse_arguments(argv)
        # define silx plot backend. For now the si;pler is to
        # define an environment variable.
        # this way we should also be able to let the user define it
        # on it's own later...

        if self.options.use_opengl_plot:

            # other standalones are not passing by the silx.config
            # but for the canvas this is way simpler to use it.
            # then all plot which have backend==None will pick the default plot backend
            silx.config.DEFAULT_PLOT_BACKEND = "gl"
        else:
            silx.config.DEFAULT_PLOT_BACKEND = "matplotlib"

    def setup_logging(self):
        level = self.options.log_level
        logformat = "%(asctime)s:%(levelname)s:%(name)s: %(message)s"

        # File handler should always be at least INFO level so we need
        # the application root level to be at least at INFO.
        root_level = min(level, logging.INFO)
        rootlogger = logging.getLogger()
        rootlogger.setLevel(root_level)

        # Standard output stream handler at the requested level
        if sys.platform in ("linux", "linux2", "darwin"):
            stream_hander = make_linux_stream_colored_handler(
                level, fileobj=self.__stderr__
            )
        else:
            stream_hander = make_stream_handler(
                level, fileobj=self.__stderr__, fmt=logformat
            )
        rootlogger.addHandler(stream_hander)
        # Setup log capture for MainWindow/Log
        log_stream = TextStream(objectName="-log-stream")
        self.output.connectStream(log_stream)
        self.stack.push(closing(log_stream))  # close on exit
        log_handler = make_stream_handler(level, fileobj=log_stream, fmt=logformat)
        rootlogger.addHandler(log_handler)

        # Also log to file
        file_handler = make_file_handler(
            root_level,
            os.path.join(config.log_dir(), "canvas.log"),
            mode="w",
        )
        rootlogger.addHandler(file_handler)

        make_sql_logger(self.options.log_level)

    def setup_application(self):
        super().setup_application()
        # NOTE: No OWWidgetBase subclass should be imported before this

        self._update_check = check_for_updates()
        self._send_stat = send_usage_statistics()
        self._pull_notifs = pull_notifications()

        settings = qt.QSettings()
        settings.setValue(
            "startup/launch-count",
            settings.value("startup/launch-count", 0, int) + 1,
        )

        UsageStatistics.set_enabled(False)

    def show_splash_message(self, message: str, color=qt.QColor("#FFD39F")):
        super().show_splash_message(message, color)

    def create_main_window(self):
        window = MainWindow()
        return window

    def setup_sys_redirections(self):
        super().setup_sys_redirections()
        if isinstance(sys.excepthook, ExceptHook):
            sys.excepthook.handledException.connect(handle_exception)

    def tear_down_sys_redirections(self):
        if isinstance(sys.excepthook, ExceptHook):
            sys.excepthook.handledException.disconnect(handle_exception)
        super().tear_down_sys_redirections()

    def splash_screen(self):
        """Return the application splash screen"""
        settings = qt.QSettings()
        options = self.options
        want_splash = (
            settings.value("startup/show-splash-screen", True, type=bool)
            and not options.no_splash
        )

        if want_splash:
            pm, rect = self.config.splash_screen()
            splash_screen = TomwerSplashScreen(pixmap=pm, textRect=rect)
            splash_screen.setAttribute(qt.Qt.WA_DeleteOnClose)
            splash_screen.setFont(qt.QFont("Helvetica", 12))
            palette = splash_screen.palette()
            color = qt.QColor("#b3baba")
            palette.setColor(qt.QPalette.Text, color)
            splash_screen.setPalette(palette)
        else:
            splash_screen = None
        return splash_screen


def data_dir():
    return os.path.join(data_dir_base(), "tomwer", tomwer.version.version)


def widget_settings_dir():
    return os.path.join(data_dir(), "widgets")


ABOUT_TEMPLATE = """\
<h4>{name}</h4>
<p>tomwer version: {tomwer_version}</p>
<p>nabu version: {nabu_version}</p>
<p>nxtomo version: {nxtomo_version}</p>
<p>nxtomomill version: {nxtomomill_version}</p>
<p>tomoscan version: {tomoscan_version}</p>
<p>ewokscore version: {ewokscore_version}</p>
<p>ewoksorange version: {ewoksorange_version}</p>
<p>sluurp version: {sluurp_version}</p>
"""


class AboutDialog(qt.QDialog):
    def __init__(self, parent=None, **kwargs) -> None:
        super().__init__(parent, **kwargs)
        layout = qt.QVBoxLayout()
        label = qt.QLabel(self)

        pixmap, _ = TomwerConfig.splash_screen()
        pixmap = pixmap.scaled(150, 150)

        label.setPixmap(pixmap)

        layout.addWidget(label, qt.Qt.AlignCenter)

        text = ABOUT_TEMPLATE.format(
            name=escape("tomwer"),
            tomwer_version=escape(tomwer.version.version),
            nabu_version=escape(nabu.version if has_nabu else "not installed"),
            nxtomomill_version=escape(
                nxtomomill.version.version if has_nxtomomill else "not installed"
            ),
            nxtomo_version=escape(
                nxtomo.__version__ if has_nxotmo else "not installed"
            ),
            tomoscan_version=escape(tomoscan.version.version),
            sluurp_version=escape(
                sluurp.__version__ if has_sluurp else "not installed"
            ),
            ewokscore_version=escape(
                pkg_resources.get_distribution("ewokscore").version
            ),
            ewoksorange_version=escape(
                pkg_resources.get_distribution("ewoksorange").version
            ),
        )
        text_label = qt.QLabel(text)
        layout.addWidget(text_label, qt.Qt.AlignCenter)

        buttons = qt.QDialogButtonBox(qt.QDialogButtonBox.Close, qt.Qt.Horizontal, self)
        layout.addWidget(buttons)
        buttons.rejected.connect(self.accept)
        layout.setSizeConstraint(qt.QVBoxLayout.SetFixedSize)
        self.setLayout(layout)


class OMain(_OMain):
    config: TomwerConfig
    DefaultConfig = "tomwer.app.canvas_launcher.config.TomwerConfig"

    def run(self, argv):
        log.info("Clearing widget settings")
        shutil.rmtree(widget_settings_dir(), ignore_errors=True)
        dealWithLogFile()
        super().run(argv)

    def setup_application(self):
        qt.QLocale.setDefault(qt.QLocale(qt.QLocale.English))
        return super().setup_application()

    def setup_logging(self):
        super().setup_logging()
        # rootlogger = logging.getLogger()
        # rootlogger = TomwerLogger(rootlogger)
        # logging.setLoggerClass(TomwerLogger)

    def setup_sys_redirections(self):
        self.output = doc = TerminalTextDocument()

        stdout = TextStream(objectName="-stdout")
        stderr = TextStream(objectName="-stderr")
        doc.connectStream(stdout)
        doc.connectStream(stderr, color=qt.Qt.red)

        if sys.stdout is not None:
            stdout.stream.connect(sys.stdout.write, qt.Qt.DirectConnection)

        self.__stdout__ = sys.stdout
        sys.stdout = stdout

        if sys.stderr is not None:
            stderr.stream.connect(sys.stderr.write, qt.Qt.DirectConnection)

        self.__stderr__ = sys.stderr
        sys.stderr = stderr
        self.__excepthook__ = sys.excepthook
        sys.excepthook = ExceptHook(stream=stderr)

        self.stack.push(closing(stdout))
        self.stack.push(closing(stderr))

    def argument_parser(self) -> argparse.ArgumentParser:
        parser = super().argument_parser()
        for action in parser._actions:
            # avoid clearing settings because this make people confused
            if action.dest == "clear_widget_settings":
                parser._remove_action(action)
                break
            # by default log are only displaying errors. But we want to get warning as well (for deprecation for example).
            if action.dest == "log_level":
                action.default = logging.WARNING

        parser.add_argument(
            "--no-color-stdout-logs",
            "--no-colored-logs",
            action="store_true",
            help="instead of having logs in the log view, color logs of the stdout",
            default=False,
        )
        return parser

    def create_main_window(self):
        window = MainWindow()
        return window


def dealWithLogFile():
    """Move log file history across log file hierarchy and create the new log file"""

    # move log file if exists
    for i in range(MAX_LOG_FILE):
        logFile = LOG_FILE_NAME
        if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
            logFile = os.path.join(LOG_FOLDER, logFile)
        defLogName = logFile

        iLog = MAX_LOG_FILE - i
        maxLogNameN1 = logFile + "." + str(iLog)
        if iLog - 1 == 0:
            maxLogNameN2 = defLogName
        else:
            maxLogNameN2 = logFile + "." + str(iLog - 1)
        if os.path.exists(maxLogNameN2):
            try:
                stat = os.stat(maxLogNameN2)
                shutil.copy(maxLogNameN2, maxLogNameN1)
                os.utime(maxLogNameN1, (stat.st_atime, stat.st_mtime))
            except Exception:
                pass
    # create a new log file
    if os.path.exists(LOG_FOLDER) and os.access(LOG_FOLDER, os.W_OK):
        logFile = os.path.join(LOG_FOLDER, logFile)
        logging.basicConfig(
            filename=logFile,
            filemode="w",
            level=logging.WARNING,
            format="%(asctime)s %(message)s",
        )


class _ColoredFormatter(logging.Formatter):
    """Dedicated colors to highlight level name by coloring logs (only for linux terminals)"""

    @staticmethod
    def color_formatting(message: str, levelname: str, ascii_time):
        """colors message using ascii"""
        return (
            f"{ascii_time} {LOG_COLORS[levelname]}[{levelname}]{_RESET_SEQ} {message}"
        )

    def format(self, record):
        record.asctime = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        record.message = record.getMessage()
        return self.color_formatting(
            message=record.message,
            levelname=record.levelname,
            ascii_time=record.asctime,
        )


def make_linux_stream_colored_handler(level, fileobj=None):
    handler = logging.StreamHandler(fileobj)
    handler.setLevel(level)
    formatter = _ColoredFormatter()
    handler.setFormatter(formatter)
    return handler


def make_stream_handler(level, fileobj=None, fmt=None):
    handler = logging.StreamHandler(fileobj)
    handler.setLevel(level)
    if fmt:
        handler.setFormatter(logging.Formatter(fmt))
    return handler


def make_file_handler(level, filename, mode="w", fmt=None):
    handler = logging.FileHandler(filename, mode=mode, encoding="utf-8")
    handler.setLevel(level)
    if fmt:
        handler.setFormatter(logging.Formatter(fmt))
    return handler

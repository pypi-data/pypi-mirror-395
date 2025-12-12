import gc
import os
import logging

import pytest
from ewoksorange.bindings.qtapp import get_all_qtwidgets, qtapp_context

_logger = logging.getLogger(__name__)


def global_cleanup_orange():
    from orangecanvas.document.suggestions import Suggestions

    Suggestions.instance = None


def global_cleanup_pytest():
    for obj in gc.get_objects():
        if isinstance(obj, logging.LogRecord):
            obj.exc_info = None  # traceback keeps frames which keep locals


def collect_garbage(app):
    if app is None:
        return
    app.processEvents()
    while gc.collect():
        app.processEvents()


@pytest.fixture(scope="session")
def qtapp():
    """
    create a Qt application if doesn't exists
    """
    with qtapp_context() as app:
        yield app
    collect_garbage(app)
    global_cleanup_orange()
    global_cleanup_pytest()
    collect_garbage(app)
    warn_qtwidgets_alive()


def warn_qtwidgets_alive():
    widgets = get_all_qtwidgets()
    if widgets:
        _logger.warning(
            "%d remaining widgets after tests:\n %s",
            len(widgets),
            "\n ".join(map(str, widgets)),
        )


@pytest.fixture(scope="function")
def nxtomo_scan_180(tmp_path):
    test_path = tmp_path / "test"
    test_path.mkdir()
    yield create_default_scan(
        scan_path=os.path.join(test_path, "scan_180"),
        scan_range=180,
    )


@pytest.fixture(scope="function")
def nxtomo_scan_360(tmp_path):
    test_path = tmp_path / "test"
    test_path.mkdir()
    yield create_default_scan(
        scan_path=os.path.join(test_path, "scan_360"),
        scan_range=360,
    )


def create_default_scan(scan_path: str, scan_range: int):
    from tomwer.core.utils.scanutils import MockNXtomo

    return MockNXtomo(
        scan_path=scan_path,
        n_proj=10,
        n_ini_proj=10,
        scan_range=scan_range,
        dim=20,
        energy=12.3,
    ).scan

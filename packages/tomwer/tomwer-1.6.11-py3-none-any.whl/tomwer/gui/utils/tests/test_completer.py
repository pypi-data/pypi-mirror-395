# coding: utf-8

"""module defining dedicated completer"""

from __future__ import annotations


import pytest
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt

from tomwer.gui.utils.completer import UrlCompleterDialog
from tomwer.tests.utils import skip_gui_test


@pytest.mark.skipif(skip_gui_test(), reason="skip gui test")
class TestUrlCompleterDialog(TestCaseQt):
    def setUp(self):
        super().setUp()
        self._urls = (
            "test",
            "test1",
            "test2",
        )
        self._dialog = UrlCompleterDialog(
            urls=self._urls,
            current_url="test",
        )

    def tearDown(self):
        self._dialog.setAttribute(qt.Qt.WA_DeleteOnClose)
        self._dialog.close()
        self._dialog = None
        super().tearDown()

    def test(self):
        """simple test on the dialog behavior"""
        assert self._dialog._buttons.button(qt.QDialogButtonBox.Ok).isEnabled()
        self._dialog._completerWidget.setText("toto")
        self.qapp.processEvents()
        assert not self._dialog._buttons.button(qt.QDialogButtonBox.Ok).isEnabled()

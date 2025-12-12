"""This is almost the original orange3 PythonScript widget except that
the icon change (to difference them) and here the input is not a Table
but a TomwerScanBase (use silx.gui.qt instead of AnyQt too)"""

import code
import itertools
import keyword
import os
import sys
import unicodedata
from unittest.mock import patch

from orangewidget import gui, widget
from orangewidget.settings import Setting, SettingsHandler
from orangewidget.utils import itemmodels
from orangewidget.widget import Input, Output, OWBaseWidget
from silx.gui import qt
from tomoscan.series import Series

import tomwer.tasks.script.python
from tomwer.core.settings import ParametersKeys
from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.tomwer_object import TomwerObject


__all__ = ["OWPythonScript"]


def text_format(foreground=qt.Qt.black, weight=qt.QFont.Normal):
    fmt = qt.QTextCharFormat()
    fmt.setForeground(qt.QBrush(foreground))
    fmt.setFontWeight(weight)
    return fmt


class PythonSyntaxHighlighter(qt.QSyntaxHighlighter):
    def __init__(self, parent=None):
        self.keywordFormat = text_format(qt.Qt.blue, qt.QFont.Bold)
        self.stringFormat = text_format(qt.Qt.darkGreen)
        self.defFormat = text_format(qt.Qt.black, qt.QFont.Bold)
        self.commentFormat = text_format(qt.Qt.lightGray)
        self.decoratorFormat = text_format(qt.Qt.darkGray)

        self.keywords = list(keyword.kwlist)

        self.rules = [
            (qt.QRegularExpression(r"\b%s\b" % kwd), self.keywordFormat)
            for kwd in self.keywords
        ] + [
            (
                qt.QRegularExpression(r"\bdef\s+([A-Za-z_]+[A-Za-z0-9_]+)\s*\("),
                self.defFormat,
            ),
            (
                qt.QRegularExpression(r"\bclass\s+([A-Za-z_]+[A-Za-z0-9_]+)\s*\("),
                self.defFormat,
            ),
            (qt.QRegularExpression(r"'.*'"), self.stringFormat),
            (qt.QRegularExpression(r'".*"'), self.stringFormat),
            (qt.QRegularExpression(r"#.*"), self.commentFormat),
            (qt.QRegularExpression(r"@[A-Za-z_]+[A-Za-z0-9_]+"), self.decoratorFormat),
        ]

        self.multilineStart = qt.QRegularExpression(r"(''')|" + r'(""")')
        self.multilineEnd = qt.QRegularExpression(r"(''')|" + r'(""")')

        super().__init__(parent)

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            exp = qt.QRegularExpression(pattern)
            index = exp.match(text).capturedStart()
            while index >= 0:
                match = exp.match(text)
                length = match.capturedLength()
                if exp.captureCount() > 0:
                    nth = 1
                else:
                    nth = 0
                capture_text = exp.match(text).capturedTexts()[nth]
                self.setFormat(match.capturedStart(nth=nth), len(capture_text), format)
                index = exp.match(text, index + length).capturedStart()

        # Multi line strings
        start = self.multilineStart
        end = self.multilineEnd

        self.setCurrentBlockState(0)
        startIndex, skip = 0, 0
        if self.previousBlockState() != 1:
            startIndex, skip = start.match(text).capturedStart(), 3
        while startIndex >= 0:
            endIndex = end.match(text).capturedStart(startIndex + skip)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLen = len(text) - startIndex
            else:
                commentLen = endIndex - startIndex + 3
            self.setFormat(startIndex, commentLen, self.stringFormat)
            startIndex, skip = (
                start.match(text).capturedStart(startIndex + commentLen + 3),
                3,
            )


class PythonScriptEditor(qt.QPlainTextEdit):
    INDENT = 4

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def lastLine(self):
        text = str(self.toPlainText())
        pos = self.textCursor().position()
        index = text.rfind("\n", 0, pos)
        text = text[index:pos].lstrip("\n")
        return text

    def keyPressEvent(self, event):
        if event.key() == qt.Qt.Key_Return:
            if event.modifiers() & (
                qt.Qt.ShiftModifier | qt.Qt.ControlModifier | qt.Qt.MetaModifier
            ):
                self.widget.commit()
                return
            text = self.lastLine()
            indent = len(text) - len(text.lstrip())
            if text.strip() == "pass" or text.strip().startswith("return "):
                indent = max(0, indent - self.INDENT)
            elif text.strip().endswith(":"):
                indent += self.INDENT
            super().keyPressEvent(event)
            self.insertPlainText(" " * indent)
        elif event.key() == qt.Qt.Key_Tab:
            self.insertPlainText(" " * self.INDENT)
        elif event.key() == qt.Qt.Key_Backspace:
            text = self.lastLine()
            if text and not text.strip():
                cursor = self.textCursor()
                for _ in range(min(self.INDENT, len(text))):
                    cursor.deletePreviousChar()
            else:
                super().keyPressEvent(event)

        else:
            super().keyPressEvent(event)


class PythonConsole(qt.QPlainTextEdit, code.InteractiveConsole):
    def __init__(self, locals=None, parent=None):
        qt.QPlainTextEdit.__init__(self, parent)
        code.InteractiveConsole.__init__(self, locals)
        self.history, self.historyInd = [""], 0
        self.loop = self.interact()
        next(self.loop)

    def setLocals(self, locals):
        self.locals = locals

    def updateLocals(self, locals):
        self.locals.update(locals)

    def interact(self, banner=None):
        try:
            sys.ps1
        except AttributeError:
            sys.ps1 = ">>> "
        try:
            sys.ps2
        except AttributeError:
            sys.ps2 = "... "
        cprt = (
            'Type "help", "copyright", "credits" or "license" ' "for more information."
        )
        if banner is None:
            self.write(
                "Python %s on %s\n%s\n(%s)\n"
                % (sys.version, sys.platform, cprt, self.__class__.__name__)
            )
        else:
            self.write("%s\n" % str(banner))
        more = 0
        while 1:
            try:
                if more:
                    prompt = sys.ps2
                else:
                    prompt = sys.ps1
                self.new_prompt(prompt)
                yield
                try:
                    line = self.raw_input(prompt)
                except EOFError:
                    self.write("\n")
                    break
                else:
                    more = self.push(line)
            except KeyboardInterrupt:
                self.write("\nKeyboardInterrupt\n")
                self.resetbuffer()
                more = 0

    def raw_input(self, prompt):
        input = str(self.document().lastBlock().previous().text())
        return input[len(prompt) :]

    def new_prompt(self, prompt):
        self.write(prompt)
        self.newPromptPos = self.textCursor().position()
        self.repaint()

    def write(self, data):
        cursor = qt.QTextCursor(self.document())
        cursor.movePosition(qt.QTextCursor.End, qt.QTextCursor.MoveAnchor)
        cursor.insertText(data)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def flush(self):
        pass

    def push(self, line):
        if self.history[0] != line:
            self.history.insert(0, line)
        self.historyInd = 0

        # prevent console errors to trigger error reporting & patch stdout, stderr
        with (
            patch("sys.excepthook", sys.__excepthook__),
            patch("sys.stdout", self),
            patch("sys.stderr", self),
        ):
            return code.InteractiveConsole.push(self, line)

    def setLine(self, line):
        cursor = qt.QTextCursor(self.document())
        cursor.movePosition(qt.QTextCursor.End)
        cursor.setPosition(self.newPromptPos, qt.QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(line)
        self.setTextCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == qt.Qt.Key_Return:
            self.write("\n")
            next(self.loop)
        elif event.key() == qt.Qt.Key_Up:
            self.historyUp()
        elif event.key() == qt.Qt.Key_Down:
            self.historyDown()
        elif event.key() == qt.Qt.Key_Tab:
            self.complete()
        elif event.key() in [qt.Qt.Key_Left, qt.Qt.Key_Backspace]:
            if self.textCursor().position() > self.newPromptPos:
                qt.QPlainTextEdit.keyPressEvent(self, event)
        else:
            qt.QPlainTextEdit.keyPressEvent(self, event)

    def historyUp(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = min(self.historyInd + 1, len(self.history) - 1)

    def historyDown(self):
        self.setLine(self.history[self.historyInd])
        self.historyInd = max(self.historyInd - 1, 0)

    def complete(self):
        pass

    def _moveCursorToInputLine(self):
        """
        Move the cursor to the input line if not already there. If the cursor
        if already in the input line (at position greater or equal to
        `newPromptPos`) it is left unchanged, otherwise it is moved at the
        end.

        """
        cursor = self.textCursor()
        pos = cursor.position()
        if pos < self.newPromptPos:
            cursor.movePosition(qt.QTextCursor.End)
            self.setTextCursor(cursor)

    def pasteCode(self, source):
        """
        Paste source code into the console.
        """
        self._moveCursorToInputLine()

        for line in interleave(source.splitlines(), itertools.repeat("\n")):
            if line != "\n":
                self.insertPlainText(line)
            else:
                self.write("\n")
                next(self.loop)

    def insertFromMimeData(self, source):
        """
        Reimplemented from QPlainTextEdit.insertFromMimeData.
        """
        if source.hasText():
            self.pasteCode(str(source.text()))
            return


def interleave(seq1, seq2):
    """
    Interleave elements of `seq2` between consecutive elements of `seq1`.

        >>> list(interleave([1, 3, 5], [2, 4]))
        [1, 2, 3, 4, 5]

    """
    iterator1, iterator2 = iter(seq1), iter(seq2)
    leading = next(iterator1)
    for element in iterator1:
        yield leading
        yield next(iterator2)
        leading = element

    yield leading


class Script(object):
    Modified = 1
    MissingFromFilesystem = 2

    def __init__(self, name, script, flags=0, filename=None):
        self.name = name
        self.script = script
        self.flags = flags
        self.filename = filename


class ScriptItemDelegate(qt.QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)

    def displayText(self, script, locale):
        if script.flags & Script.Modified:
            return "*" + script.name
        else:
            return script.name

    def paint(self, painter, option, index):
        script = index.data(qt.Qt.DisplayRole)

        if script.flags & Script.Modified:
            option = qt.QStyleOptionViewItem(option)
            option.palette.setColor(qt.QPalette.Text, qt.QColor(qt.Qt.red))
            option.palette.setColor(qt.QPalette.Highlight, qt.QColor(qt.Qt.darkRed))
        super().paint(painter, option, index)

    def createEditor(self, parent, option, index):
        return qt.QLineEdit(parent)

    def setEditorData(self, editor, index):
        script = index.data(qt.Qt.DisplayRole)
        editor.setText(script.name)

    def setModelData(self, editor, model, index):
        model[index.row()].name = str(editor.text())


def select_row(view, row):
    """
    Select a `row` in an item view
    """
    selmodel = view.selectionModel()
    selmodel.select(view.model().index(row, 0), qt.QItemSelectionModel.ClearAndSelect)


class PrepareSavingSettingsHandler(SettingsHandler):
    """Calls storeSpecificSettings, which is currently not called from non-context handlers."""

    def pack_data(self, widget):
        """
        Pack the settings for the given widget. This method is used when
        saving schema, so that when the schema is reloaded the widget is
        initialized with its proper data and not the class-based defaults.
        See :obj:`SettingsHandler.initialize` for detailed explanation of its
        use.

        Inherited classes add other data, in particular widget-specific
        local contexts.

        :param OWBaseWidget widget:
        """
        widget.storeSpecificSettings()
        return super().pack_data(widget)


class OWPythonScript(widget.OWBaseWidget, openclass=True):
    name = "Python Script"
    description = "Write a Python script and run it on input data or models."
    icon = "icons/PythonScript.svg"
    priority = 3150
    keywords = ["file", "program"]

    class Inputs:
        tomo_obj = Input(
            "tomo_obj",
            TomwerObject,
            replaces=["in_tomo_obj"],
            default=True,
            multiple=True,
        )
        tomo_objs = Input(
            "tomo_objs",
            TomwerObject,
            replaces=["in_tomo_objs"],
            default=True,
            multiple=True,
        )
        data = Input(
            "data", TomwerScanBase, replaces=["in_data"], default=True, multiple=True
        )
        volume = Input(
            "volume",
            TomwerVolumeBase,
            replaces=["in_volume"],
            default=True,
            multiple=True,
        )
        future_tomo_obj = Input(
            "future_tomo_obj",
            FutureTomwerObject,
            replaces=["in_future_tomo_obj"],
            default=True,
            multiple=True,
        )
        cluster_config = Input(
            ParametersKeys.SLURM_CLUSTER_KEY,
            SlurmClusterConfiguration,
            replaces=["in_cluster_config"],
            default=True,
            multiple=True,
        )
        object = Input(
            "Object",
            object,
            replaces=["in_object"],
            default=False,
            multiple=True,
            auto_summary=False,
        )
        configuration = Input(
            "configuration",
            TomwerScanBase,
            replaces=["in_configuration"],
            default=True,
            multiple=True,
        )
        series = Input(
            "series",
            Series,
            replaces=["in_series"],
            default=True,
            multiple=True,
        )

    class Outputs:
        data = Output("data", TomwerScanBase, replaces=["out_data"])
        tomo_obj = Output("tomo_obj", TomwerObject, replaces=["out_tomo_obj"])
        tomo_objs = Output("tomo_objs", tuple, replaces=["out_tomo_objs"])
        volume = Output("volume", TomwerVolumeBase, replaces=["out_volume"])
        object = Output("Object", object, replaces=["out_object"], auto_summary=False)
        configuration = Output("configuration", dict, replaces=["out_configuration"])
        future_tomo_obj = Output(
            "future_tomo_obj", FutureTomwerObject, replaces=["out_future_tomo_obj"]
        )
        cluster_config = Output(
            ParametersKeys.SLURM_CLUSTER_KEY,
            SlurmClusterConfiguration,
            replaces=["out_cluster_config"],
        )
        series = Output("series", dict, replaces=["out_series"])

    signal_names = (
        "data",
        "volume",
        "future_tomo_obj",
        "object",
        "configuration",
        ParametersKeys.SLURM_CLUSTER_KEY,
        "series",
        "tomo_obj",
        "tomo_objs",
    )

    settingsHandler = PrepareSavingSettingsHandler()

    libraryListSource = Setting([Script("Hello world", "print('Hello world')\n")])
    currentScriptIndex = Setting(0)
    scriptText = Setting(None, schema_only=True)
    splitterState = Setting(None)

    ewokstaskclass = tomwer.tasks.script.python.PythonScript

    class Error(OWBaseWidget.Error):
        pass

    def __init__(self):
        super().__init__()

        for name in self.signal_names:
            setattr(self, name, {})

        for s in self.libraryListSource:  # pylint: disable=E1133
            s.flags = 0

        self._cachedDocuments = {}

        self.infoBox = gui.vBox(self.controlArea, "Info")
        gui.label(
            self.infoBox,
            self,
            "<p>Execute python script.</p><p>Input variables:<ul><li> "
            + "<li>".join(map("in_{0}, in_{0}s".format, self.signal_names))
            + "</ul></p><p>Output variables:<ul><li>"
            + "<li>".join(map("out_{0}".format, self.signal_names))
            + "</ul></p>",
        )

        self.libraryList = itemmodels.PyListModel(
            [],
            self,
            flags=qt.Qt.ItemIsSelectable | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsEditable,
        )

        self.libraryList.wrap(self.libraryListSource)

        self.controlBox = gui.vBox(self.controlArea, "Library")
        self.controlBox.layout().setSpacing(1)

        self.libraryView = qt.QListView(
            editTriggers=qt.QListView.DoubleClicked | qt.QListView.EditKeyPressed,
            sizePolicy=qt.QSizePolicy(qt.QSizePolicy.Ignored, qt.QSizePolicy.Preferred),
        )
        self.libraryView.setItemDelegate(ScriptItemDelegate(self))
        self.libraryView.setModel(self.libraryList)

        self.libraryView.selectionModel().selectionChanged.connect(
            self.onSelectedScriptChanged
        )
        self.controlBox.layout().addWidget(self.libraryView)

        w = itemmodels.ModelActionsWidget()

        self.addNewScriptAction = action = qt.QAction("+", self)
        action.setToolTip("Add a new script to the library")
        action.triggered.connect(self.onAddScript)
        w.addAction(action)

        action = qt.QAction(unicodedata.lookup("MINUS SIGN"), self)
        action.setToolTip("Remove script from library")
        action.triggered.connect(self.onRemoveScript)
        w.addAction(action)

        action = qt.QAction("Update", self)
        action.setToolTip("Save changes in the editor to library")
        action.setShortcut(qt.QKeySequence(qt.QKeySequence.Save))
        action.triggered.connect(self.commitChangesToLibrary)
        w.addAction(action)

        action = qt.QAction("More", self, toolTip="More actions")

        new_from_file = qt.QAction("Import Script from File", self)
        save_to_file = qt.QAction("Save Selected Script to File", self)
        restore_saved = qt.QAction("Undo Changes to Selected Script", self)
        save_to_file.setShortcut(qt.QKeySequence(qt.QKeySequence.SaveAs))

        new_from_file.triggered.connect(self.onAddScriptFromFile)
        save_to_file.triggered.connect(self.saveScript)
        restore_saved.triggered.connect(self.restoreSaved)

        menu = qt.QMenu(w)
        menu.addAction(new_from_file)
        menu.addAction(save_to_file)
        menu.addAction(restore_saved)
        action.setMenu(menu)
        button = w.addAction(action)
        button.setPopupMode(qt.QToolButton.InstantPopup)

        w.layout().setSpacing(1)

        self.controlBox.layout().addWidget(w)

        self.execute_button = gui.button(
            self.controlArea, self, "Run", callback=self.commit
        )

        self.splitCanvas = qt.QSplitter(qt.Qt.Vertical, self.mainArea)
        self.mainArea.layout().addWidget(self.splitCanvas)

        self.defaultFont = defaultFont = (
            "Monaco" if sys.platform == "darwin" else "Courier"
        )

        self.textBox = gui.vBox(self, "Python Script")
        self.splitCanvas.addWidget(self.textBox)
        self.text = PythonScriptEditor(self)
        self.textBox.layout().addWidget(self.text)

        self.textBox.setAlignment(qt.Qt.AlignVCenter)
        self.text.setTabStopWidth(4)

        self.text.modificationChanged[bool].connect(self.onModificationChanged)

        self.saveAction = action = qt.QAction("&Save", self.text)
        action.setToolTip("Save script to file")
        action.setShortcut(qt.QKeySequence(qt.QKeySequence.Save))
        action.setShortcutContext(qt.Qt.WidgetWithChildrenShortcut)
        action.triggered.connect(self.saveScript)

        self.consoleBox = gui.vBox(self, "Console")
        self.splitCanvas.addWidget(self.consoleBox)
        self.console = PythonConsole({}, self)
        self.consoleBox.layout().addWidget(self.console)
        self.console.document().setDefaultFont(qt.QFont(defaultFont))
        self.consoleBox.setAlignment(qt.Qt.AlignBottom)
        self.console.setTabStopWidth(4)

        select_row(self.libraryView, self.currentScriptIndex)

        self.restoreScriptText()

        self.splitCanvas.setSizes([2, 1])
        if self.splitterState is not None:
            self.splitCanvas.restoreState(qt.QByteArray(self.splitterState))

        self.splitCanvas.splitterMoved[int, int].connect(self.onSpliterMoved)
        self.controlArea.layout().addStretch(1)
        self.resize(800, 600)

    def storeSpecificSettings(self):
        self.saveScriptText()

    def restoreScriptText(self):
        if self.scriptText is not None:
            current = self.text.toPlainText()
            # do not mark scripts as modified
            if self.scriptText != current:
                self.text.document().setPlainText(self.scriptText)

    def saveScriptText(self):
        self.scriptText = self.text.toPlainText()

    def handle_input(self, obj, id, signal):
        id = id[0]
        dic = getattr(self, signal)
        if obj is None:
            if id in dic.keys():
                del dic[id]
        else:
            dic[id] = obj

    @Inputs.data  # noqa F811
    def set_data(self, data, id):
        self.handle_input(data, id, "data")

    @Inputs.volume  # noqa F811
    def set_volume(self, volume, id):
        self.handle_input(volume, id, "volume")

    @Inputs.object  # noqa F811
    def set_object(self, data, id):  # noqa F811
        self.handle_input(data, id, "object")

    @Inputs.configuration  # noqa F811
    def set_configuration(self, data, id):
        self.handle_input(data, id, "configuration")

    @Inputs.future_tomo_obj  # noqa F811
    def set_future_tomo_object(self, data, id):  # noqa F811 pylint: disable=E0102
        self.handle_input(data, id, "future_tomo_obj")

    @Inputs.cluster_config  # noqa F811
    def set_cluster_config(self, data, id):  # noqa F811 pylint: disable=E0102
        self.handle_input(data, id, ParametersKeys.SLURM_CLUSTER_KEY)

    @Inputs.series  # noqa F811
    def set_series(self, data, id):
        self.handle_input(data, id, "series")

    @Inputs.tomo_obj  # noqa F811
    def set_tomo_obj(self, tomo_obj, id):
        self.handle_input(tomo_obj, id, "tomo_obj")

    @Inputs.tomo_objs  # noqa F811
    def set_tomo_objs(self, tomo_objs, id):
        self.handle_input(tomo_objs, id, "tomo_objs")

    def handleNewSignals(self):
        self.commit()

    def selectedScriptIndex(self):
        rows = self.libraryView.selectionModel().selectedRows()
        if rows:
            return [i.row() for i in rows][0]
        else:
            return None

    def setSelectedScript(self, index):
        select_row(self.libraryView, index)

    def onAddScript(self, *args):
        self.libraryList.append(Script("New script", self.text.toPlainText(), 0))
        self.setSelectedScript(len(self.libraryList) - 1)

    def onAddScriptFromFile(self, *args):  # pragma: no cover
        filename, _ = qt.QFileDialog.getOpenFileName(
            self,
            "Open Python Script",
            os.path.expanduser("~/"),
            "Python files (*.py)\nAll files(*.*)",
        )
        if filename:
            name = os.path.basename(filename)
            # TODO: use `tokenize.detect_encoding`
            with open(filename, encoding="utf-8") as f:
                contents = f.read()
            self.libraryList.append(Script(name, contents, 0, filename))
            self.setSelectedScript(len(self.libraryList) - 1)

    def onRemoveScript(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            del self.libraryList[index]
            select_row(self.libraryView, max(index - 1, 0))

    def onSaveScriptToFile(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            self.saveScript()

    def onSelectedScriptChanged(self, selected, deselected):
        index = [i.row() for i in selected.indexes()]
        if index:
            current = index[0]
            if current >= len(self.libraryList):
                self.addNewScriptAction.trigger()
                return

            self.text.setDocument(self.documentForScript(current))
            self.currentScriptIndex = current

    def documentForScript(self, script=0):
        if type(script) is not Script:
            script = self.libraryList[script]
        if script not in self._cachedDocuments:
            doc = qt.QTextDocument(self)
            doc.setDocumentLayout(qt.QPlainTextDocumentLayout(doc))
            doc.setPlainText(script.script)
            doc.setDefaultFont(qt.QFont(self.defaultFont))
            doc.highlighter = PythonSyntaxHighlighter(doc)
            doc.modificationChanged[bool].connect(self.onModificationChanged)
            doc.setModified(False)
            self._cachedDocuments[script] = doc
        return self._cachedDocuments[script]

    def commitChangesToLibrary(self, *args):
        index = self.selectedScriptIndex()
        if index is not None:
            self.libraryList[index].script = self.text.toPlainText()
            self.text.document().setModified(False)
            self.libraryList.emitDataChanged(index)

    def onModificationChanged(self, modified):
        index = self.selectedScriptIndex()
        if index is not None:
            self.libraryList[index].flags = Script.Modified if modified else 0
            self.libraryList.emitDataChanged(index)

    def onSpliterMoved(self, pos, ind):
        self.splitterState = bytes(self.splitCanvas.saveState())

    def restoreSaved(self):
        index = self.selectedScriptIndex()
        if index is not None:
            self.text.document().setPlainText(self.libraryList[index].script)
            self.text.document().setModified(False)

    def saveScript(self):  # pragma: no cover
        index = self.selectedScriptIndex()
        if index is not None:
            script = self.libraryList[index]
            filename = script.filename
        else:
            filename = os.path.expanduser("~/")

        filename, _ = qt.QFileDialog.getSaveFileName(
            self, "Save Python Script", filename, "Python files (*.py)\nAll files(*.*)"
        )

        if filename:
            fn = ""
            head, tail = os.path.splitext(filename)
            if not tail:
                fn = head + ".py"
            else:
                fn = filename

            f = open(fn, "w")
            f.write(self.text.toPlainText())
            f.close()

    def initial_locals_state(self):
        d = {}
        for name in self.signal_names:
            value = getattr(self, name)
            all_values = list(value.values())
            one_value = all_values[0] if len(all_values) == 1 else None
            d["in_" + name + "s"] = all_values
            d["in_" + name] = one_value
        return d

    def commit(self):
        self.Error.clear()
        self._script = str(self.text.toPlainText())
        lcls = self.initial_locals_state()
        lcls["_script"] = str(self.text.toPlainText())
        self.console.updateLocals(lcls)
        self.console.write("\nRunning script:\n")
        self.console.push("exec(_script)")
        self.console.new_prompt(sys.ps1)
        for signal in self.signal_names:
            out_var = self.console.locals.get("out_" + signal)
            signal_type = getattr(self.Outputs, signal).type
            if not isinstance(out_var, signal_type) and out_var is not None:
                self.Error.add_message(
                    signal,
                    f"'{signal}' has to be an instance of '{signal_type.__name__}'",
                )
                getattr(self.Error, signal)()
                out_var = None
            getattr(self.Outputs, signal).send(out_var)

# coding: utf-8

"""
Some utils GUI associated to illustrations
"""

from __future__ import annotations

from silx.gui import qt

from tomwer.gui import illustrations


class _IllustrationWidget(qt.QWidget):
    """Simple widget to display an image keeping the aspect ratio"""

    def __init__(self, parent, img=None):
        super().__init__(parent)
        self._ratio = 1.0
        self._oPixmap = None
        """Pixmap containing the image to display"""

        self.setLayout(qt.QGridLayout())
        try:
            self._display = qt.QSvgWidget(parent=self)
            self._use_svg = True
        except Exception:
            self._display = qt.QLabel(parent=self)
            self._use_svg = False
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._display.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

        self.layout().addWidget(self._display, 0, 0)
        spacer1 = qt.QWidget(self)
        spacer1.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.MinimumExpanding)
        self.layout().addWidget(spacer1, 0, 1)
        spacer2 = qt.QWidget(self)
        spacer2.setSizePolicy(qt.QSizePolicy.MinimumExpanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(spacer2, 1, 0)

        if img:
            assert isinstance(img, str)
            self.setImage(img)

    def heightForWidth(self, width):
        return width * self._ratio

    def widthForHeight(self, height):
        return height / self._ratio

    def resizeEvent(self, event):
        width = event.size().width()
        height = self.heightForWidth(width)
        if height > event.size().height():
            height = event.size().height()
            width = self.widthForHeight(height)

        self._display.resize(int(width), int(height))
        if self.isUsingSvg() is False:
            self._updatePixamp()

    def setImage(self, image):
        _image = image.replace(" ", "_")
        self._ratio = 1.0
        self._oPixmap = illustrations.getQPixmap(_image)
        self._ratio = self._oPixmap.height() / self._oPixmap.width()

        if type(self._display) is qt.QLabel:
            self._updatePixamp()
        else:
            self._display.load(illustrations.getResourceFileName(_image + ".svg"))

    def _updatePixamp(self):
        pixmap = self._oPixmap.scaled(self.width(), self.height())
        self._display.setPixmap(pixmap)

    def isUsingSvg(self):
        return self._use_svg


class _IllustrationDialog(qt.QDialog):
    def __init__(self, parent, title, img):
        qt.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.setLayout(qt.QVBoxLayout())
        self._illustration = _IllustrationWidget(parent=self, img=img)
        self.layout().addWidget(self._illustration)

        types = qt.QDialogButtonBox.Ok
        self.__buttons = qt.QDialogButtonBox(parent=self)
        self.__buttons.setStandardButtons(types)
        self.layout().addWidget(self.__buttons)

        self.__buttons.accepted.connect(self.accept)

    def sizeHint(self):
        return qt.QSize(300, 300)

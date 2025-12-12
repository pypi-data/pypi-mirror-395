"""contains 'QConfigFileDialog': dialog to get / set a .cfg file"""

import os
from silx.gui import qt


class QConfigFileDialog(qt.QFileDialog):
    """dialog to get / set a configuration file (as a .cfg file)"""

    def __init__(self, parent, multiSelection=False):
        qt.QFileDialog.__init__(self, parent)
        self.setNameFilters(
            [
                "config file (*.cfg *.conf *.config *.par)",
                "Any files (*)",
            ]
        )
        self._selected_files = []

        # check if 'TOMWER_DEFAULT_INPUT_DIR' has been set
        if os.environ.get("TOMWER_DEFAULT_INPUT_DIR", None) and os.path.exists(
            os.environ["TOMWER_DEFAULT_INPUT_DIR"]
        ):
            self.setDirectory(os.environ["TOMWER_DEFAULT_INPUT_DIR"])

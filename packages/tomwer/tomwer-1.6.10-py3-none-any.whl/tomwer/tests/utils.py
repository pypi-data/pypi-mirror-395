import os


def skip_gui_test():
    return os.environ.get("_TOMWER_NO_GUI_UNIT_TESTS", "False") == "True"

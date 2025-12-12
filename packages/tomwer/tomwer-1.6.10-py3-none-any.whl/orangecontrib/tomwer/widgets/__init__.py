"""
(Ewoks)Orange Widgets dedicated for tomography
"""

from ewoksorange.pkg_meta import get_distribution


ICON = "../widgets/icons/tomwer.png"

BACKGROUND = "#C0CCFF"


# Entry point for main Orange categories/widgets discovery
def widget_discovery(discovery):
    dist = get_distribution("tomwer")
    pkgs = [
        "orangecontrib.tomwer.widgets.cluster",
        "orangecontrib.tomwer.widgets.control",
        "orangecontrib.tomwer.widgets.deprecated",
        "orangecontrib.tomwer.widgets.debugtools",
        "orangecontrib.tomwer.widgets.edit",
        "orangecontrib.tomwer.widgets.dataportal",
        "orangecontrib.tomwer.widgets.reconstruction",
        # "orangecontrib.tomwer.widgets.stitching",
        "orangecontrib.tomwer.widgets.visualization",
        "orangecontrib.tomwer.widgets.other",
    ]
    for pkg in pkgs:
        discovery.process_category_package(pkg, distribution=dist)


WIDGET_HELP_PATH = (
    # Used for development.
    # You still need to build help pages using
    # make htmlhelp
    # inside doc folder
    # (
    #     "/home/payno/Documents/dev/tomography/tomwer/build/html/canvas/widgets/widgets.html",
    #     None,
    # ),
    ("https://tomwer.readthedocs.io/en/latest/canvas/widgets/widgets.html", None),
)

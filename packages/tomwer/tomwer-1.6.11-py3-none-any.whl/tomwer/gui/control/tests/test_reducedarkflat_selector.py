import numpy
from silx.gui.utils.testutils import SignalListener
from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.control.reducedarkflatselector import (
    filter_selected_reduced_frames,
    filter_unselected_reduced_frames,
    ReduceDarkFlatSelectorWidget,
    ReduceDarkFlatSelectorDialog,
)


def test_reduce_darkflat_selector(
    qtapp,  # noqa F811
):
    widget = ReduceDarkFlatSelectorWidget()
    widget.show()

    widget.addReduceFrames(
        {
            0: numpy.random.random(100 * 100).reshape(100, 100),
            1: numpy.random.random(100 * 100).reshape(100, 100),
        }
    )

    widget.addReduceFrames(
        {
            "reduce_frames_name": "my_dict",
            -1: numpy.random.random(100 * 100).reshape(100, 100),
            2: numpy.random.random(100 * 100).reshape(100, 100),
        }
    )

    config = widget.getConfiguration()
    assert len(config) == 2
    assert config[0]["reduce_frames_name"] == "reduced frames #0"
    assert config[1]["reduce_frames_name"] == "my_dict"

    widget.setConfiguration(
        (
            {
                "reduce_frames_name": "toto frames",
                "reduce_frames": (
                    {
                        "index": -1,  # -1 will be interpreated as at the end of the acquisition
                        "data": numpy.random.random(20 * 20).reshape(20, 20),
                        "selected": True,
                    },
                    {
                        "index": 0,
                        "data": numpy.random.random(20 * 20).reshape(20, 20),
                        "selected": True,
                    },
                ),
            },
            {
                "reduce_frames_name": "tata frames",
                "reduce_frames": (
                    {
                        "index": "0.25r",
                        "data": numpy.random.random(40 * 20).reshape(40, 20),
                        "selected": False,
                    },
                ),
            },
        )
    )

    config = widget.getConfiguration()
    assert len(config) == 2
    # check selection has been well take into account
    assert config[0]["reduce_frames"][0]["selected"]
    assert config[0]["reduce_frames"][1]["selected"]
    assert not config[1]["reduce_frames"][0]["selected"]

    selected_frames = widget.getSelectedReduceFrames()
    assert -1 in selected_frames
    assert 0 in selected_frames
    assert 0.25 not in selected_frames

    # test receive twice the same 'reduce_frames_name'
    widget.clear()
    assert len(widget.getConfiguration()) == 0
    for i in range(2):
        widget.addReduceFrames(
            {
                "reduce_frames_name": "my_dict",
                -1: numpy.random.random(100 * 100).reshape(100, 100),
                2: numpy.random.random(100 * 100).reshape(100, 100),
            }
        )
    assert len(widget.getConfiguration()) == 1


def test_reduce_darkflat_selector_dialog(
    qtapp,  # noqa F811
):
    dialog = ReduceDarkFlatSelectorDialog()

    flat_sel_signal_listener = SignalListener()
    dialog.sigSelectActiveAsFlats.connect(flat_sel_signal_listener)

    dark_sel_signal_listener = SignalListener()
    dialog.sigSelectActiveAsDarks.connect(dark_sel_signal_listener)

    dialog.show()

    dialog.addReduceFrames(
        {
            0: numpy.random.random(100 * 100).reshape(100, 100),
            1: numpy.random.random(100 * 100).reshape(100, 100),
        },
        selected=(1,),
    )

    dialog.addReduceFrames(
        {
            "reduce_frames_name": "my_dict",
            -1: numpy.random.random(100 * 100).reshape(100, 100),
            2: numpy.random.random(100 * 100).reshape(100, 100),
        },
        selected=(-1,),
    )

    # check dark selection
    assert dark_sel_signal_listener.callCount() == 0
    dialog._darkSelected()
    assert dark_sel_signal_listener.callCount() == 1
    assert -1 in dark_sel_signal_listener.arguments()[0][0]

    # check flat selection
    assert flat_sel_signal_listener.callCount() == 0
    dialog._flatSelected()
    assert flat_sel_signal_listener.callCount() == 1
    assert -1 in flat_sel_signal_listener.arguments()[0][0]

    # check remove selected
    dialog._removeSelected()
    assert dialog._widget.getSelectedReduceFrames() == {}

    # check clear selection
    dialog.addReduceFrames(
        {
            "reduce_frames_name": "new dict",
            -1: numpy.random.random(100 * 100).reshape(100, 100),
            2: numpy.random.random(100 * 100).reshape(100, 100),
        },
        selected=(-1, 2),
    )

    assert len(dialog._widget.getSelectedReduceFrames()) == 2
    dialog._clearSelection()
    assert len(dialog._widget.getSelectedReduceFrames()) == 0


def test_reduced_frames_filtering():
    """
    dummy test of the filter_selected_reduced_frames filter_unselected_reduced_frames function
    """
    check_reduce_frames_configuration(
        filter_selected_reduced_frames(
            (
                {
                    "reduce_frames_name": "toto frames",
                    "reduce_frames": (
                        {
                            "index": -1,  # -1 will be interpreated as at the end of the acquisition
                            "data": numpy.random.random(20 * 20).reshape(20, 20),
                            "selected": True,
                        },
                        {
                            "index": 0,
                            "data": numpy.random.random(20 * 20).reshape(20, 20),
                            "selected": True,
                        },
                    ),
                },
                {
                    "reduce_frames_name": "tata frames",
                    "reduce_frames": (
                        {
                            "index": "0.25r",
                            "data": numpy.random.random(40 * 20).reshape(40, 20),
                            "selected": False,
                        },
                    ),
                },
            )
        ),
        (
            {
                "reduce_frames_name": "toto frames",
                "reduce_frames": (
                    {
                        "index": -1,  # -1 will be interpreated as at the end of the acquisition
                        "data": numpy.random.random(20 * 20).reshape(20, 20),
                        "selected": True,
                    },
                    {
                        "index": 0,
                        "data": numpy.random.random(20 * 20).reshape(20, 20),
                        "selected": True,
                    },
                ),
            },
        ),
    )

    check_reduce_frames_configuration(
        filter_unselected_reduced_frames(
            (
                {
                    "reduce_frames_name": "toto frames",
                    "reduce_frames": (
                        {
                            "index": -1,  # -1 will be interpreated as at the end of the acquisition
                            "data": numpy.random.random(20 * 20).reshape(20, 20),
                            "selected": True,
                        },
                        {
                            "index": 0,
                            "data": numpy.random.random(20 * 20).reshape(20, 20),
                            "selected": False,
                        },
                    ),
                },
                {
                    "reduce_frames_name": "tata frames",
                    "reduce_frames": (
                        {
                            "index": "0.25r",
                            "data": numpy.random.random(40 * 20).reshape(40, 20),
                            "selected": False,
                        },
                    ),
                },
            )
        ),
        (
            {
                "reduce_frames_name": "toto frames",
                "reduce_frames": (
                    {
                        "index": 0,
                        "data": numpy.random.random(20 * 20).reshape(20, 20),
                        "selected": False,
                    },
                ),
            },
            {
                "reduce_frames_name": "tata frames",
                "reduce_frames": (
                    {
                        "index": "0.25r",
                        "data": numpy.random.random(40 * 20).reshape(40, 20),
                        "selected": False,
                    },
                ),
            },
        ),
    )

    check_reduce_frames_configuration(filter_unselected_reduced_frames(()), ())


def check_reduce_frames_configuration(config_1, config_2):
    """
    simple comparaison of two configurations
    """
    assert len(config_1) == len(config_2)
    for reduce_frame_group_1, reduce_frame_group_2 in zip(config_1, config_2):
        assert reduce_frame_group_1.get(
            "reduce_frames_name", None
        ) == reduce_frame_group_2.get("reduce_frames_name", None)

        for reduce_frame_group_1, reduce_frame_group_2 in zip(
            reduce_frame_group_1.get("reduce_frames", tuple()),
            reduce_frame_group_2.get("reduce_frames", tuple()),
        ):
            assert reduce_frame_group_1["index"] == reduce_frame_group_2["index"]
            assert reduce_frame_group_1["selected"] == reduce_frame_group_2["selected"]

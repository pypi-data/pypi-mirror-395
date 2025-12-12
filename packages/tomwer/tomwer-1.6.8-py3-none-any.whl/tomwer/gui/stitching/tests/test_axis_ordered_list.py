from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.gui.stitching.axisorderedlist import EditableOrderedTomoObjWidget


def test_axis_ordered_list_widget(
    qtapp,  # noqa F811
):
    widget = EditableOrderedTomoObjWidget(axis=0)
    volumes = tuple(
        HDF5Volume(
            file_path=f"my_volume{i}.hdf5",
            data_path="my_volume",
        )
        for i in range(5)
    )
    [widget.addTomoObj(volume) for volume in volumes]

    widget.setSelectedTomoObjs([volumes[1], volumes[-1]])
    widget._callbackRemoveSelectedTomoObj()
    assert widget.getTomoObjsAxisOrdered() == (volumes[0], volumes[2], volumes[3])

import numpy
from copy import deepcopy
from ewokscore.task import Task as EwoksTask
from tomwer.model.volume_viewer import VolumeViewerModel
from tomwer.core.volume.volumebase import TomwerVolumeBase


class VolumeViewerTask(
    EwoksTask,
    input_model=VolumeViewerModel,
    output_names=("slices", "volume_metadata", "volume_shape", "loaded_volume"),
):
    """Function loading a three slices into each direction and volume metadata and create a 'summary' of the reconstructed volume"""

    N_SLICES_PER_AXIS = 3

    def run(self):
        volume = self.inputs.volume
        assert isinstance(
            volume, TomwerVolumeBase
        ), f"volume should be an instance of {TomwerVolumeBase}. got {type(volume)}"
        if self.inputs.load_volume:
            loaded_volume = deepcopy(volume)
            loaded_volume.load_data(store=True)
            self.outputs.loaded_volume = loaded_volume
        else:
            self.outputs.loaded_volume = None
        self.outputs.slices = volume.get_slices(slices=self.get_slices_to_extract())
        self.outputs.volume_metadata = (
            self.inputs.volume.metadata or self.inputs.volume.load_metadata()
        )
        self.outputs.volume_shape = volume.get_volume_shape()

    def get_slices_to_extract(self) -> tuple[tuple[int, tuple[int]]]:
        """
        Return the indices of the slices to extract on each axis (N_SLICES_PER_AXIS on each axis).

        return tuple (A) is a two elements tuple. First element if the axis (B).
        Second is the tuple of indices to extract along the axis (B)
        indices are equally spaced in each dimensions
        """
        result: list[tuple[int, tuple[int]]] = []
        volume = self.inputs.volume
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"Volume is expected to be an instance of {TomwerVolumeBase}. Got {type(volume)}"
            )
        volume_shape = volume.get_volume_shape()
        for axis, axis_len in enumerate(volume_shape):
            for slice_index in numpy.linspace(
                0, axis_len, endpoint=False, num=self.N_SLICES_PER_AXIS + 1
            )[1:]:
                result.append((axis, numpy.round(slice_index).astype(numpy.uint16)))

        return tuple(result)

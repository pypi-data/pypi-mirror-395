from __future__ import annotations

from silx.gui import qt
from tomwer.core.volume.volumebase import TomwerVolumeBase
from weakref import ref


class SliceLoader(qt.QThread):
    """
    Thread to load a single slice from a volume.
    """

    def __init__(
        self, parent, volume: TomwerVolumeBase, slice_index: int, axis: int
    ) -> None:
        super().__init__(parent)
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError()
        self.__volume = ref(volume)
        self.slice_index = slice_index
        self.__axis = axis
        self.__data = None

    def run(self):
        if self.__volume() is None:
            return
        self.__data = self.__volume().get_slice(
            index=self.slice_index,
            axis=self.__axis,
        )

    @property
    def data(self):
        return self.__data

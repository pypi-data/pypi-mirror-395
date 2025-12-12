"""Define Interface for widget handling stitching over one axis"""

from __future__ import annotations

from silx.gui import qt


class _SingleAxisMixIn:
    """Common API for widget able to handle stitching over one axis (no matter if it is 0, 1, 2 (aka z, y, x))"""

    @property
    def first_axis(self) -> int:
        """
        Axis along which stitching is done. For stitching along z will return 0...
        """
        return self._axis

    @property
    def second_axis(self) -> int:
        """
        second axis involved in the stitching. In case of stitching along axis 0 the axis 1can also be involved (axis present in the camera reference)
        """
        if self._axis == 0:
            return 1
        elif self._axis == 1:
            return 0
        else:
            raise NotImplementedError

    @property
    def third_axis(self):
        all_axis = {(0, 1, 2)}
        all_axis.remove(self.first_axis)
        all_axis.remove(self.second_axis)
        return all_axis.pop()

    @staticmethod
    def axis_alias(axis: int):
        if axis == 0:
            return "z"
        elif axis == 1:
            return "y"
        elif axis == 2:
            return "z"
        else:
            raise ValueError(f"axis should be in (0, 1, 2). {axis} given")


class SingleAxisMetaClass(type(qt.QMainWindow), type(_SingleAxisMixIn)):
    """
    Metaclass for single axis stitcher in order to aggregate dumper class and axis
    """

    def __new__(mcls, name, bases, attrs, axis: int | None = None):
        mcls = super().__new__(mcls, name, bases, attrs)
        mcls._axis = axis  # used from _SingleAxisMixIn interface
        return mcls

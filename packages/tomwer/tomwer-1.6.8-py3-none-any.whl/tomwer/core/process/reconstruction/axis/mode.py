import logging

from enum import Enum as _Enum
from tomwer.core.process.reconstruction.axis.side import Side

_logger = logging.getLogger(__name__)


class AxisModeMetadata:
    """
    Util class to store metadata regarding processing of a mode.

    Ease processing and display
    Maybe this function should be part of nabu ?

    :param lockable: True if this value can be lock and process automatically when a new scan is received
    :param tooltip: short description of the mode (to be used by the GUI)
    :param computing_constrains: some constrain like need to have a 0-360 acquisition (so no Half acquisition)
    :param allows_padding: does the algorithm applies padding (and so can the user provide some mode)
    :param valid_inputs: compatible input type (pair of radios or sinogram...)
    :param valid_sides: can a side be provided
    :param allows_estimated_cor_as_numerical_value: can a numerical value (first guess) be provided to the algorithm
    """

    def __init__(
        self,
        lockable,
        tooltip="",
        computing_constrains=(),
        allows_padding=False,
        valid_inputs=(),
        valid_sides=(),
        allows_estimated_cor_as_numerical_value: bool = True,
    ) -> None:
        self._lockable = lockable
        self._tooltip = tooltip
        self._computing_constrains = computing_constrains
        self._allows_padding = allows_padding
        self._valid_inputs = valid_inputs
        self._valid_sides = valid_sides
        self._allows_estimated_cor_as_numerical_value = (
            allows_estimated_cor_as_numerical_value
        )

    @property
    def is_lockable(self) -> bool:
        return self._lockable

    @property
    def tooltip(self) -> str:
        return self._tooltip

    @property
    def computing_constrains(self) -> tuple:
        return self._computing_constrains

    @property
    def allows_padding(self) -> bool:
        return self._allows_padding

    @property
    def valid_inputs(self) -> tuple:
        return self._valid_inputs

    @property
    def valid_sides(self) -> tuple:
        return self._valid_sides

    @property
    def allows_estimated_cor_as_numerical_value(self) -> bool:
        return self._allows_estimated_cor_as_numerical_value


class _InputType(_Enum):
    SINOGRAM = "sinogram"
    RADIOS_X2 = "2 radios"
    COMPOSITE = "composite"


class _Constrain(_Enum):
    FULL_TURN = "full turn"


class AxisMode(_Enum):
    centered = "centered"
    global_ = "global"
    manual = "manual"
    growing_window_sinogram = "sino-growing-window"
    growing_window_radios = "growing-window"
    sliding_window_sinogram = "sino-sliding-window"
    sliding_window_radios = "sliding-window"
    sino_coarse_to_fine = "sino-coarse-to-fine"
    composite_coarse_to_fine = "composite-coarse-to-fine"
    fourier_angles = "fourier-angles"
    octave_accurate_radios = "octave-accurate"
    read = "read 'x_rotation_axis_pixel_position'"
    # alias to composite_coarse_to_fine with near mode
    near = "near"

    @classmethod
    def from_value(cls, value):
        # ensure backward compatibility with workflow defined before COR method on sinograms
        if value in ("global_", "global"):
            value = AxisMode.global_
        if value == "radio-growing-window":
            _logger.warning(
                f"Axis mode requested is '{value}'. To insure backward compatibility replace it by '{AxisMode.growing_window_radios.value}'"
            )
            value = AxisMode.growing_window_radios
        elif value == "radio-sliding-window":
            _logger.warning(
                f"Axis mode requested is '{value}'. To insure backward compatibility replace it by '{AxisMode.sliding_window_radios.value}'"
            )
            value = AxisMode.sliding_window_radios
        elif value in ("radios-octave-accurate", "accurate"):
            _logger.warning(
                f"Axis mode requested is '{value}'. To insure backward compatibility replace it by '{AxisMode.octave_accurate_radios.value}'"
            )
            value = AxisMode.octave_accurate_radios
        elif value in ("read", "read from estimated cor"):
            value = AxisMode.read

        return AxisMode(value)

    def requires_radio_indices(self) -> bool:
        return self in (
            AxisMode.growing_window_radios,
            AxisMode.sliding_window_radios,
            AxisMode.octave_accurate_radios,
        )

    def requires_sinogram_index(self) -> bool:
        return self in (
            AxisMode.growing_window_sinogram,
            AxisMode.sliding_window_sinogram,
            AxisMode.fourier_angles,
            AxisMode.sino_coarse_to_fine,
        )


AXIS_MODE_METADATAS = {
    # manual
    AxisMode.manual: AxisModeMetadata(
        lockable=False,
        tooltip="Enter or find manually the COR value",
        computing_constrains=(),
        allows_padding=False,
        valid_inputs=(_InputType.RADIOS_X2,),
        allows_estimated_cor_as_numerical_value=False,
    ),
    # read
    AxisMode.read: AxisModeMetadata(
        lockable=True,
        tooltip="Read COR value from nexus file ({entry}/instrument/detector/x_rotation_axis_pixel_position dataset). Will work only for NXtomo / hdf5 datasets",
        computing_constrains=(),
        allows_padding=False,
        valid_inputs=None,
        allows_estimated_cor_as_numerical_value=False,
    ),
    # radio algorithm
    AxisMode.centered: AxisModeMetadata(
        lockable=True,
        tooltip="Dedicated to fullfield. Previously named 'accurate'",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.RADIOS_X2,),
        valid_sides=(Side.CENTER,),
    ),
    AxisMode.global_: AxisModeMetadata(
        lockable=True,
        tooltip="Algorithm which can work for both half acquisition and standard ('full field') acquisition",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.RADIOS_X2,),
        allows_estimated_cor_as_numerical_value=False,
    ),
    AxisMode.growing_window_radios: AxisModeMetadata(
        lockable=True,
        tooltip="A auto-Cor method",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.RADIOS_X2,),
        valid_sides=(Side.RIGHT, Side.LEFT, Side.CENTER, Side.ALL),
        allows_estimated_cor_as_numerical_value=False,
    ),
    AxisMode.sliding_window_radios: AxisModeMetadata(
        lockable=True,
        tooltip="A method for estimating semi-automatically the CoR position. You have to provide a hint on where the CoR is (left, center, right).",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.RADIOS_X2,),
        valid_sides=(Side.RIGHT, Side.LEFT, Side.CENTER),
    ),
    AxisMode.octave_accurate_radios: AxisModeMetadata(
        lockable=True,
        tooltip="Same method as the 'accurate' octave code",
        computing_constrains=(_Constrain.FULL_TURN,),
        allows_padding=True,
        valid_inputs=(_InputType.RADIOS_X2,),
        valid_sides=(Side.CENTER,),
        allows_estimated_cor_as_numerical_value=False,
    ),
    # sinogram algorithm
    AxisMode.growing_window_sinogram: AxisModeMetadata(
        lockable=True,
        tooltip="A auto-Cor method",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.SINOGRAM,),
        valid_sides=(Side.RIGHT, Side.LEFT, Side.CENTER, Side.ALL),
        allows_estimated_cor_as_numerical_value=False,
    ),
    AxisMode.sliding_window_sinogram: AxisModeMetadata(
        lockable=True,
        tooltip="A method for estimating semi-automatically the CoR position. You have to provide a hint on where the CoR is (left, center, right).",
        computing_constrains=(),
        allows_padding=True,
        valid_inputs=(_InputType.SINOGRAM,),
        valid_sides=(
            Side.RIGHT,
            Side.LEFT,
            Side.CENTER,
        ),
    ),
    AxisMode.sino_coarse_to_fine: AxisModeMetadata(
        lockable=True,
        tooltip="Estimate CoR from sinogram. Only works for 360 degrees scans.",
        computing_constrains=(_Constrain.FULL_TURN,),
        allows_padding=True,
        valid_inputs=(_InputType.SINOGRAM,),
        valid_sides=(
            Side.RIGHT,
            Side.LEFT,
        ),
        allows_estimated_cor_as_numerical_value=False,
    ),
    AxisMode.fourier_angles: AxisModeMetadata(
        lockable=True,
        tooltip="",
        computing_constrains=(_Constrain.FULL_TURN,),
        allows_padding=True,
        valid_inputs=(_InputType.SINOGRAM,),
        valid_sides=(
            Side.RIGHT,
            Side.LEFT,
            Side.CENTER,
        ),
    ),
    # coarse-to-fine algorithm
    AxisMode.composite_coarse_to_fine: AxisModeMetadata(
        lockable=True,
        tooltip="A auto-Cor method",
        computing_constrains=(_Constrain.FULL_TURN,),
        allows_padding=True,
        valid_inputs=(_InputType.COMPOSITE,),
        valid_sides=(
            Side.RIGHT,
            Side.LEFT,
            Side.CENTER,
        ),
    ),
    AxisMode.near: AxisModeMetadata(
        lockable=True,
        tooltip="Alias to composite_coarse_to_fine",
        computing_constrains=(_Constrain.FULL_TURN,),
        allows_padding=True,
        valid_inputs=(_InputType.COMPOSITE,),
        valid_sides=(
            Side.RIGHT,
            Side.LEFT,
            Side.CENTER,
        ),
    ),
}

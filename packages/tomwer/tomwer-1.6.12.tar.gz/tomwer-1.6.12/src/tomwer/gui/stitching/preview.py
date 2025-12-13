from __future__ import annotations

from silx.gui import qt
from nabu.stitching.config import dict_to_config_obj
from nabu.stitching.stitcher.z_stitcher import (
    PreProcessingZStitcher,
    PostProcessingZStitcher,
)
from nabu.stitching.stitcher.y_stitcher import PreProcessingYStitcher


class PreviewThread(qt.QThread):
    """
    Thread to compute an overview of the stitching
    """

    def __init__(self, stitching_config: dict, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._stitching_config = dict_to_config_obj(stitching_config)
        self._output_identifier = None
        self._frame_composition = None
        self._final_tomo_objs_positions = None
        # store position of all the tomo objects (scan, volumes) used for the final stitching (after shift refinement)

    @property
    def stitching_config(self):
        return self._stitching_config

    @property
    def output_identifier(self):
        return self._output_identifier

    @property
    def frame_composition(self):
        return self._frame_composition

    @property
    def final_tomo_objs_positions(self) -> dict:
        """
        :return: dict with tomo object identifier (str) as key and a tuple of position in pixel (axis_0_pos, axis_1_pos, axis_2_pos)
        """
        return self._final_tomo_objs_positions

    def run(self):
        stitching_type = self.stitching_config.stitching_type
        if stitching_type.value == "z-preproc":
            stitcher = PreProcessingZStitcher(configuration=self.stitching_config)
        elif stitching_type.value == "z-postproc":
            stitcher = PostProcessingZStitcher(configuration=self.stitching_config)
        elif stitching_type.value == "y-preproc":
            stitcher = PreProcessingYStitcher(configuration=self.stitching_config)
        else:
            raise NotImplementedError
        self._output_identifier = stitcher.stitch()
        if self._output_identifier is not None:
            self._output_identifier = self._output_identifier.to_str()
        # store in cache the frame composition to be able to provide them to the PreviewPlot
        self._frame_composition = stitcher.frame_composition
        self._final_tomo_objs_positions = stitcher.get_final_axis_positions_in_px()

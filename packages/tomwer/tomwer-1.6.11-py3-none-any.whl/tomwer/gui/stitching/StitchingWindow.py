from __future__ import annotations

import logging
import os
import shutil
import tempfile
import functools

from nabu.stitching.config import StitchingType
from nabu.pipeline.config import generate_nabu_configfile, parse_nabu_config_file
from nabu.stitching.config import (
    get_default_stitching_config,
    SECTIONS_COMMENTS as _SECTIONS_COMMENTS,
)

from silx.gui import qt

from tomwer.core.scan.nxtomoscan import NXtomoScan, NXtomoScanIdentifier
from tomwer.core.volume.hdf5volume import HDF5Volume, HDF5VolumeIdentifier
from tomwer.gui.qconfigfile import QConfigFileDialog
from tomwer.gui.stitching.config.positionoveraxis import PosEditorOverOneAxis
from tomwer.gui.stitching.config.output import StitchingOutput
from tomwer.gui.stitching.StitchingOptionsWidget import StitchingOptionsWidget
from tomwer.gui.configuration.action import (
    BasicConfigurationAction,
    ExpertConfigurationAction,
    MinimalisticConfigurationAction,
)
from tomwer.gui.configuration.level import ConfigurationLevel
from tomwer.gui.stitching import action as stitching_action
from tomwer.gui.stitching.preview import PreviewThread
from tomwer.gui.stitching.singleaxis import SingleAxisMetaClass, _SingleAxisMixIn
from tomwer.gui.stitching.SingleAxisStitchingWidget import SingleAxisStitchingWidget

from .utils import concatenate_dict

_logger = logging.getLogger(__name__)


class _SingleAxisStitchingWindow(
    qt.QMainWindow, _SingleAxisMixIn, metaclass=SingleAxisMetaClass
):
    """
    Main widget containing all the options to define the stitching to be done

    :param with_configuration_action: if True append the load and save stitching configuration tool button.
                                           In some cases those can also be part of Menu so we want to avoid having those twice
    """

    sigChanged = qt.Signal()
    """Signal emit each time the configuration is modified"""

    def __init__(self, parent=None, with_configuration_action=True) -> None:
        super().__init__(parent)
        assert self._axis in (0, 1, 2)
        """axis along which we want to apply stitching"""
        self._previewFolder = None
        # folder to store files (volume or NXtomo) for previews
        self._previewThread = None
        # thread to compute the stitching for preview
        self._callbackToGetSlurmConfig = None
        self._callbackToSetSlurmConfig = None
        # convenient work around to avoid having to redefine the n=interface for slurm and the API
        # to load and save settings
        # if it is defined upper

        toolbar = qt.QToolBar(self)
        self.addToolBar(qt.Qt.TopToolBarArea, toolbar)
        style = qt.QApplication.instance().style()

        # clean option
        self.__cleanAction = qt.QAction(self)
        self.__cleanAction.setToolTip("clear")
        clear_icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        self.__cleanAction.setIcon(clear_icon)
        toolbar.addAction(self.__cleanAction)
        self.__cleanAction.triggered.connect(self.clean)

        # separator
        toolbar.addSeparator()

        if with_configuration_action:
            # load action
            self.__loadAction = stitching_action.LoadConfigurationAction(self)
            toolbar.addAction(self.__loadAction)
            self.__loadAction.triggered.connect(
                functools.partial(self._loadSettings, file_path=None)
            )

            # save action
            self.__saveAction = stitching_action.SaveConfigurationAction(self)
            toolbar.addAction(self.__saveAction)
            self.__saveAction.triggered.connect(
                functools.partial(self._saveSettings, file_path=None)
            )

            # separator
            toolbar.addSeparator()

        # update preview action
        self.__updatePreviewAction = stitching_action.PreviewAction(self)
        toolbar.addAction(self.__updatePreviewAction)
        self.__updatePreviewAction.triggered.connect(self._trigger_update_preview)

        # separator
        toolbar.addSeparator()

        # configuration level / mode
        self.__configurationModesAction = qt.QAction(self)
        self.__configurationModesAction.setCheckable(False)
        menu = qt.QMenu(self)
        self.__configurationModesAction.setMenu(menu)
        toolbar.addAction(self.__configurationModesAction)

        self.__configurationModesGroup = qt.QActionGroup(self)
        self.__configurationModesGroup.setExclusive(True)
        self.__configurationModesGroup.triggered.connect(self._userModeChanged)

        self._minimalisticAction = MinimalisticConfigurationAction(toolbar)
        menu.addAction(self._minimalisticAction)
        self.__configurationModesGroup.addAction(self._minimalisticAction)
        self._basicConfigAction = BasicConfigurationAction(toolbar)
        menu.addAction(self._basicConfigAction)
        self.__configurationModesGroup.addAction(self._basicConfigAction)
        self._expertConfiguration = ExpertConfigurationAction(toolbar)
        menu.addAction(self._expertConfiguration)
        self.__configurationModesGroup.addAction(self._expertConfiguration)

        # separator
        toolbar.addSeparator()

        # create central widget
        self._widget = SingleAxisStitchingWidget(parent=self, axis=self.first_axis)
        self.setCentralWidget(self._widget)

        # create Dock widgets
        ##  output
        self._outputWidget = StitchingOutput(parent=self)
        self._outputWidget.setObjectName("outputSettingsWidget")
        self._outputDockWidget = qt.QDockWidget(parent=self)
        self._outputDockWidget.setWindowTitle("output")
        self._outputDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._outputDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._outputDockWidget.setWidget(self._outputWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._outputDockWidget)
        self._outputDockWidget.setToolTip(
            "options to where and how to save the stitching"
        )
        ##  stitching strategies
        self._stitchingOptsWidget = StitchingOptionsWidget(
            parent=self, first_axis=self.first_axis, second_axis=self.second_axis
        )
        self._stitchingOptsScrollArea = qt.QScrollArea(self)
        self._stitchingOptsScrollArea.setWidget(self._stitchingOptsWidget)
        self._stitchingOptsScrollArea.setWidgetResizable(True)
        self._stitchingOptsScrollArea.setHorizontalScrollBarPolicy(
            qt.Qt.ScrollBarAlwaysOff
        )
        self._stitchingOptsDockWidget = qt.QDockWidget(parent=self)
        self._stitchingOptsDockWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._stitchingOptsDockWidget.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._stitchingOptsDockWidget.setWidget(self._stitchingOptsScrollArea)
        self._stitchingOptsDockWidget.setWindowTitle("processing options")
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._stitchingOptsDockWidget)

        ## all scan z positions
        self._editTomoObjFirstAxisPositionsWidget = PosEditorOverOneAxis(
            parent=self,
            axis_edited=self.first_axis,
            axis_order=self.first_axis,
        )
        self._editTomoObjFirstAxisPositionsDockWidget = qt.QDockWidget(parent=self)
        self._editTomoObjFirstAxisPositionsDockWidget.layout().setContentsMargins(
            0, 0, 0, 0
        )
        self._editTomoObjFirstAxisPositionsDockWidget.setFeatures(
            qt.QDockWidget.DockWidgetMovable
        )
        self._editTomoObjFirstAxisPositionsDockWidget.setWidget(
            self._editTomoObjFirstAxisPositionsWidget
        )
        self._editTomoObjFirstAxisPositionsDockWidget.setWindowTitle(
            f"edit positions over axis {self.first_axis} (px) - aka {self.axis_alias(self.first_axis)}"
        )
        self._editTomoObjFirstAxisPositionsDockWidget.setToolTip(
            f"This allows to edit tomo objects positions along the axis {self.first_axis} (aka {self.axis_alias(self.first_axis)})"
        )
        self.addDockWidget(
            qt.Qt.RightDockWidgetArea, self._editTomoObjFirstAxisPositionsDockWidget
        )
        ### add a check box to update position from preview if asked by the user
        self._updateFirstAxisPosFromPreviewCalc = qt.QCheckBox(
            f"update position {self.first_axis} from preview calc",
            self,
        )
        self._updateFirstAxisPosFromPreviewCalc.setToolTip(
            f"When the user trigger a preview, if some shift search refined over axis {self.first_axis} is done then will update the axis 0 positions",
        )
        self._updateFirstAxisPosFromPreviewCalc.setChecked(True)
        self._editTomoObjFirstAxisPositionsWidget.layout().insertWidget(
            0, self._updateFirstAxisPosFromPreviewCalc
        )

        ## all scan axis 1 positions
        self._editTomoObjSecondAxisPositionsWidget = PosEditorOverOneAxis(
            parent=self,
            axis_edited=self.second_axis,
            axis_order=0,
        )
        self._editTomoObjSecondAxisPositionsDockWidget = qt.QDockWidget(parent=self)
        self._editTomoObjSecondAxisPositionsDockWidget.layout().setContentsMargins(
            0, 0, 0, 0
        )
        self._editTomoObjSecondAxisPositionsDockWidget.setFeatures(
            qt.QDockWidget.DockWidgetMovable
        )
        self._editTomoObjSecondAxisPositionsDockWidget.setWidget(
            self._editTomoObjSecondAxisPositionsWidget
        )
        self._editTomoObjSecondAxisPositionsDockWidget.setWindowTitle(
            f"edit positions over axis {self.second_axis} (px)"
        )
        self._editTomoObjSecondAxisPositionsDockWidget.setToolTip(
            f"This allows to edit tomo objects positions along the axis {self.second_axis}"
        )
        self.addDockWidget(
            qt.Qt.RightDockWidgetArea, self._editTomoObjSecondAxisPositionsDockWidget
        )
        ### add a check box to update position from preview if asked by the user
        self._updateSecondAxisPosFromPreviewCalc = qt.QCheckBox(
            f"update position {self.second_axis} from preview calc", self
        )
        self._updateSecondAxisPosFromPreviewCalc.setToolTip(
            f"When the user trigger a preview, if some position refinement can be done will update axis {self.second_axis}"
        )
        self._updateSecondAxisPosFromPreviewCalc.setChecked(True)
        self._editTomoObjSecondAxisPositionsWidget.layout().insertWidget(
            0, self._updateSecondAxisPosFromPreviewCalc
        )

        self._widget.setAddTomoObjCallbacks(
            (
                self._editTomoObjFirstAxisPositionsWidget.addTomoObj,
                self._editTomoObjSecondAxisPositionsWidget.addTomoObj,
                self.getRawDisplayPlot().addTomoObj,
            )
        )
        self._widget.setRemoveTomoObjCallbacks(
            (
                self._editTomoObjFirstAxisPositionsWidget.removeTomoObj,
                self._editTomoObjSecondAxisPositionsWidget.removeTomoObj,
                self.getRawDisplayPlot().removeTomoObj,
            )
        )

        # update layout: for now lets tabify some widget
        self.tabifyDockWidget(self._outputDockWidget, self._stitchingOptsDockWidget)
        self.tabifyDockWidget(
            self._outputDockWidget, self._editTomoObjSecondAxisPositionsDockWidget
        )
        self.tabifyDockWidget(
            self._outputDockWidget, self._editTomoObjFirstAxisPositionsDockWidget
        )

        # handle raw display plot. By display avoid displaying raw data as this can be resource consuming
        self._widget._mainWidget._rawDisplayCB.setChecked(False)
        self._widget._mainWidget._rawDisplayPlot.setActive(False)

        # connect signal / slot
        self._widget._mainWidget._rawDisplayCB.toggled.connect(
            self._handleRawDisplayConnection
        )
        self._outputWidget.sigChanged.connect(self._changed)
        self._stitchingOptsWidget.sigChanged.connect(self._changed)
        self._widget.sigStitchingTypeChanged.connect(
            self._outputWidget._updateOutputForStitchingType
        )
        self._widget.sigStitchingTypeChanged.connect(
            self._stitchingOptsWidget._stitchingTypeChanged
        )

        ## handle raw plot preview
        self._stitchingOptsWidget.sigFlipLRChanged.connect(
            self.getRawDisplayPlot().setFlipLRFrames
        )
        self._stitchingOptsWidget.sigFlipUDChanged.connect(
            self.getRawDisplayPlot().setFlipUDFrames
        )
        self._stitchingOptsWidget.sigSliceForPreviewChanged.connect(
            self.getRawDisplayPlot().setSliceForPreview
        )

        ## handle tomo obj loading from settings
        self._widget.sigTomoObjsLoaded.connect(
            self._editTomoObjFirstAxisPositionsWidget.setTomoObjs
        )
        self._widget.sigTomoObjsLoaded.connect(
            self._editTomoObjSecondAxisPositionsWidget.setTomoObjs
        )
        self._widget.sigTomoObjsLoaded.connect(self.getRawDisplayPlot().setTomoObjs)

        # set up
        self._basicConfigAction.setChecked(True)
        self._userModeChanged(self._basicConfigAction)

    def setCallbackToGetSlurmConfig(self, callback):
        self._callbackToGetSlurmConfig = callback

    def setCallbackToSetSlurmConfig(self, callback):
        self._callbackToSetSlurmConfig = callback

    def close(self):
        # remove folder used for preview
        if self._previewFolder is not None:
            shutil.rmtree(self._previewFolder, ignore_errors=True)
        self._widget.close()
        # requested for the waiting plot update
        super().close()

    def getRawDisplayPlot(self):
        return self._widget._mainWidget._rawDisplayPlot

    def _handleRawDisplayConnection(self, toggled: bool):
        raw_display_plot = self.getRawDisplayPlot()
        raw_display_plot.setActive(toggled)

    def getPreviewAction(self):
        return self.__updatePreviewAction

    def getPreviewFolder(self):
        if self._previewFolder is None:
            self._previewFolder = tempfile.mkdtemp(prefix="tomwer_stitcher_preview")
        return self._previewFolder

    def getVolumeIdentifierPreview(self) -> HDF5VolumeIdentifier:
        folder = self.getPreviewFolder()
        # for now use hdf5 by default
        return HDF5VolumeIdentifier(
            object=HDF5Volume,
            hdf5_file=os.path.join(folder, "vol_stitching_preview.hdf5"),
            entry="my_volume",
        )

    def getNXtomoIdentifierForPreview(self):
        folder = self.getPreviewFolder()
        return NXtomoScanIdentifier(
            object=NXtomoScan,
            hdf5_file=os.path.join(folder, "nxtomo_stiching_preview.hdf5"),
            entry="entry0000",
        )

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def _saveSettings(self, file_path=None, **kwargs):
        """
        dump current configuration into a txt file
        """
        # get a file if necessary
        if file_path is None:
            dialog = QConfigFileDialog(self)
            dialog.setAcceptMode(qt.QFileDialog.AcceptSave)
            if not dialog.exec():
                return

            selected_file = dialog.selectedFiles()
            if len(selected_file) == 0:
                return
            file_path = selected_file[0]

        configuration = self.getConfiguration()
        if self._callbackToGetSlurmConfig is not None:
            slurm_config = {"slurm": self._callbackToGetSlurmConfig()}
            configuration = concatenate_dict(configuration, slurm_config)

        _, ext = os.path.splitext(file_path)
        if ext == "":
            file_path = f"{file_path}.cfg"
        # dump configuration
        generate_nabu_configfile(
            fname=file_path,
            default_config=get_default_stitching_config(self.getStitchingType()),
            comments=True,
            sections_comments=_SECTIONS_COMMENTS,
            options_level="advanced",
            prefilled_values=configuration,
        )

    def _loadSettings(self, file_path=None, **kwargs):
        """
        load configuration from a txt file
        """
        # get a file if necessary
        if file_path is None:
            dialog = QConfigFileDialog(self)
            dialog.setAcceptMode(qt.QFileDialog.AcceptOpen)
            dialog.setFileMode(qt.QFileDialog.ExistingFiles)

            if not dialog.exec():
                return

            selected_file = dialog.selectedFiles()
            if len(selected_file) == 0:
                return
            file_path = selected_file[0]

        # Do configuration load
        conf_dict = parse_nabu_config_file(file_path, allow_no_value=True)
        self.setConfiguration(config=conf_dict)
        if self._callbackToSetSlurmConfig is not None:
            self._callbackToSetSlurmConfig(conf_dict.get("slurm", {}))

    def _trigger_update_preview(self):
        if self._previewThread is not None:
            _logger.warning(
                "some preview is already running. Please wait before relaunching it"
            )
            return
        config = self.getConfiguration()
        # update the output file to set if from raw...
        stitching_type = config.get("stitching", {}).get("type", None)
        if stitching_type in ("z-preproc", "y-preproc"):
            output_identifier = self.getNXtomoIdentifierForPreview()
            config["preproc"]["location"] = output_identifier.file_path
            config["preproc"]["data_path"] = output_identifier.data_path
            assert "postproc" not in config
        elif stitching_type == "z-postproc":
            config["postproc"][
                "output_volume"
            ] = self.getVolumeIdentifierPreview().to_str()
            assert "preproc" not in config
        else:
            raise NotImplementedError

        # update the slice to avoid doing the stitching on all the frames
        config["inputs"]["slices"] = self.getSlicesForPreview()

        # update to force overwrite
        config["output"]["overwrite_results"] = True

        # avoid any recalculation of the axis position. So the preview is accurate
        config["output"]["axis_0_params"] = ""
        config["output"]["axis_1_params"] = ""
        config["output"]["axis_2_params"] = ""

        # clean current preview to notify some calculation is going on
        preview_plot = self._widget._mainWidget._previewPlot
        preview_plot._waitingOverlay.show()

        # start stitching on a thread
        self._previewThread = PreviewThread(stitching_config=config)
        self._previewThread.finished.connect(self._previewCalculationFinished)
        self._previewThread.start()

    def getSlicesForPreview(self):
        return self._stitchingOptsWidget.getSlicesForPreview()

    def _previewCalculationFinished(self):
        sender = self.sender()
        assert isinstance(sender, PreviewThread)
        composition = sender.frame_composition
        tomo_objs_new_axis_positions = sender.final_tomo_objs_positions
        assert isinstance(
            tomo_objs_new_axis_positions, dict
        ), f"final_tomo_objs_positions is expected to be a dict with obj identifier as key and the tuple of position as value. Got {type(tomo_objs_new_axis_positions)}"
        # expect it to be a dict with tomo obj identifier as key and a tuple of (axis_2_pos, axis_1_pos, axis_0_pos) as value
        output_obj_identifier = sender.output_identifier

        preview_plot = self._widget._mainWidget._previewPlot
        preview_plot._waitingOverlay.hide()

        self._previewThread.finished.disconnect(self._previewCalculationFinished)
        self._previewThread = None

        if output_obj_identifier is None:
            _logger.error("preview of stitching failed")
        else:
            preview_plot.setStitchedTomoObj(
                tomo_obj_id=output_obj_identifier,
                composition=composition,
            )

        # update object values if requested
        update_requested = {
            self.first_axis: self._updateFirstAxisPosFromPreviewCalc.isChecked(),
            self.second_axis: self._updateSecondAxisPosFromPreviewCalc.isChecked(),
        }

        if update_requested[self.first_axis] or update_requested[self.second_axis]:
            existing_tomo_obj = {
                tomo_obj.get_identifier().to_str(): tomo_obj
                for tomo_obj in self._widget._mainWidget.getTomoObjs()
            }

            for tomo_obj_id, value in tomo_objs_new_axis_positions.items():
                assert (
                    isinstance(value, tuple) and len(value) == 3
                ), "value is expected to be (new_pos_axis_0, new_pos_axis_1, new_pos_axis_2)"
                new_first_axis_pos = value[self.first_axis]
                new_second_axis_pos = value[self.second_axis]
                tomo_obj = existing_tomo_obj.get(tomo_obj_id, None)
                if tomo_obj is None:
                    continue

                if update_requested[self.first_axis]:
                    tomo_obj.stitching_metadata.setPxPos(
                        int(new_first_axis_pos), self.first_axis
                    )
                if update_requested[self.second_axis]:
                    tomo_obj.stitching_metadata.setPxPos(
                        int(new_second_axis_pos), self.second_axis
                    )
            if update_requested[self.first_axis]:
                self._editTomoObjFirstAxisPositionsWidget._orderedMightHaveChanged(
                    force_sb_update=True
                )
            if update_requested[self.second_axis]:
                self._editTomoObjSecondAxisPositionsWidget._orderedMightHaveChanged(
                    force_sb_update=True
                )

    def clean(self):
        self._widget.clean()
        self._editTomoObjFirstAxisPositionsWidget.clean()
        self._editTomoObjSecondAxisPositionsWidget.clean()

    def setSeries(self, series):
        self.clean()
        self._widget._mainWidget.setSeries(series)
        self._editTomoObjFirstAxisPositionsWidget.clean()
        self._editTomoObjSecondAxisPositionsWidget.clean()
        for tomo_obj in series:
            self._editTomoObjFirstAxisPositionsWidget.addTomoObj(tomo_obj)
            self._editTomoObjSecondAxisPositionsWidget.addTomoObj(tomo_obj)
        self.getRawDisplayPlot().setTomoObjs(tomo_objs=series[:])

    def addTomoObj(self, tomo_obj):
        self._widget.addTomoObj(tomo_obj)
        self._editTomoObjFirstAxisPositionsWidget.addTomoObj(tomo_obj)
        self._editTomoObjSecondAxisPositionsWidget.addTomoObj(tomo_obj)
        self.getRawDisplayPlot().addTomoObj(tomo_obj=tomo_obj)

    def getTomoObjs(self) -> tuple:
        return self._widget.getTomoObjs()

    def removeTomoObj(self, tomo_obj):
        self._widget.removeTomoObj(tomo_obj)
        self.getRawDisplayPlot().removeTomoObj(tomo_obj=tomo_obj)

    def getConfiguration(self) -> dict:
        # make sure the sync is fine between the two
        configs = (
            self._widget.getConfiguration(),
            self._outputWidget.getConfiguration(),
            self._stitchingOptsWidget.getConfiguration(),
        )
        result = {}
        for config in configs:
            result = concatenate_dict(result, config)
        return result

    def setConfiguration(self, config: dict):
        self._widget.setConfiguration(config)
        self._outputWidget.setConfiguration(config)
        self._stitchingOptsWidget.setConfiguration(config)

    # expose API
    def getStitchingType(self) -> StitchingType:
        return self._widget.getStitchingType()

    def setStitchingType(self, stitching_type: StitchingType):
        self._widget.setStitchingType(stitching_type)

    def _userModeChanged(self, action):
        self.__configurationModesAction.setIcon(action.icon())
        self.__configurationModesAction.setToolTip(action.tooltip())
        if action is self._basicConfigAction:
            level = ConfigurationLevel.OPTIONAL
        elif action is self._expertConfiguration:
            level = ConfigurationLevel.ADVANCED
        else:
            level = ConfigurationLevel.REQUIRED
        self._stitchingOptsWidget.setConfigurationLevel(level)
        self._editTomoObjSecondAxisPositionsDockWidget.setVisible(
            level >= ConfigurationLevel.ADVANCED
        )

    def setPreProcessingOutput(self, *args, **kwargs):
        self._outputWidget.setPreProcessingOutput(*args, **kwargs)

    def setPostProcessingOutput(self, *args, **kwargs):
        self._outputWidget.setPostProcessingOutput(*args, **kwargs)

    def get_available_pre_processing_stitching_mode(self):
        return self._widget.get_available_pre_processing_stitching_mode()

    def get_available_post_processing_stitching_mode(self):
        return self._widget.get_available_post_processing_stitching_mode()


class YStitchingWindow(_SingleAxisStitchingWindow, axis=1):
    pass


class ZStitchingWindow(_SingleAxisStitchingWindow, axis=0):
    pass

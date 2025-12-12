import logging

from nabu.resources.nxflatfield import update_dataset_info_flats_darks
from nabu.resources.dataset_analyzer import HDF5DatasetAnalyzer
from nabu.io.reader import load_images_from_dataurl_dict
from nabu.app.prepare_weights_double import create_heli_maps

from tomwer.core.process.task import TaskWithProgress
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.scanutils import format_output_location


_logger = logging.getLogger(__name__)


class NabuHelicalPrepareWeightsDouble(
    TaskWithProgress,
    input_names=(
        "data",
        "transition_width_vertical",
        "transition_width_horizontal",
        "processes_file",
        "rotation_axis_position",
    ),
    optional_input_names=("progress",),
    output_names=("data",),
):
    def run(self):
        # TODO: handle future /cluster config ???
        scan = self.inputs.data
        if not isinstance(scan, NXtomoScan):
            raise TypeError(f"data is expected to be an instance of {NXtomoScan}")
        dataset_info = HDF5DatasetAnalyzer(
            scan.master_file,
            extra_options={"h5_entry": scan.entry},
        )
        update_dataset_info_flats_darks(
            dataset_info, flatfield_mode=1, loading_mode="load_if_present"
        )

        mappe = 0
        my_flats = load_images_from_dataurl_dict(dataset_info.flats)

        for _, flat in my_flats.items():
            mappe += flat
        mappe = mappe / len(list(dataset_info.flats.keys()))

        scan.helical.processes_files = format_output_location(
            location=self.inputs.processes_file, scan=scan
        )
        create_heli_maps(
            profile=mappe,
            process_file_name=scan.helical.processes_files,
            entry_name=scan.entry,
            transition_width_vertical=self.inputs.transition_width_vertical,
            transition_width_horizontal=self.inputs.transition_width_horizontal,
            rotation_axis_position=self.inputs.rotation_axis_position,
        )

        self.outputs.data = scan

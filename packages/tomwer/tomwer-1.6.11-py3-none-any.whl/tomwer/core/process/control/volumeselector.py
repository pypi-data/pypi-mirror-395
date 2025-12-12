from ewokscore.task import Task as EwoksTask

from tomwer.core.utils.scanutils import data_identifier_to_scan


class _VolumeSelectorPlaceHolder(
    EwoksTask, input_names=["volume"], output_names=["volume"]
):
    """
    task to select a volume or a set of volumes
    """

    def run(self):
        self.outputs.volume = data_identifier_to_scan(self.inputs.volume)

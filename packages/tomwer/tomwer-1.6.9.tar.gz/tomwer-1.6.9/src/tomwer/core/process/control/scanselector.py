from ewokscore.task import Task as EwoksTask

from tomwer.core.utils.scanutils import data_identifier_to_scan


class _ScanSelectorPlaceHolder(EwoksTask, input_names=["data"], output_names=["data"]):
    """
    task to select one or several scan / data to be processed
    """

    def run(self):
        self.outputs.data = data_identifier_to_scan(self.inputs.data)

from tomwer.core.process.task import Task
from tomwer.core.utils.scanutils import data_identifier_to_scan


class SingleTomoObjProcess(
    Task, optional_input_names=("tomo_obj",), output_names=("tomo_obj",)
):
    """For now data can only be a single element and not a list.
    This must be looked at.
    Also when part of an ewoks graph 'data' is mandatory which is not the class
    when part of a orange workflow. Those can be added interactively"""

    def run(self):
        self.outputs.tomo_obj = data_identifier_to_scan(self.inputs.tomo_obj)

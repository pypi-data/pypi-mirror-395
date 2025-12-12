from ewokscore.task import Task as EwoksTask


class _TomoobjseriesPlaceHolder(
    EwoksTask, input_names=["series"], output_names=["series"]
):
    """
    task to define a tomography 'serie'
    """

    def run(self):
        self.outputs.s = self.inputs.series

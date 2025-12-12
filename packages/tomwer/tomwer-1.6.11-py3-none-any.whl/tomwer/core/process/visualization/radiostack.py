# coding: utf-8


from ewokscore.task import Task as EwoksTask


class _RadioStackPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to aggregate radios of several scans and allow to browse along them all
    """

    def run(self):
        pass

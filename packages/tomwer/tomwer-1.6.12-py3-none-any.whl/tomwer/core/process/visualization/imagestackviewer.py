# coding: utf-8


from ewokscore.task import Task as EwoksTask


class _ImageStackViewerPlaceHolder(EwoksTask, input_names=("data",)):
    """
    Task to aggregate several images
    """

    def run(self):
        pass

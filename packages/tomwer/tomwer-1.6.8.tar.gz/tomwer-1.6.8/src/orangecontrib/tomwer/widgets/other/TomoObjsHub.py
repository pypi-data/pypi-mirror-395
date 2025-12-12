from orangewidget import widget
from tomwer.core.tomwer_object import TomwerObject
from orangewidget.widget import Input, Output


class TomoObjsHubOW(widget.OWBaseWidget, openclass=True):
    name = "Tomo objs hub"
    description = "takes a list of tomo_obj in entry and trigger a tomo_obj scalar for each element in downstream"
    icon = "icons/hub.svg"
    priority = 4000
    keywords = ["hub", "tomo-obj", "tomobj"]

    want_basic_layout = False
    want_control_area = False
    want_main_area = False

    class Inputs:
        tomo_objs = Input("tomo_objs", tuple, default=True, multiple=True)

    class Outputs:
        tomo_objs = Output("tomo_obj", TomwerObject)

    @Inputs.tomo_objs
    def execute(self, tomo_objs, *args, **kwargs):
        if tomo_objs is None:
            return
        for tomo_obj in tomo_objs:
            self.Outputs.tomo_objs.send(tomo_obj)

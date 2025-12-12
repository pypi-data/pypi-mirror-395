import platform
import os
import string

from processview.core.manager import ProcessManager

try:
    from ewoksnotify.tasks.email import EmailTask
except ImportError:
    has_ewoksnotify = False
else:
    has_ewoksnotify = True

from tomwer.core.process.task import Task
from tomwer.core.tomwer_object import TomwerObject
from tomwer.core.scan.scanbase import TomwerScanBase
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.hdf5volume import HDF5Volume

from datetime import datetime
from tomwer.version import version as __version


class TomoEmailTask(
    Task,
    input_names=("tomo_obj", "configuration"),
    output_names=("tomo_obj",),
):
    """Dedicated task for tomography and gui approach"""

    def __init__(
        self, varinfo=None, inputs=None, node_id=None, node_attrs=None, execinfo=None
    ):
        super().__init__(varinfo, inputs, node_id, node_attrs, execinfo)
        if not has_ewoksnotify:
            raise ImportError(
                "ewoksnotify not install but required. Please run 'pip install ewoksnotify[full]'"
            )

    def run(self):
        tomo_obj = self.inputs.tomo_obj
        configuration = self.inputs.configuration
        configuration["text"] = format_email_info(
            configuration.get("text", ""), tomo_obj=tomo_obj
        )
        configuration["subject"] = format_email_info(
            configuration.get("subject", ""), tomo_obj=tomo_obj
        )
        task = EmailTask(inputs=configuration)
        task.run()
        self.outputs.tomo_obj = self.inputs.tomo_obj


def _ls_tomo_obj(tomo_obj) -> tuple:
    """
    list information regarding a tomo obj
    """
    if isinstance(tomo_obj, TomwerScanBase):
        # for tomoscan base use the `path` attribut
        file_path_to_list = tomo_obj.path
    elif isinstance(tomo_obj, TomwerVolumeBase):
        if isinstance(tomo_obj, HDF5Volume):
            file_path_to_list = os.path.dirname(tomo_obj.url.file_path())
        else:
            file_path_to_list = tomo_obj.url.file_path()
    else:
        raise TypeError

    def get_size(file_path, decimal_places=2) -> str:
        size = os.path.getsize(file_path)
        for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB"):
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

    return tuple(
        [
            f"{get_size(os.path.join(file_path_to_list, file_path))} - {file_path}"
            for file_path in os.listdir(file_path_to_list)
        ]
    )


def _ls_dataset_state(tomo_obj) -> str:
    """
    list the status of all met processes by the tomo_obj
    """
    states = {}
    for process in ProcessManager().get_processes():
        state = ProcessManager().get_dataset_state(
            dataset_id=tomo_obj.get_identifier(),
            process=process,
        )
        if state is not None:
            states[process] = state

    return "\n".join(
        [f"* {process.name}: {state.value}" for process, state in states.items()]
    )


def format_email_info(my_str: str, tomo_obj: TomwerObject) -> str:
    """
    format `my_str` string. It can contain one of the following keyword:

    - {tomo_obj_short_id}: tomo_obj 'short id' (calling identifier.short_description)
    - {tomo_obj_id}: tomo_obj id
    - {ls_tomo_obj}: ls of the scan folder
    - {timestamp}: current time
    - {footnote}: some footnote defined by tomwer
    - {dataset_processing_states}: list the status of all met processing
    """

    keywords = {
        "tomo_obj_short_id": tomo_obj.get_identifier().short_description(),
        "tomo_obj_id": tomo_obj.get_identifier().to_str(),
        "ls_tomo_obj": "\n".join(_ls_tomo_obj(tomo_obj)),
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "footnote": f"email send by tomwer - {__version} from {platform.node()}",
        "dataset_processing_states": _ls_dataset_state(tomo_obj),
    }

    # filter necessary keywords
    def get_necessary_keywords():
        formatter = string.Formatter()
        return [field for _, field, _, _ in formatter.parse(my_str) if field]

    requested_keywords = get_necessary_keywords()

    def keyword_needed(pair):
        keyword, _ = pair
        return keyword in requested_keywords

    keywords = dict(filter(keyword_needed, keywords.items()))
    return my_str.format(**keywords)

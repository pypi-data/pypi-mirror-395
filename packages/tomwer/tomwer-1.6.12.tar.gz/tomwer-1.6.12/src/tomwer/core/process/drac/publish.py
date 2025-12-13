from __future__ import annotations
import logging

from tomwer.core.process.task import Task
from tomwer.core.process.drac.dracbase import DracDatasetBase

from processview.core.manager import DatasetState, ProcessManager

try:
    from pyicat_plus.client.main import IcatClient  # noqa F401
except ImportError:
    has_pyicat_plus = False
else:
    has_pyicat_plus = True

_logger = logging.getLogger(__name__)

__all__ = [
    "PublishICatDatasetTask",
]


class PublishICatDatasetTask(
    Task,
    input_names=(
        "data_portal_processed_datasets",
        "beamline",
        "proposal",
        "dataset",
    ),
    optional_input_names=(
        "dry_run",
        "__process__",
    ),
):
    """
    publish a list of 'IcatDataBase' instances.

    `IcatDataBase` provide API to retrieve data and metadata to be publish

    input field:
    * data_portal_processed_datasets: list of 'DracDatasetBase' instances.
    * beamline: name of the beamline (bm05, id19...)
    * proposal: proposal name
    """

    def run(self):
        for icat_data in self.inputs.data_portal_processed_datasets:
            if not isinstance(icat_data, DracDatasetBase):
                raise TypeError(f"icat_data should be an instance of {DracDatasetBase}")

            # build gallery (if needed by the icat data)

            process = self.get_input_value("__process__", None)

            if process is not None and icat_data.tomo_obj is not None:
                ProcessManager().notify_dataset_state(
                    dataset=icat_data.tomo_obj,
                    process=process(),
                    state=DatasetState.ON_GOING,
                )

            icat_data.build_gallery()

            try:
                self.publish_to_data_portal(
                    path=icat_data.data_dir,
                    metadata=icat_data.metadata,
                    raw=icat_data.bliss_raw_datasets,
                    dataset=icat_data.dataset_name,
                )

            except Exception as e:
                if process is not None and icat_data.tomo_obj is not None:
                    ProcessManager().notify_dataset_state(
                        dataset=icat_data.tomo_obj,
                        process=process(),
                        state=DatasetState.FAILED,
                    )
                    raise e
            else:
                if process is not None and icat_data.tomo_obj is not None:
                    ProcessManager().notify_dataset_state(
                        dataset=icat_data.tomo_obj,
                        process=process(),
                        state=DatasetState.SUCCEED,
                    )

    def publish_to_data_portal(self, path: str, metadata: dict, raw: str, dataset: str):
        """publish path to data_portal (drac) with given metadata"""
        if not self.inputs.dry_run:
            if not has_pyicat_plus:
                raise RuntimeError(
                    "pyicat_plus not installed it. Please install it to be able to publish dataset to icat"
                )
            icat_client = IcatClient(
                metadata_urls=("bcu-mq-01.esrf.fr:61613", "bcu-mq-02.esrf.fr:61613")
            )

            _logger.info(
                "publish to icat: %s",
                {
                    "path": path,
                    "beamline": self.inputs.beamline,
                    "proposal": self.inputs.proposal,
                    "raw": raw,
                    "dataset": dataset,
                    "metadata": metadata,
                },
            )
            icat_client.store_processed_data(
                beamline=self.inputs.beamline,
                proposal=self.inputs.proposal,
                dataset=dataset,
                path=path,
                metadata=metadata,
                raw=raw,
            )

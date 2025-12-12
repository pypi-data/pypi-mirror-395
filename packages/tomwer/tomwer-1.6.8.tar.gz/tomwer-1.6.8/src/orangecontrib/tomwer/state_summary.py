from orangewidget.utils.signals import PartialSummary, summarize

from tomwer.core.cluster import SlurmClusterConfiguration
from tomwer.core.futureobject import FutureTomwerObject
from tomwer.core.scan.blissscan import BlissScan
from tomwer.core.scan.scanbase import TomwerScanBase


@summarize.register(object)  # noqa F811
def summarize_(Object: object):  # noqa F811
    return PartialSummary("any object", "an oject of any type")


@summarize.register(dict)  # noqa F811
def summarize_(configuration: dict):  # noqa F811
    return PartialSummary(
        "any configuration", "any configuration that can be provided to a process"
    )


@summarize.register(SlurmClusterConfiguration)  # noqa F811
def summarize_(cluster_config: SlurmClusterConfiguration):  # noqa F811
    return PartialSummary(
        "cluster configuration",
        "cluster configuration to launch some remote processing",
    )


@summarize.register(TomwerScanBase)  # noqa F811
def summarize_(data: TomwerScanBase):  # noqa F811
    return PartialSummary(
        "dataset with processing history",
        "core object used to ship dataset and history of processing done on this dataset",
    )


@summarize.register(FutureTomwerObject)  # noqa F811
def summarize_(future_data: FutureTomwerObject):  # noqa F811
    return PartialSummary(
        "dataset with pending processing",
        "object used when there is some pending processing (asyncio.future). Can be convert back to `data`",
    )


@summarize.register(BlissScan)  # noqa F811
def summarize_(bliss_scan: BlissScan):  # noqa F811
    return PartialSummary(
        "raw dataset from bliss",
        "object used when debug some processing relative to bliss",
    )

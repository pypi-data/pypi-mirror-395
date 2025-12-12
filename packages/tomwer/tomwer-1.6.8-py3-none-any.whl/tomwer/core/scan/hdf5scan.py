from tomwer.core.scan.nxtomoscan import NXtomoScanIdentifier, NXtomoScan
from tomwer.core.utils.deprecation import deprecated_warning


class HDF5TomoScanIdentifier(NXtomoScanIdentifier):
    def __init__(self, metadata=None, *args, **kwargs):
        deprecated_warning(
            name="tomwer.core.scan.nxtomoscan.NXtomoScanIdentifier",
            type_="class",
            reason="improve readibility",
            since_version="1.3",
            replacement="NXtomoScanIdentifier",
        )
        super().__init__(metadata, *args, **kwargs)


class HDF5TomoScan(NXtomoScan):
    def __init__(self, scan, entry, index=None, overwrite_proc_file=False):
        deprecated_warning(
            name="tomwer.core.scan.nxtomoscan.NXtomoScan",
            type_="class",
            reason="improve readibility",
            since_version="1.3",
            replacement="NXtomoScan",
        )
        super().__init__(scan, entry, index, overwrite_proc_file)

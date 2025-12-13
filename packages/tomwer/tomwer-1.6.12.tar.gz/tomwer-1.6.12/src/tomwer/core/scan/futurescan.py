from silx.utils.deprecation import deprecated

from tomwer.core.futureobject import TomwerScanBase


@deprecated(replacement="TomwerScanBase", since_version="1.0")
class FutureTomwerScan(TomwerScanBase):
    pass

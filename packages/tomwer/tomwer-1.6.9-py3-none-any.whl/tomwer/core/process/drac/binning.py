import numpy
from enum import Enum as _Enum


class Binning(_Enum):
    ONE_BY_ONE = "1x1"
    TWO_BY_TWO = "2x2"
    FOUR_BY_FOUR = "4x4"
    HEIGHT_BY_HEIGHT = "8x8"
    SIXTEEN_BY_SIXTEEN = "16x16"
    THIRTY_TWO_BY_THIRTY_TWO = "32x32"
    SIXTY_FOUR_BY_SIXTY_FOUR = "64x64"
    ONE_HUNDRED_TWENTY_HEIGHT_BY_ONE_HUNDRED_TWENTY_HEIGHT = "128x128"

    @staticmethod
    def _bin_data(data, binning):
        if not isinstance(data, numpy.ndarray):
            raise TypeError("data should be a numpy array")
        if not data.ndim == 2:
            raise ValueError("data is expected to be 2d")
        binning = Binning(binning)
        if binning is Binning.ONE_BY_ONE:
            return data
        elif binning is Binning.TWO_BY_TWO:
            return data[::2, ::2]
        elif binning is Binning.FOUR_BY_FOUR:
            return data[::4, ::4]
        elif binning is Binning.HEIGHT_BY_HEIGHT:
            return data[::8, ::8]
        elif binning is Binning.SIXTEEN_BY_SIXTEEN:
            return data[::16, ::16]
        elif binning is Binning.THIRTY_TWO_BY_THIRTY_TWO:
            return data[::32, ::32]
        elif binning is Binning.SIXTY_FOUR_BY_SIXTY_FOUR:
            return data[::64, ::64]
        else:
            raise NotImplementedError

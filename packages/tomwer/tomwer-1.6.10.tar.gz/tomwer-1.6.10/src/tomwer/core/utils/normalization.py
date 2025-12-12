# coding: utf-8
from __future__ import annotations

import logging

import fabio

_logger = logging.getLogger(__name__)


def flatFieldCorrection(imgs, dark, flat):
    """
    Simple normalization of a list of images.
    Normalization is made for X-Ray imaging:
    (img - dark) / (flat - dark)

    :param imgs: list of imgs to correct. key: index of the image,
                      value: the image path or numpy.ndarray
    :param dark: dark image
    :param flat: flat image
    :return: list of corrected images
    """
    res = {}
    conditionOK = True
    if dark.ndim != 2:
        _logger.error(
            "cannot make flat field correction, dark should be of " "dimension 2"
        )
        conditionOK = False

    if flat.ndim != 2:
        _logger.error(
            "cannot make flat field correction, flat should be of " "dimension 2"
        )
        conditionOK = False

    if dark.shape != flat.shape:
        _logger.error("Given dark and flat have incoherent dimension")
        conditionOK = False

    if conditionOK is False:
        return res

    for index, img in imgs.items():
        imgData = img
        if type(img) is str:
            assert img.endswith(".edf")
            imgData = fabio.open(img).data

        if imgData.shape != dark.shape:
            _logger.error("Image has invalid. Cannot apply flat field" "correction it")
            corrrectedImage = imgData
        else:
            corrrectedImage = (imgData - dark) / (flat - dark)

        res[index] = corrrectedImage

    return res

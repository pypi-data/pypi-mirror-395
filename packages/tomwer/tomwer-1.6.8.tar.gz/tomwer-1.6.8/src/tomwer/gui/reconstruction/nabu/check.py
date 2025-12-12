# coding: utf-8
from __future__ import annotations


from silx.gui import qt
from nxtomo.nxobject.nxdetector import ImageKey

from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.core.utils.nxtomoutils import get_n_series


def check_dark_series(scan: NXtomoScan, logger=None, user_input: bool = True) -> bool:
    """
    check:
        - if scan has computed_dark attached. If there is more than one then ask confirmation to the user to process the dataset
        - else if the NXTomo has more than one series of dark. Otherwise ask confirmation to the user to process the dataset

    ask confirmation for processing is done by a pop up dialog.

    :param scan: scan to check
    :param user_input: if True and if n series of flat is invalid then ask the user to confirm the processing. Else print a warning and refuse processing

    :return: True if processing can be done else False
    :note: user can 'force' the processing to be done
    """
    if not isinstance(scan, NXtomoScan):
        raise TypeError(
            f"scan is expected to be an instance of {NXtomoScan} not a {type(scan)}"
        )
    try:
        image_keys = scan.image_keys
    except AttributeError:
        image_keys = scan.image_key

    n_series = get_n_series(
        image_key_values=image_keys, image_key_type=ImageKey.DARK_FIELD
    )
    if n_series != 1:
        text = f"{n_series} series of dark found when one expected. Nabu won't be able to run reconstruction (flat field will fail)."
        if n_series > 1:
            text += "\nYou can edit image_keys from the `image-key-editor` to ignore a series (invalid all keys of series you want to ignore)."
        if user_input is False:
            text += "\n skip processing"
            if logger is not None:
                logger.error(text)
            return False
        else:
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Warning)
            types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
            msg.setStandardButtons(types)
            text += "\nContinue ?"
            msg.setText(text)
            return msg.exec() == qt.QMessageBox.Ok
    else:
        return True


def check_flat_series(scan: NXtomoScan, logger, user_input: bool = True) -> bool:
    """
    Insure the scan contains at least one series of flat. Otherwise warn the user nabu will not be able to process
    """
    if not isinstance(scan, NXtomoScan):
        raise TypeError(
            f"scan is expected to be an instance of {NXtomoScan} not a {type(scan)}"
        )
    try:
        image_keys = scan.image_keys
    except AttributeError:
        image_keys = scan.image_key
    n_series = get_n_series(
        image_key_values=image_keys, image_key_type=ImageKey.FLAT_FIELD
    )
    if n_series == 0:
        text = "No flat found. Nabu will no be able to do the flat field correction and to reconstruct dataset."
        if user_input is False:
            if logger is not None:
                logger.error(text)
            return False
        else:
            msg = qt.QMessageBox()
            msg.setIcon(qt.QMessageBox.Warning)
            types = qt.QMessageBox.Ok | qt.QMessageBox.Cancel
            msg.setStandardButtons(types)
            text += "\nContinue ?"
            msg.setText(text)
            return msg.exec() == qt.QMessageBox.Ok
    else:
        return True

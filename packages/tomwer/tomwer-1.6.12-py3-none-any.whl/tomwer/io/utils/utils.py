"""
contains utils for inputs and outputs
"""

from __future__ import annotations

import logging
import os

import h5py
import numpy.lib.npyio
from PIL import Image
from silx.io.utils import open as open_hdf5
from tomoscan.esrf import has_glymur
from tomoscan.esrf.scan.utils import get_data as tomoscan_get_data

from tomwer.core.utils import ftseriesutils

try:
    import tifffile  # noqa #F401 needed for later possible lazy loading
except ImportError:
    has_tifffile = False
else:
    has_tifffile = True


_logger = logging.getLogger(__name__)


def get_slice_data(url):
    """Return data from an url"""
    if os.path.exists(url.file_path()) and os.path.isfile(url.file_path()):
        if url.file_path().lower().endswith(
            ".vol.info"
        ) or url.file_path().lower().endswith(".vol"):
            data = _loadVol(url)

        elif url.scheme() == "tomwer":
            data = numpy.array(Image.open(url.file_path()))
            if url.data_slice() is not None:
                data = data[url.data_slice()]
        elif url.scheme() == ("tifffile"):
            if not has_tifffile:
                _logger.warning("tifffile must be installed to read tiff")
                data = None
            else:
                data = tifffile.imread(url.file_path())
                if url.data_slice() is not None:
                    data = data[url.data_slice()]
        elif url.scheme() in ("jp2", "jp2k", "glymur"):
            if not has_glymur:
                _logger.warning("glymur must be installed to read jpeg2000")
                data = None
            else:
                import glymur

                data = glymur.Jp2k(url.file_path())[:]
        else:
            try:
                data = tomoscan_get_data(url)
            except Exception as e:
                _logger.warning(
                    f"file {url} not longer exists or is empty. Error is {e}"
                )
                data = None
    else:
        _logger.warning("file %s not longer exists or is empty" % url)
        data = None
    return data


def _loadVol(url):
    """Load data from a .vol file and an url"""
    if url.file_path().lower().endswith(".vol.info"):
        infoFile = url.file_path()
        rawFile = url.file_path().replace(".vol.info", ".vol")
    else:
        assert url.file_path().lower().endswith(".vol")
        rawFile = url.file_path()
        infoFile = url.file_path().replace(".vol", ".vol.info")

    if not os.path.exists(rawFile):
        data = None
        mess = f"Can't find raw data file {rawFile} associated with {infoFile}"
        _logger.warning(mess)
    elif not os.path.exists(infoFile):
        mess = f"Can't find info file {infoFile} associated with {rawFile}"
        _logger.warning(mess)
        data = None
    else:
        shape = ftseriesutils.get_vol_file_shape(infoFile)
        if None in shape:
            _logger.warning(f"Fail to retrieve data shape for {infoFile}.")
            data = None
        else:
            try:
                numpy.zeros(shape)
            except MemoryError:
                data = None
                _logger.warning(f"Raw file {rawFile} is to large for being readed")
            else:
                data = numpy.fromfile(rawFile, dtype=numpy.float32, count=-1, sep="")
                try:
                    data = data.reshape(shape)
                except ValueError:
                    _logger.warning(
                        f"unable to fix shape for raw file {rawFile}. Look for information in {infoFile}"
                    )
                    try:
                        sqr = int(numpy.sqrt(len(data)))
                        shape = (1, sqr, sqr)
                        data = data.reshape(shape)
                    except ValueError:
                        _logger.info(f"deduction of shape size for {rawFile} failed")
                        data = None
                    else:
                        _logger.warning(
                            f"try deducing shape size for {rawFile} might be an incorrect interpretation"
                        )
    if url.data_slice() is None:
        return data
    else:
        return data[url.data_slice()]


def get_default_directory() -> str:
    """

    :return: default directory where to open a QFolder dialdg for example
    """
    if "TOMWER_DEFAULT_INPUT_DIR" in os.environ and os.path.exists(
        os.environ["TOMWER_DEFAULT_INPUT_DIR"]
    ):
        return os.environ["TOMWER_DEFAULT_INPUT_DIR"]
    else:
        try:
            return os.getcwd()
        except FileNotFoundError:
            return os.sep


def format_stderr_stdout(stdout, stderr, config=None):
    s_out = stdout.decode("utf-8") if stdout is not None else ""
    s_err = stderr.decode("utf-8") if stderr is not None else ""
    if config is None:
        config = ""
    else:
        assert isinstance(config, dict)
    return (
        f"############# nabu ############## \nconfig: {config}\n"
        f"------------- stderr -------------\n{s_err}\n"
        f"------------- stdout -------------\n{s_out}\n"
    )


def get_linked_files_with_entry(hdf5_file: str, entry: str) -> set:
    """
    parse all datasets under the entry and look for connections with external files (vds or ExternalLink)
    """
    items_to_treat = set()  # abs_file_path, file_path, data_path
    final_datasets = set()  # file_path, dataset_path
    treated_items = set()  # abs_file_path, data_path

    abs_hdf5_file = os.path.abspath(hdf5_file)
    items_to_treat.add((abs_hdf5_file, hdf5_file, entry))

    while len(items_to_treat) > 0:
        to_treat = list(items_to_treat)
        items_to_treat.clear()
        for abs_file_path, file_path, data_path in to_treat:
            item = abs_file_path, data_path
            if item in treated_items:
                continue
            dirname = os.path.dirname(abs_file_path)
            with open_hdf5(abs_file_path) as h5f:
                node = h5f.get(data_path, getlink=True)
                if isinstance(node, h5py.ExternalLink):
                    ext_file_path = node.filename
                    if not os.path.isabs(ext_file_path):
                        ext_file_path = os.path.join(dirname, ext_file_path)
                    items_to_treat.add(
                        (os.path.abspath(ext_file_path), node.filename, node.path)
                    )
                node = h5f.get(data_path, getlink=False)
                if isinstance(node, h5py.Dataset) and node.is_virtual:
                    final_datasets.update(
                        get_linked_files_with_vds(abs_file_path, data_path)
                    )
                elif abs_file_path != abs_hdf5_file:
                    final_datasets.add((file_path, data_path))

                treated_items.add(item)

                if isinstance(node, h5py.Group):
                    for key in node.keys():
                        data_sub_path = "/".join((data_path, key))
                        if (
                            abs_file_path,
                            data_sub_path,
                        ) not in treated_items:
                            items_to_treat.add(
                                (abs_file_path, file_path, data_sub_path)
                            )
    return final_datasets


def get_linked_files_with_vds(hdf5_file: str, dataset_path: str) -> set:
    """
    parse all virtual sources of a virtual dataset and return a set of files / dataset connected to it
    """
    items_to_treat = set()  # abs_file_path, file_path, dataset_path
    final_datasets = set()  # file_path, dataset_path
    treated_items = set()  # abs_file_path, dataset_path

    abs_hdf5_file = os.path.abspath(hdf5_file)
    items_to_treat.add((abs_hdf5_file, hdf5_file, dataset_path))

    while len(items_to_treat) > 0:
        to_treat = list(items_to_treat)
        items_to_treat.clear()
        for abs_file_path, file_path, dataset_path in to_treat:
            item = abs_file_path, dataset_path
            if item in treated_items:
                continue
            dirname = os.path.dirname(abs_file_path)
            with open_hdf5(abs_file_path) as h5f:
                dataset = h5f[dataset_path]
                if dataset.is_virtual:
                    for vs_info in dataset.virtual_sources():
                        vs_file_path = vs_info.file_name
                        if not os.path.isabs(vs_file_path):
                            vs_file_path = os.path.join(dirname, vs_file_path)
                        items_to_treat.add(
                            (
                                os.path.abspath(vs_file_path),
                                vs_info.file_name,
                                vs_info.dset_name,
                            )
                        )
                else:
                    final_datasets.add((file_path, dataset_path))
            treated_items.add(item)

    return final_datasets


def str_to_dict(my_str: str | dict):
    """convert a string as key_1=value_2;key_2=value_2 to a dict"""
    if isinstance(my_str, dict):
        return my_str
    res = {}
    for key_value in filter(None, my_str.split(";")):
        key, value = key_value.split("=")
        res[key] = value
    return res

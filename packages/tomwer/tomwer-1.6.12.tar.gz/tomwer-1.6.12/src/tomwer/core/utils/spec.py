from __future__ import annotations

import fileinput
import logging
import os
import pint

import fabio

from lxml import etree


_logger = logging.getLogger(__name__)

_ureg = pint.get_application_registry()


def _getInformation(scan, refFile, information, _type, aliases=None):
    """
    Parse files contained in the given directory to get the requested
    information

    :param scan: directory containing the acquisition. Must be an absolute path
    :param refFile: the refXXXX_YYYY which should contain information about the
                    scan.
    :return: the requested information or None if not found
    """

    def parseRefFile(filePath):
        header = fabio.open(filePath).header
        for k in aliases:
            if k in header:
                return _type(header[k])
        return None

    def parseXMLFile(filePath):
        try:
            for alias in info_aliases:
                tree = etree.parse(filePath)
                elmt = tree.find("acquisition/" + alias)
                if elmt is None:
                    continue
                else:
                    info = _type(elmt.text)
                    if info == -1:
                        return None
                    else:
                        return info
        except etree.XMLSyntaxError as e:
            _logger.warning(e)
            return None

    def parseInfoFile(filePath):
        def extractInformation(text, alias):
            text = text.replace(alias, "")
            text = text.replace("\n", "")
            text = text.replace(" ", "")
            text = text.replace("=", "")
            return _type(text)

        info = None
        f = open(filePath, "r")
        line = f.readline()
        while line:
            for alias in info_aliases:
                if alias in line:
                    info = extractInformation(line, alias)
                    break
            line = f.readline()
        f.close()
        return info

    info_aliases = [information]
    if aliases is not None:
        assert type(aliases) in (tuple, list)
        [info_aliases.append(alias) for alias in aliases]

    if not os.path.isdir(scan):
        return None

    if refFile is not None and os.path.isfile(refFile):
        try:
            info = parseRefFile(refFile)
        except IOError as e:
            _logger.warning(e)
        else:
            if info is not None:
                return info

    baseName = os.path.basename(scan)
    infoFiles = [os.path.join(scan, baseName + ".info")]
    infoOnDataVisitor = infoFiles[0].replace("lbsram", "", 1)
    # hack to check in lbsram, would need to be removed to add some consistency
    if os.path.isfile(infoOnDataVisitor):
        infoFiles.append(infoOnDataVisitor)
    for infoFile in infoFiles:
        if os.path.isfile(infoFile) is True:
            info = parseInfoFile(infoFile)
            if info is not None:
                return info

    xmlFiles = [os.path.join(scan, baseName + ".xml")]
    xmlOnDataVisitor = xmlFiles[0].replace("lbsram", "", 1)
    # hack to check in lbsram, would need to be removed to add some consistency
    if os.path.isfile(xmlOnDataVisitor):
        xmlFiles.append(xmlOnDataVisitor)
    for xmlFile in xmlFiles:
        if os.path.isfile(xmlFile) is True:
            info = parseXMLFile(xmlFile)
            if info is not None:
                return info

    return None


def getClosestEnergy(scan, refFile=None):
    """
    Parse files contained in the given directory to get information about the
    incoming energy for the serie `iSerie`

    :param scan: directory containing the acquisition
    :param refFile: the refXXXX_YYYY which should contain information about the
                    energy.
    :return: the energy in keV or none if no energy found
    """
    return _getInformation(
        os.path.abspath(scan),
        refFile,
        information="Energy",
        aliases=["energy", "ENERGY"],
        _type=float,
    )


def getTomo_N(scan):
    """Return the number of radio taken"""
    return _getInformation(
        os.path.abspath(scan),
        refFile=None,
        information="TOMO_N",
        _type=int,
        aliases=["tomo_N", "Tomo_N"],
    )


def getDARK_N(scan):
    return _getInformation(
        os.path.abspath(scan),
        refFile=None,
        information="DARK_N",
        _type=int,
        aliases=["dark_N"],
    )


def rebaseParFile(_file, oldfolder, newfolder):
    """Update the given .par file to replace oldfolder location by the newfolder.

    .. warning:: make the replacement in place.

    :param _file: par file to update
    :param oldfolder: previous location of the .par file
    :param newfolder: new location of the .par file
    """
    with fileinput.FileInput(_file, inplace=True, backup=".bak") as parfile:
        for line in parfile:
            line = line.rstrip().replace(oldfolder, newfolder, 1)
            print(line)


def getDim1Dim2(scan: str) -> tuple[int]:
    """

    :param scan: path to the acquisition
    :return: detector definition
    """
    d1 = _getInformation(
        scan=scan,
        refFile=None,
        information="Dim_1",
        aliases=["projectionSize/DIM_1"],
        _type=int,
    )
    d2 = _getInformation(
        scan=scan,
        refFile=None,
        information="Dim_2",
        aliases=["projectionSize/DIM_2"],
        _type=int,
    )
    return d1, d2


def getParametersFromParOrInfo(_file):
    """
    Create a dictionary from the file with the information name as keys and
    their values as values
    """
    assert os.path.exists(_file) and os.path.isfile(_file)
    ddict = {}
    f = open(_file, "r")
    lines = f.readlines()
    for line in lines:
        if "=" not in line:
            continue
        line_str = line.replace(" ", "")
        line_str = line_str.rstrip("\n")
        # remove on the line comments
        if "#" in line_str:
            line_str = line_str.split("#")[0]
        if line_str == "":
            continue
        try:
            key, value = line_str.split("=")
        except ValueError:
            _logger.error('fail to extract information from "%s"' % line_str)
        else:
            ddict[key.lower()] = value
    return ddict


def getFirstProjFile(scan):
    """Return the first .edf containing a projection"""
    if os.path.isdir(scan) is False:
        return None
    files = sorted(os.listdir(scan))

    while (
        len(files) > 0
        and (files[0].startswith(os.path.basename(scan)) and files[0].endswith(".edf"))
        is False
    ):
        files.remove(files[0])

    if len(files) > 0:
        return os.path.join(scan, files[0])
    else:
        return None


def getPixelSize(scan) -> float | None:
    """
    Try to retrieve the pixel size from the set of files.

    :return: the pixel size in meter or None
    """
    if os.path.isdir(scan) is False:
        return None
    value = _getInformation(
        scan=scan,
        refFile=None,
        information="PixelSize",
        _type=float,
        aliases=["pixelSize"],
    )
    if value is None:
        parFile = os.path.join(scan, os.path.basename(scan) + ".par")
        if os.path.exists(parFile):
            ddict = getParametersFromParOrInfo(parFile)
            if "IMAGE_PIXEL_SIZE_1".lower() in ddict:
                value = float(ddict["IMAGE_PIXEL_SIZE_1".lower()])
    # for now pixel size are stored in microns. We want to return them in meter
    if value is not None:
        return (value * _ureg.micrometer).to_base_units().magnitude
    else:
        return None

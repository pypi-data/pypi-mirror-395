from tomoscan.esrf.identifier.edfidentifier import EDFVolumeIdentifier
from tomoscan.esrf.identifier.hdf5Identifier import (
    HDF5VolumeIdentifier,
)
from tomoscan.esrf.identifier.jp2kidentifier import JP2KVolumeIdentifier
from tomoscan.esrf.identifier.rawidentifier import RawVolumeIdentifier
from tomoscan.esrf.identifier.tiffidentifier import (
    MultiTiffVolumeIdentifier,
    TIFFVolumeIdentifier,
)

from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.volume.volumefactory import VolumeFactory
from tomoscan.esrf.volume.utils import guess_volumes

from tomwer.core.volume.edfvolume import EDFVolume
from tomwer.core.volume.hdf5volume import HDF5Volume
from tomwer.core.volume.jp2kvolume import JP2KVolume
from tomwer.core.volume.rawvolume import RawVolume
from tomwer.core.volume.tiffvolume import MultiTIFFVolume, TIFFVolume


DEFAULT_SCHEME_TO_VOL = {
    EDFVolumeIdentifier.scheme: EDFVolume,
    HDF5VolumeIdentifier.scheme: HDF5Volume,
    TIFFVolumeIdentifier.scheme: TIFFVolume,
    MultiTiffVolumeIdentifier.scheme: MultiTIFFVolume,
    JP2KVolumeIdentifier.scheme: JP2KVolume,
    RawVolumeIdentifier.scheme: RawVolume,
}


def get_tomo_objs_instances(tomo_objs: tuple) -> tuple:
    """
    return instances of TomoObj from a tuple of string (either from identifiers directly or from file path parsing)
    """
    instances = []
    has_scans = False
    has_vols = False
    for tomo_obj in tomo_objs:

        def get_scans():
            try:
                return (ScanFactory.create_tomo_object_from_identifier(tomo_obj),)
            except Exception:
                try:
                    return ScanFactory.create_scan_objects(tomo_obj)
                except Exception:
                    return tuple()

        def get_volumes():
            try:
                return (VolumeFactory.create_tomo_object_from_identifier(tomo_obj),)
            except Exception:
                try:
                    return guess_volumes(
                        tomo_obj,
                        scheme_to_vol=DEFAULT_SCHEME_TO_VOL,
                        filter_histograms=True,
                    )
                except Exception:
                    return tuple()

        scans_found = get_scans()
        if len(scans_found) == 0:
            # we start by scan because they have a 'definition' as NXtomo available.
            # otherwise we might get some entries defined as scan AND volume...
            # for stitching we expect users to ask of for one or the other.
            volumes = get_volumes() or ()
            if len(volumes) > 0:
                has_vols = True
                instances.extend(volumes)
        else:
            has_scans = len(scans_found) > 0
            instances.extend(scans_found)

    return tuple(instances), (has_scans, has_vols)

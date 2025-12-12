from typing import Any

from tomwer.core.volume.volumefactory import VolumeFactory


def volume_identifier_to_volume(volume_identifier: Any):
    """
    from a str identifier try to create a volume.
    Mostly used when 'volume' parameter is set from ewoks. In this case we expect it to be a (string) identifier
    """
    if isinstance(volume_identifier, str):
        return VolumeFactory.create_tomo_object_from_identifier(volume_identifier)
    else:
        return volume_identifier

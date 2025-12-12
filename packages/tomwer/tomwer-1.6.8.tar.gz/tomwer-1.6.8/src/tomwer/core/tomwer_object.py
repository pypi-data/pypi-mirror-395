"""contains TomwerObject class. Mother object of all the object used as input / output through the tomwer project.
At the moment those objects are either a scan (ready to be processed), a volume or a bliss scan (raw scan that needs to be converted to scan to be processed)
"""

from processview.core.dataset import Dataset


class TomwerObject(Dataset):
    """Common tomwer object"""

    _DICT_USER_STITCHING_METADATA = "user_def_stitching_metadata"

    def __init__(self) -> None:
        super().__init__()
        self._cast_volume = None
        self._stitching_metadata = None

    def _clear_heavy_cache(self):
        """util function to clear some heavy object from the cache"""
        raise NotImplementedError()

    def clear_cache(self):
        pass

    @property
    def cast_volume(self):
        # for now this is used as an east way to cache the identifier and provide it to the remaining of the orange canvas.
        # but this is a wrong designa and should be removed at one point.
        return self._cast_volume

    @cast_volume.setter
    def cast_volume(self, volume):
        from tomwer.core.volume.volumebase import TomwerVolumeBase

        if not (volume is None or isinstance(volume, TomwerVolumeBase)):
            from tomwer.core.volume.volumefactory import (
                VolumeFactory,
            )  # avoid cyclic import

            volume = VolumeFactory.create_tomo_object_from_identifier(identifier=volume)
        self._cast_volume = volume

    @property
    def stitching_metadata(self):
        return self._stitching_metadata

    @stitching_metadata.setter
    def stitching_metadata(self, metadata):
        from tomwer.core.process.stitching.metadataholder import StitchingMetadata

        if metadata is not None and not isinstance(metadata, StitchingMetadata):
            raise TypeError(
                f"metadata is expected to be an optional instance of {StitchingMetadata}. Not {type(metadata)}"
            )
        self._stitching_metadata = metadata

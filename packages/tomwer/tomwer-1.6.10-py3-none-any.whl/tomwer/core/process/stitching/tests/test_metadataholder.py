from tomwer.core.process.stitching.metadataholder import StitchingMetadata


def test_to_dict_from_dict():
    """Test conversion of StitchingMetadata from dict and to dict"""
    metadata = StitchingMetadata(tomo_obj=None)
    metadata._pixel_or_voxel_size = [12.3, 2.5, None]
    metadata._pos_as_m = [None, 3.6, None]
    metadata._pos_as_px = [5, 9, 8]

    ddict = metadata.to_dict()
    assert isinstance(ddict, dict)

    loaded_metadata = StitchingMetadata.from_dict(ddict, tomo_obj=None)
    assert loaded_metadata == metadata
    assert loaded_metadata.to_dict() == ddict
    assert isinstance(str(loaded_metadata), str)

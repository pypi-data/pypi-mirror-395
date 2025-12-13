from __future__ import annotations

from pydantic import field_validator
from ewokscore.model import BaseInputModel
from tomwer.core.volume.volumebase import TomwerVolumeBase
from tomwer.core.volume.volumefactory import VolumeFactory


class VolumeViewerModel(BaseInputModel):
    volume: TomwerVolumeBase | str
    load_volume: bool

    @field_validator("volume", mode="before")
    @classmethod
    def cast_volume(cls, value) -> TomwerVolumeBase:
        if isinstance(value, str):
            value = VolumeFactory.create_tomo_object_from_identifier(value)
        return value

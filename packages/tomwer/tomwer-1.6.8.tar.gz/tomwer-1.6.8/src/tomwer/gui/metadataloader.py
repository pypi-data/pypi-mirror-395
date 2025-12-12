"""Utils to load metadata (from a volume at the moment)"""

import logging
from silx.gui import qt
from tomwer.core.volume.volumefactory import VolumeFactory

_logger = logging.getLogger(__name__)

__all__ = [
    "VolumeMetadataLoader",
]


class VolumeMetadataLoader(qt.QThread):
    """Thread to load metadata from a given volume"""

    def __init__(self, parent, tomo_obj_identifier: str):
        super().__init__(parent=parent)
        self.volume = VolumeFactory.create_tomo_object_from_identifier(
            tomo_obj_identifier
        )
        self.metadata = None

    def run(self):
        try:
            self.metadata = self.volume.load_metadata()
        except IOError:
            self.metadata = None
        except Exception as e:
            _logger.error(
                "Fail to load metadata from %s. Error is %s",
                self.volume.get_identifier(),
                e,
            )
            self.metadata = None

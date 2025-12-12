from enum import Enum as _Enum


PROPOSAL_GALLERY_DIR_NAME = "GALLERY"
DATASET_GALLERY_DIR_NAME = "gallery"


class OutputFormat(_Enum):
    """possible output format to save screenshots"""

    PNG = "png"
    JPEG = "jpg"

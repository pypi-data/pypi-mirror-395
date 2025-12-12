import os

from tomwer.core.tomwer_object import TomwerObject


class TomwerVolumeBase(TomwerObject):
    def _clear_heavy_cache(self):
        """util user"""
        self.data = None
        self.metadata = None

    @property
    def icat_data_dir(self) -> str:
        """Return the data directory to be used by icat for the volume"""
        return os.path.dirname(self.data_url.file_path())  # pylint: disable=E1101

    @staticmethod
    def format_output_location(location: str, volume):
        if not isinstance(volume, TomwerVolumeBase):
            raise TypeError(
                f"volume is expected to be an instance of {TomwerVolumeBase}"
            )

        keywords = {
            "volume_data_parent_folder": volume.volume_data_parent_folder(),
        }

        # filter necessary keywords
        def get_necessary_keywords():
            import string

            formatter = string.Formatter()
            return [field for _, field, _, _ in formatter.parse(location) if field]

        requested_keywords = get_necessary_keywords()

        def keyword_needed(pair):
            keyword, _ = pair
            return keyword in requested_keywords

        keywords = dict(filter(keyword_needed, keywords.items()))
        location = os.path.abspath(location.format(**keywords))
        return location

    def volume_data_parent_folder(self):
        if self.data_url is None:  # pylint: disable=E1101
            raise ValueError("data_url doesn't exists")
        else:
            return os.path.dirname(self.data_url.file_path())  # pylint: disable=E1101

    def __str__(self) -> str:
        try:
            return self.get_identifier().to_str()
        except Exception:
            return super().__str__()

class HelicalMetadata:
    def __init__(self) -> None:
        self._processes_files = (
            "{scan_parent_dir_basename}/{scan_dir_name}/map_and_doubleff.hdf5"
        )

    @property
    def processes_files(self) -> str:
        return self._processes_files

    @processes_files.setter
    def processes_files(self, path: str):
        if not isinstance(path, str):
            raise TypeError(f"expects a str. Get {path}")
        self._processes_files = path

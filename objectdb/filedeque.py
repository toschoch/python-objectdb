from pathlib import Path


class FileDeque:

    def __init__(self, maxlen=None, maxsize=None, **kwargs):
        self._path = Path(kwargs.pop("path", "/data"))
        self._index_file_path = self._path.joinpath(kwargs.pop("index_filename", ".index.csv"))

        return

    def append(self, filename, meta: dict = None, **kwargs) -> None:
        return

    def clear(self) -> None:
        return

    def reindex(self) -> None:
        return

    def _append_to_index(self):
        return

    def sizeGB(self) -> float:
        return 0

    def _release(self, gb_to_release):
        return

    def _delete_file(self, filename):
        return

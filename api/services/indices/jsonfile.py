from uuid import UUID
from typing import List, Tuple, Union
import os, json

from .index import Index
from ...models import Object


class JsonFileIndex(Index):

    def __init__(self, index_filename: Union[str, os.PathLike] = "index.jsons"):
        self._index_filename = index_filename

    @staticmethod
    def buffer_count(filename) -> int:
        f = open(filename, 'r')
        lines = 0
        buf_size = 1024 * 1024
        read_f = f.read  # loop optimization

        buf = read_f(buf_size)
        while buf:
            lines += buf.count('\n')
            buf = read_f(buf_size)

        return lines

    def total_size(self) -> int:
        if not os.path.isfile(self._index_filename):
            return 0
        with open(self._index_filename, 'r') as reader:
            size = sum(obj['size'] for obj in json.load(reader.readline()) if obj['size'] is not None)
        return size

    def total_entries(self) -> int:
        if not os.path.isfile(self._index_filename):
            return 0
        return self.buffer_count(self._index_filename)

    def get_oldest_with_size_exceeding(self, size: int) -> Tuple[int, List[Object]]:
        pass

    def get_all(self, bucket: str = None) -> List[Object]:
        pass

    def get(self, id: UUID) -> Object:
        pass

    def contains(self, id: UUID) -> bool:
        pass

    def remove(self, id: UUID):
        pass

    def insert(self, obj: Object):
        if os.path.isfile(self._index_filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        with open(self._index_filename, append_write) as fp:
            fp.write(obj.json()+"\n")

    def update(self, object: Object):
        pass

    def clear(self):
        pass

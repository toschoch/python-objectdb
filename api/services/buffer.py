from abc import ABC, abstractmethod
import humanfriendly

from .index import Index
from .storage import Storage
from ..models import Object


class CircularQueue(ABC):

    @abstractmethod
    def append(self, obj: Object) -> Object:
        pass


class MaxSizeQueue(CircularQueue):

    def __init__(self, max_size: str, usual_object_size: str, margin: str,
                 index: Index,
                 storage: Storage):
        self.max_size = humanfriendly.parse_size(max_size, binary=True)
        self.usual_object_size = humanfriendly.parse_size(usual_object_size, binary=True)
        self.margin = humanfriendly.parse_size(margin, binary=True)

        self._index = index

        self._storage = storage

    def append(self, obj: Object) -> Object:
        if obj.size is None:
            obj.size = self.usual_object_size

        self.reserve_space(obj.size)
        self._index.insert(obj)
        return obj

    def reserve_space(self, size: int):
        excess_size = self.excess_size(size)
        if excess_size > 0:
            self.free(excess_size)
        assert self.excess_size(size) == 0

    def free(self, size: int):
        additional_bytes, to_remove = self._index.get_oldest_with_size_exceeding(size)
        for obj in to_remove:
            self._index.remove(obj.id)
            self._storage.delete(obj)

    def excess_size(self, object_size: int = None, additional_objects: int = 1) -> int:
        return max(0, self.size() + object_size * additional_objects + self.margin - self.max_size)

    def size(self) -> int:
        return self._index.total_size()

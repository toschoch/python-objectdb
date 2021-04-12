from abc import ABC, abstractmethod
import humanfriendly

from .index import Index
from .storage import Storage
from ..models import Object


class MaxSizeDeque:

    def __init__(self, max_size: str, usual_object_size: str, margin: str,
                 index: Index, reservations: Index,
                 storage: Storage):
        self.max_size = humanfriendly.parse_size(max_size, binary=True)
        self.usual_object_size = humanfriendly.parse_size(usual_object_size, binary=True)
        self.margin = humanfriendly.parse_size(margin, binary=True)

        self.index = index
        self.reservations = reservations

        self.storage = storage

    def append(self, obj: Object) -> None:
        assert self.reservations.contains(obj.id)
        assert self.storage.exists(obj)

        obj = self.storage.update(obj)

        self.reservations.remove(obj.id)
        self.index.insert_or_update(obj)

    def clear(self) -> None:
        self.reservations.clear()
        self.index.clear()

    def reserve(self, obj: Object):
        if obj.size is None:
            obj.size = self.usual_object_size

        excess_size = self.excess_size(obj.size)
        if excess_size > 0:
            self.free(excess_size)
        assert self.excess_size(obj.size) == 0
        self.reservations.insert_or_update(obj)

    def free(self, size: int):
        additional_bytes, to_remove = self.index.get_oldest_with_size_exceeding(size)
        for obj in to_remove:
            self.index.remove(obj.id)

    def excess_size(self, object_size: int = None, additional_objects: int = 1) -> int:
        return max(0, self.size() + object_size * additional_objects + self.margin - self.max_size)

    def size(self) -> int:
        return self.index.total_size() + self.reservations.total_size()

    def reindex(self) -> None:
        return


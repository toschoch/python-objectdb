from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Tuple

from ..models import Object


class Index(ABC):
    @abstractmethod
    def total_size(self) -> int:
        pass

    @abstractmethod
    def total_entries(self) -> int:
        pass

    @abstractmethod
    def get_oldest_with_size_exceeding(self, size: int) -> Tuple[int, List[Object]]:
        pass

    @abstractmethod
    def get_all(self, bucket: str = None) -> List[Object]:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Object:
        pass

    @abstractmethod
    def contains(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def remove(self, id: UUID):
        pass

    @abstractmethod
    def insert(self, object: Object):
        pass

    @abstractmethod
    def update(self, object: Object):
        pass

    @abstractmethod
    def clear(self):
        pass


class InMemoryIndex(Index):

    def __init__(self):
        self.db = {}

    def get(self, id: UUID) -> Object:
        return self.db[id]

    def contains(self, id: UUID) -> bool:
        return id in self.db

    def remove(self, id: UUID):
        del self.db[id]

    def insert(self, obj: Object):
        self.db[obj.id] = obj.copy()

    def update(self, obj: Object):
        self.db[obj.id] = obj.copy()

    def clear(self):
        self.db.clear()

    def get_all(self, bucket: str = None) -> List[Object]:
        if not bucket:
            return list(self.db.values())

        return list(filter(lambda o: o.bucket == bucket, self.db.values()))

    def get_oldest_with_size_exceeding(self, size: int) -> Tuple[int, List[Object]]:
        oldest = sorted(self.db.values(), key=lambda o: o.date, reverse=True)
        oldest = oldest.__iter__()
        total_size = 0
        objects = []
        while total_size < size:
            try:
                obj = next(oldest)
                total_size += obj.size
                objects.append(obj)
            except StopIteration:
                break
        return total_size, objects

    def total_entries(self) -> int:
        return len(self.db)

    def total_size(self) -> int:
        return sum(obj.size for obj in self.db.values())


class CSVIndex(InMemoryIndex):
    pass

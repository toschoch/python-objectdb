from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Tuple

from ...models import Object


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

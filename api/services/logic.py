from uuid import UUID

from ..models import Object, NewObject, Status, update_model

from .storage import Storage
from .buckets import Buckets
from .buffer import CircularQueue
from .index import Index


class Logic:

    def __init__(self, buckets: Buckets, buffer: CircularQueue, index: Index, storage: Storage):
        self._buckets = buckets
        self._storage = storage
        self._buffer = buffer
        self._index = index

    def create_object(self, obj: NewObject) -> Object:

        bucket = self._buckets.get(obj.bucket)
        obj = update_model(obj, bucket, {'extension', 'mimetype', 'filename_template'})
        self._storage.create(obj)
        obj.status = Status.created

        self._buffer.append(obj)
        return obj

    def update_object(self, obj: Object) -> Object:
        self._index.update(obj)
        return obj

    def finalize_object(self, obj: Object) -> Object:

        assert self._storage.exists(obj)

    def delete_object(self, id: UUID):
        obj = self._index.get(id)
        self._storage.delete(obj)
        self._index.remove(obj.id)


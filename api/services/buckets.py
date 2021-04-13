from typing import List

from fastapi import HTTPException
from jinja2 import Environment, BaseLoader, DebugUndefined
import yaml
import os

from ..models import Bucket
from .storage import Storage
from .index import Index
from .buffer import CircularQueue, MaxSizeQueue


class Buckets:

    def __init__(self, index: Index, storage: Storage):
        self._buckets = {b['name']: Bucket(**b) for b in self.load()}
        self._storage = storage
        self._index = index

    @staticmethod
    def load() -> List[dict]:
        """ loads the buckets configuration from file """

        with open('config/buckets.yml', 'r') as fp:
            content = fp.read()

        variables = {'ENVIRONMENT': os.environ}

        buckets = yaml.safe_load(Environment(loader=BaseLoader,
                                             undefined=DebugUndefined)
                                 .from_string(content)
                                 .render(variables))['buckets']

        validate_buckets(buckets)

        return buckets

    def get_queue(self, bucket: str) -> CircularQueue:
        config = self.get(bucket).buffer

        if config.max_size is not None:
            return MaxSizeQueue(config.max_size.absolute,
                                '1M', '500k', self._index, self._storage)

    def get(self, bucket: str) -> Bucket:
        return self._buckets[bucket]

    def get_all(self) -> List[Bucket]:
        return list(self._buckets.values())

    def validate_bucket(self, bucket: str):
        if bucket not in self._buckets:
            raise HTTPException(400, {
                "loc": [
                    "query",
                    "bucket"
                ],
                "msg": "value is not a valid bucket name",
                "type": "type_error.str"
            })


def validate_buckets(buckets: List[dict]):
    """ validates the buckets configuration """

    assert all('name' in b for b in buckets)
    assert len(set(b['name'] for b in buckets)) == len(buckets)


class Partition:

    def __init__(self, buckets_config: List[Bucket], storage: Storage):

        self.config = buckets_config
        self.storage = storage

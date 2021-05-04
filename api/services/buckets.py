from typing import List, Union

from fastapi import HTTPException
import yaml
import os
from pathlib import Path

from ..models import Bucket
from .storage import Storage
from .indices import Index
from .buffer import CircularQueue, MaxSizeQueue

from ..utils import PartialFormatter


class Buckets:

    def __init__(self, index: Index, storage: Storage):
        self._buckets = {b['name']: Bucket(**b) for b in self.load()}
        self._storage = storage
        self._index = index

    @staticmethod
    def load() -> List[dict]:
        """ loads the buckets configuration from file """

        with open(Path(os.environ.get('BUCKETS_CONFIG', 'config/buckets.yml')), 'r') as fp:
            content = fp.read()

        variables = {'ENVIRONMENT': os.environ}

        s = PartialFormatter().format(content, **variables)

        buckets = yaml.safe_load(s)['buckets']

        validate_buckets(buckets)

        return buckets

    def get_queue(self, bucket: Union[Bucket, str]) -> CircularQueue:
        if isinstance(bucket, str):
            config = self.get(bucket).storage
        else:
            config = bucket.storage

        if config.max_size is not None:
            return MaxSizeQueue(config.max_size.absolute,
                                config.usual_object_size, config.margin_size,
                                self._index, self._storage)
        raise NotImplementedError("Not yet implemented!")

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

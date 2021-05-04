import os
from typing import List, Tuple, Union
from uuid import UUID
import pandas as pd
import json

from .index import Index
from ...models import Object


class FeatherIndex(Index):

    def __init__(self, index_filename: Union[str, os.PathLike] = "index.feather"):
        self._index_filename = index_filename
        self._read()

    def _read(self):
        if os.path.isfile(self._index_filename):
            self._df = pd.read_feather(self._index_filename)
            self._df.set_index('id', drop=False, inplace=True)
        else:
            self._df = pd.DataFrame()

    def _write(self):
        self._df.reset_index(drop=True).to_feather(self._index_filename, compression=None)

    def total_entries(self) -> int:
        return self._df.shape[0]

    def get_oldest_with_size_exceeding(self, size: int) -> Tuple[int, List[Object]]:
        sorted_index = self._df.sort_values('date', ascending=False)
        sorted_index = sorted_index[sorted_index['size'].cumsum() >= size]
        return sorted_index['size'].sum(), list(map(lambda m: Object(**m), sorted_index.to_dict('records')))

    def get_all(self, bucket: str = None) -> List[Object]:
        return list(map(lambda m: Object(**m), self._df.to_dict('records')))

    def get(self, id: UUID) -> Object:
        return Object(**self._df.loc[str(id)].to_dict())

    def contains(self, id: UUID) -> bool:
        return self._df.index.__contains__(str(id))

    def remove(self, id: UUID):
        self._df.drop(str(id), inplace=True)
        self._write()

    def insert(self, obj: Object):
        assert not self.contains(obj.id)
        obj = json.loads(obj.json())
        self._df = self._df.append(pd.Series(obj, name=obj['id']))
        self._write()

    def update(self, obj: Object) -> Object:
        old_obj = self._df.loc[str(obj.id)].to_dict()
        obj = json.loads(obj.json())
        old_obj.update(obj)
        self._df.loc[old_obj['id']] = pd.Series(old_obj)
        self._write()
        return Object(**old_obj)

    def clear(self):
        self._df.drop(self._df.index)
        self._write()

    def total_size(self) -> int:
        return 0 if self._df.empty else self._df['size'].sum()

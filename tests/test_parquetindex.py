import uuid

import pytest
from api.services.indices import ParquetIndex, Index
from api.models import Object, NewObject
import humanfriendly
from .test_jsonfileindex import example_object


@pytest.fixture
def index(tmp_path):
    return ParquetIndex()  # JsonFileIndex(tmp_path.joinpath("myjsons.jsons"))


def test_add_and_get(index: Index, example_object: Object):
    assert index.total_entries() == 0

    index.insert(example_object)
    assert index.total_entries() == 1

    example_object = Object.new(NewObject(**example_object.dict()))
    index.insert(example_object)
    assert index.total_entries() == 2

    obj = index.get(example_object.id)
    assert obj.location == 'data/{}.mp4'.format(obj.id)
    assert index.total_size() == obj.size
    size, oldest = index.get_oldest_with_size_exceeding(100)
    assert oldest[0].id == obj.id
    assert size == 1289748

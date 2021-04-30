import datetime
import uuid

import pytest
from api.services.indices import FeatherIndex, Index
from api.models import Object, NewObject
from .test_inmemoryindex import example_object


@pytest.fixture
def index(tmp_path):
    return FeatherIndex(tmp_path.joinpath("index.feather"))


def test_add_and_get(index: Index, example_object: Object):

    example_object.date = datetime.datetime.utcnow()

    assert index.total_entries() == 0

    index.insert(example_object)
    assert index.total_entries() == 1

    example_object2 = Object.new(NewObject(**example_object.dict()))
    example_object2.size = 123123
    example_object2.date = datetime.datetime.utcnow()
    index.insert(example_object2)
    assert index.total_entries() == 2

    obj = index.get(example_object.id)
    assert obj.location == 'data/{}.mp4'.format(obj.id)
    assert index.total_size() == example_object.size + example_object2.size
    size, oldest = index.get_oldest_with_size_exceeding(example_object.size-100)
    assert oldest[0].id == obj.id
    assert size == 1289748

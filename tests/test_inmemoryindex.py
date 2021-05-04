import datetime
import uuid

import pytest
from api.services.indices import InMemoryIndex, Index
from api.models import Object, Status
import humanfriendly


@pytest.fixture
def index():
    return InMemoryIndex()


@pytest.fixture
def object_factory(tmp_path):
    def create_new_obj():
        new_id = uuid.uuid4()
        ext = "mp4"
        obj = Object(id=new_id, extension=ext,
                     bucket='test',
                     status=Status.created,
                     created=datetime.datetime.utcnow(),
                     size=humanfriendly.parse_size("1.23M", binary=True),
                     location="data/{}.{}".format(new_id, ext))
        return obj

    return create_new_obj


@pytest.fixture
def example_object(object_factory):
    return object_factory()


def test_add_and_get(index: Index, example_object: Object):
    assert index.total_entries() == 0
    index.insert(example_object)
    assert index.total_entries() == 1
    obj = index.get(example_object.id)
    assert obj.location == 'data/{}.mp4'.format(obj.id)
    assert index.total_size() == obj.size
    size, oldest = index.get_oldest_with_size_exceeding(100)
    assert oldest[0].id == obj.id
    assert size == 1289748

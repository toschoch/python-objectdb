import pytest
from api.services.index import CSVIndex
from api.models import Object
import humanfriendly


@pytest.fixture
def index():
    return CSVIndex()


@pytest.fixture
def example_object():
    obj = Object.new()
    obj.extension = "mp4"
    obj.size = humanfriendly.parse_size("1.23M", binary=True)
    obj.location = "data/{}.{}".format(obj.id, obj.extension)
    return obj


def test_add_and_get(index, example_object):
    assert index.total_entries() == 0
    index.insert_or_update(example_object)
    assert index.total_entries() == 1
    obj = index.get(example_object.id)
    assert obj.location == 'data/{}.mp4'.format(obj.id)
    assert index.total_size() == obj.size
    size, oldest = index.get_oldest_with_size_exceeding(100)
    assert oldest[0].id == obj.id
    assert size == 1289748



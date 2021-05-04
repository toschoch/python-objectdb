import humanfriendly
import pytest

from api.services.indices import Index, InMemoryIndex
from api.services.storage import Storage, FileStorage
from api.services.buffer import MaxSizeQueue

from api.models import Object, NewObject

from .test_inmemoryindex import object_factory, example_object

@pytest.fixture
def index() -> Index:
    return InMemoryIndex()


@pytest.fixture
def storage(tmpdir) -> Storage:
    return FileStorage(base_path=tmpdir)


def test_reserve(index, storage, example_object):
    deque = MaxSizeQueue("1M", "450k", "10k", index, storage)
    example_object.size = None
    deque.append(example_object)
    assert deque.size() == humanfriendly.parse_size("450k", binary=True)


def test_append(index, storage, example_object):
    deque = MaxSizeQueue("1M", "450k", "10k", index, storage)
    example_object.size = None
    deque.append(example_object)


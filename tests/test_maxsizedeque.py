import humanfriendly
import pytest

from api.services.index import Index, InMemoryIndex
from api.services.storage import Storage, FileStorage
from api.services.buffer import MaxSizeQueue

from api.models import Object, NewObject


@pytest.fixture
def index() -> Index:
    return InMemoryIndex()


@pytest.fixture
def storage(tmpdir) -> Storage:
    return FileStorage(base_path=tmpdir)


def test_reserve(index, storage):
    deque = MaxSizeQueue("1M", "450k", "10k", index, storage)
    deque.append(Object.new(NewObject(bucket='test')))
    assert deque.size() == humanfriendly.parse_size("450k", binary=True)


def test_append(index, storage):
    deque = MaxSizeQueue("1M", "450k", "10k", index, storage)
    deque.append(Object.new(NewObject(bucket='test')))


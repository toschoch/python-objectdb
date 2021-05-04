import datetime
import pickle
from pathlib import Path
from random import random
import time

import pytest

from api.services.storage import Storage, FileStorage
from api.models import NewObjectToStore, NewObject


@pytest.fixture
def storage(tmpdir) -> Storage:
    return FileStorage(base_path=tmpdir)


def test_create(storage):
    obj = NewObjectToStore.new(NewObject(bucket='test', extension='dat'))
    obj = storage.create(obj)
    p = Path(obj.location)

    assert p.parent.is_dir()
    assert p.parent.exists()
    assert not storage.exists(obj)


def test_info(storage):
    obj = NewObjectToStore.new(NewObject(bucket='test', extension='dat'))
    obj = storage.create(obj)

    p = Path(obj.location)

    t_before = datetime.datetime.utcnow()
    payload = [random() for r in range(10000)]
    with open(obj.location, 'wb+') as fp:
        pickle.dump(payload, fp)

    assert storage.exists(obj)

    obj = storage.update_info(obj)

    assert obj.size == p.stat().st_size
    assert t_before < obj.created


def test_rename(storage):
    obj = NewObjectToStore.new(NewObject(bucket='test', extension='dat'))
    obj = storage.create(obj)

    t = datetime.datetime.utcnow()
    payload = [random() for r in range(10000)]
    with open(obj.location, 'wb+') as fp:
        pickle.dump(payload, fp)

    obj.meta = {'mytag': 'myvalue'}
    obj.size = 123123
    obj.filename_template = '{ meta[mytag] }_{ size }_{ created.strftime("%Y") }'

    obj = storage.rename(obj)
    p = Path(obj.location)

    assert p.name == "myvalue_123123_{}_{}.dat".format(t.year, obj.id)
    assert p.parent.name == 'test'


def test_delete(storage):
    obj = NewObjectToStore.new(NewObject(bucket='test', extension='dat'))
    obj = storage.create(obj)

    payload = [random() for r in range(10000)]
    with open(obj.location, 'wb+') as fp:
        pickle.dump(payload, fp)

    assert storage.exists(obj)
    storage.delete(obj)
    assert not storage.exists(obj)

    p = Path(obj.location)
    assert not p.exists()

    storage.delete(obj)


def test_free_space(storage, tmp_path):

    free1 = storage.free_space()

    p = tmp_path.joinpath('test.dat')

    payload = [random() for r in range(1000000)]
    with open(p, 'wb+') as fp:
        pickle.dump(payload, fp)

    free2 = storage.free_space()



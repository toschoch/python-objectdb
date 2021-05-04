#!/usr/bin/env python

"""Tests for `objectdb` package."""
import datetime
from dateutil.parser import parse
import pickle
import random

from fastapi.testclient import TestClient
import pytest
import yaml
import os
import time
from pathlib import Path

from api.app import app
from api.services.indices import InMemoryIndex
from api.services.storage import FileStorage


@pytest.fixture
def buckets_config_file(tmp_path):
    d = {
        'buckets': [
            {
                'name': 'mytest',
                'mimetype': 'application/octet-stream',
                'extension': 'mat',
                'filename_template': "{ date.strftime('%Y%m%dT%H%M%SZ')  }",
                'meta': {
                    'system': 'test'
                },
                'storage': {
                    'usual_object_size': '100k',
                    'margin_size': '1M',
                    'max_size': {
                        'absolute': '2M'
                    }
                }

            }
        ]}

    file = tmp_path.joinpath('buckets.yml')
    with open(file, 'w+') as fp:
        yaml.dump(d, fp)

    os.environ['BUCKETS_CONFIG'] = str(file)
    return file


@pytest.fixture
def test_client(buckets_config_file, tmp_path):
    app.container.index.override(InMemoryIndex())
    app.container.storage.override(FileStorage(base_path=tmp_path))

    return TestClient(app)


def test_get_buckets(test_client):
    r = test_client.get('/buckets')
    assert r.status_code == 200
    r = r.json()
    assert r[0]['meta']['system'] == 'test'


def test_get_objects(test_client):
    r = test_client.get('/objects')
    assert r.status_code == 200


def test_new_object(test_client):
    r = test_client.put('/objects', json={'bucket': 'mytest'})
    assert r.status_code == 200
    r = r.json()
    assert r['meta']['system'] == 'test'


def test_new_object_update_and_get(test_client):
    r = test_client.put('/objects', json={'bucket': 'mytest'})
    assert r.status_code == 200
    r = r.json()
    s = 23423423
    update_obj = {'id': r['id'], 'size': s, 'meta': {'myspecialtag': 'tag'}}

    r = test_client.put('/objects', json=update_obj)
    assert r.status_code == 200

    r = test_client.get('/objects/{}'.format(update_obj['id']))
    assert r.status_code == 200
    r = r.json()

    assert r['meta']['system'] == 'test'
    assert r['meta']['myspecialtag'] == 'tag'
    assert r['size'] == s


def test_new_object_and_finalize_get(test_client, tmp_path):
    r = test_client.put('/objects', json={'bucket': 'mytest'})
    assert r.status_code == 200
    r = r.json()
    assert r['status'] == 'created'

    payload = [random.random() for r in range(10000)]
    fname = tmp_path.joinpath(r['location'])
    with open(fname, 'wb+') as fp:
        pickle.dump(payload, fp)

    r = test_client.post('/objects/finalize', json={'id': r['id'], 'date': time.time(), 'meta': {'type': 'special_data'}})
    assert r.status_code == 200
    r = r.json()

    r2 = test_client.get('/objects')
    assert r2.status_code == 200
    assert len(r2.json()) == 1

    r = test_client.get('/objects/{}'.format(r['id']))
    assert r.status_code == 200
    r = r.json()

    assert r['status'] == 'written'
    date = parse(r['date'])
    assert Path(r['location']).name.startswith(date.strftime('%Y%m%dT%H%M%SZ'))




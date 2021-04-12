from typing import List

from jinja2 import Environment, BaseLoader, DebugUndefined
import yaml
import os


def get_buckets() -> List[dict]:
    """ loads the buckets configuration from file """

    with open('config/buckets.yml', 'r') as fp:
        content = fp.read()

    variables = {'ENVIRONMENT': os.environ}

    buckets = yaml.safe_load(Environment(loader=BaseLoader,
                                         undefined=DebugUndefined)
                             .from_string(content)
                             .render(variables))['buckets']

    validate_buckets(buckets)

    return buckets


def validate_buckets(buckets: List[dict]):
    """ validates the buckets configuration """

    assert all('name' in b for b in buckets)
    assert len(set(b['name'] for b in buckets)) == len(buckets)

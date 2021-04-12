
from dependency_injector import containers, providers

from .services import Storage, get_buckets


class Container(containers.DeclarativeContainer):

    buckets_config = providers.Object(
        get_buckets
    )

    storage = providers.Factory(
        Storage
    )



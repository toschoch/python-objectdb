
from dependency_injector import containers, providers

from .services import CSVIndex, Storage, Buckets


class Container(containers.DeclarativeContainer):

    buckets = providers.Factory(
        Buckets
    )

    storage = providers.Factory(
        Storage
    )

    index = providers.Singleton(
        CSVIndex
    )



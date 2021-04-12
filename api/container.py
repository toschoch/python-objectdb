
from dependency_injector import containers, providers

from .services import CSVIndex, FileStorage, Buckets, MaxSizeDeque


class Container(containers.DeclarativeContainer):

    buckets = providers.Factory(
        Buckets
    )

    storage = providers.Factory(
        FileStorage
    )

    deque = providers.Factory(
        MaxSizeDeque,
        buckets

    )

    index = providers.Singleton(
        CSVIndex
    )




from dependency_injector import containers, providers

from .services import Logic, CSVIndex, FileStorage, Buckets, MaxSizeQueue


class Container(containers.DeclarativeContainer):

    buckets = providers.Factory(
        Buckets
    )

    storage = providers.Factory(
        FileStorage
    )

    index = providers.Singleton(
        CSVIndex
    )

    buffer = providers.Factory(
        MaxSizeQueue,
        '1M', '300k', '20k',
        index, storage
    )

    logic = providers.Factory(
        Logic,
        buckets, buffer, index, storage
    )




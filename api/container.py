import os
from pathlib import Path
from dependency_injector import containers, providers

from .services import Logic, FeatherIndex, FileStorage, Buckets, MaxSizeQueue


class Container(containers.DeclarativeContainer):

    storage = providers.Factory(
        FileStorage
    )

    index = providers.Factory(
        FeatherIndex,
        Path(os.environ.get("INDEX_FILE",
                            Path(os.environ.get("DATA_DIRECTORY", "/data")).joinpath(".index.parquet")))
    )

    buffer = providers.Factory(
        MaxSizeQueue,
        '1M', '300k', '20k',
        index, storage
    )

    buckets = providers.Factory(
        Buckets,
        index,
        storage
    )

    logic = providers.Factory(
        Logic,
        buckets, buffer, index, storage
    )




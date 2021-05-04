import os
from pathlib import Path
from dependency_injector import containers, providers

from .services import Logic, PickleIndex, FeatherIndex, FileStorage, Buckets, MaxSizeQueue


class Container(containers.DeclarativeContainer):

    storage = providers.Factory(
        FileStorage
    )

    index = providers.Factory(
        PickleIndex,
        Path(os.environ.get("INDEX_FILE",
                            Path(os.environ.get("DATA_DIRECTORY", "/data")).joinpath("index.pickle")))
    )

    buckets = providers.Factory(
        Buckets,
        index,
        storage
    )

    logic = providers.Factory(
        Logic,
        buckets, index, storage
    )




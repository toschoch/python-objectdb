from abc import ABC, abstractmethod
from pathlib import Path
import shutil
import os
from datetime import datetime

from ..models import Object


class Storage(ABC):

    @abstractmethod
    def exists(self, obj: Object) -> bool:
        pass

    @abstractmethod
    def create(self, obj: Object) -> Object:
        pass

    @abstractmethod
    def finalize(self, obj: Object) -> Object:
        pass

    @abstractmethod
    def free_space(self) -> int:
        pass

    @abstractmethod
    def update_info(self, obj: Object) -> Object:
        pass

    @abstractmethod
    def delete(self, obj: Object):
        pass


class FileStorage(Storage):

    def __init__(self, base_path="/data"):
        self.base_path = Path(base_path)

    def create(self, obj: Object) -> Object:
        obj.location = str(self.base_path.joinpath("{}/{}.{}".format(obj.bucket, obj.id, obj.extension)))
        obj.created = datetime.utcnow()
        return obj

    def finalize(self, obj: Object) -> Object:
        pass

    def update_info(self, obj: Object) -> Object:
        obj.size = os.path.getsize(obj.location)
        obj.creation = datetime.fromtimestamp(os.path.getctime(obj.location))
        if obj.date is None:
            obj.date = obj.creation
        return obj

    def delete(self, obj: Object):
        os.remove(obj.location)

    def exists(self, obj: Object) -> bool:
        return Path(obj.location).exists()

    def free_space(self) -> int:
        return shutil.disk_usage(self.base_path).free

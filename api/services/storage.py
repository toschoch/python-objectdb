from abc import ABC, abstractmethod

from pathlib import Path
import shutil
import os
from datetime import datetime

from ..utils import PartialFormatter
from ..models import Object, NewObjectToStore


class Storage(ABC):

    @abstractmethod
    def exists(self, obj: Object) -> bool:
        pass

    @abstractmethod
    def create(self, obj: NewObjectToStore) -> Object:
        pass

    @abstractmethod
    def rename(self, obj: Object) -> Object:
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

    def __init__(self, base_path=os.environ.get("DATA_DIRECTORY", "/data")):
        self.base_path = Path(base_path)

    def _default_location(self, obj: Object) -> str:
        return str(self.base_path.joinpath("{}/{}.{}".format(obj.bucket, obj.id, obj.extension)))

    def create(self, obj: NewObjectToStore) -> Object:

        obj = Object(location=self._default_location(obj),
                     created=datetime.utcnow(),
                     **obj.dict())

        path = Path(obj.location)
        path.parent.mkdir(parents=True, exist_ok=True)
        return obj

    def rename(self, obj: Object) -> Object:
        filename = PartialFormatter().format(obj.filename_template,
                                             **obj.dict(exclude={'filename_template'}))

        old_location = obj.location

        if filename != "":
            obj.location = str(self.base_path
                               .joinpath("{}/{}_{}.{}".format(obj.bucket, filename, obj.id, obj.extension)))
        else:
            obj.location = self._default_location(obj)

        if obj.location != old_location:
            os.rename(old_location, obj.location)
        return obj

    def update_info(self, obj: Object) -> dict:
        obj.size = os.path.getsize(obj.location)
        obj.created = datetime.fromtimestamp(os.path.getctime(obj.location))
        return obj

    def delete(self, obj: Object):
        p = Path(obj.location)
        if p.exists():
            p.unlink()

    def exists(self, obj: Object) -> bool:
        return Path(obj.location).exists()

    def free_space(self) -> int:
        return shutil.disk_usage(self.base_path).free


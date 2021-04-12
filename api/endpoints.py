from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException

from dependency_injector.wiring import inject, Provide

from .container import Container
from .services import Index, Buckets
from .models import NewObject, Object, Bucket

router = APIRouter()


@router.get('/buckets', response_model=List[Bucket])
@inject
async def buckets_get(buckets: Buckets = Depends(Provide[Container.buckets])) -> List[Bucket]:
    """ returns all buckets configured """
    return buckets.get()


@router.get('/object', response_model=List[Object])
@inject
def objects_get(bucket: Optional[str] = None,
                index: Index = Depends(Provide[Container.index]),
                buckets: Buckets = Depends(Provide[Container.buckets])) -> List[Object]:
    """
    searches for objects
    """
    if not bucket:
        return index.get_all()

    buckets.validate_bucket(bucket)

    return index.get_all(bucket)


@router.put('/object', response_model=Object)
@inject
async def object_put(obj: Union[Object, NewObject],
                     request: Request,
                     index: Index = Depends(Provide[Container.index]),
                     buckets: Buckets = Depends(Provide[Container.buckets])) -> Object:
    """  create or update object """
    if isinstance(obj, NewObject):
        buckets.validate_bucket(obj.bucket)
        if 'id' in await request.json():
            raise HTTPException(400, {
                "loc": [
                    "body",
                    "id"
                ],
                "msg": "value is not a valid object id",
                "type": "type_error.uuid"
            })

        obj = Object.new(obj)

    index.insert_or_update(obj)

    return obj


@router.get('/object/{id}', response_model=Object)
def object_get(id: UUID) -> Object:
    """
    get an object
    """
    pass


@router.delete('/object/{id}', response_model=None)
def object_delete(id: UUID) -> None:
    """
    deletes an object
    """
    pass


@router.post('/object/{id}/finalize', response_model=Object)
def object_finalize_by_id(id: UUID) -> Object:
    """
    mark objected as completely written
    """
    pass


@router.post('/object/finalize', response_model=Object)
def object_finalize(obj: Object) -> Object:
    """
    mark objected as completely written
    """
    pass


@router.post('/object/rename', response_model=Object)
def object_rename(obj: Object) -> Object:
    """
    rename object
    """
    pass

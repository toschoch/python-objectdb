from typing import List, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException

from dependency_injector.wiring import inject, Provide

from .container import Container
from .services import Index, Buckets, Storage, Logic
from .models import NewObject, Object, Bucket

router = APIRouter()


@router.get('/buckets', response_model=List[Bucket])
@inject
async def buckets_get(buckets: Buckets = Depends(Provide[Container.buckets])) -> List[Bucket]:
    """ returns all buckets configured """
    return buckets.get_all()


@router.get('/objects', response_model=List[Object])
@inject
async def objects_get(bucket: Optional[str] = None,
                      index: Index = Depends(Provide[Container.index]),
                      buckets: Buckets = Depends(Provide[Container.buckets])) -> List[Object]:
    """
    searches for objects
    """
    if not bucket:
        return index.get_all()

    buckets.validate_bucket(bucket)

    return index.get_all(bucket)


@router.put('/objects', response_model=Object)
@inject
async def object_put(obj: Union[Object, NewObject],
                     request: Request,
                     logic: Logic = Depends(Provide[Container.logic]),
                     buckets: Buckets = Depends(Provide[Container.buckets])) -> Object:
    """  create or update object """

    if type(obj) == NewObject:
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

        obj = logic.create_object(obj)

    else:
        try:
            obj = logic.update_object(obj)
        except KeyError:
            raise HTTPException(404, {"detail": "object not found"})

    return obj


@router.get('/objects/{id}', response_model=Object)
@inject
async def object_get(id: UUID, index: Index = Depends(Provide[Container.index])) -> Object:
    """
    get an object
    """
    try:
        return index.get(id)
    except KeyError:
        raise HTTPException(404, {"detail": "object not found"})


@router.delete('/objects/{id}', response_model=None, status_code=204)
@inject
async def object_delete(id: UUID,
                        logic: Logic = Depends(Provide[Container.logic])) -> None:
    """
    deletes an object
    """
    try:
        logic.delete_object(id)
    except KeyError:
        pass


@router.post('/objects/{id}/finalize', response_model=Object)
@inject
async def object_finalize_by_id(id: UUID,
                                index: Index = Depends(Provide[Container.index]),
                                logic: Logic = Depends(Provide[Container.logic])) -> Object:
    """
    mark objected as completely written
    """
    try:
        obj = index.get(id)
        return logic.finalize_object(obj)
    except (KeyError, FileNotFoundError):
        raise HTTPException(404, {"detail": "object not found"})


@router.post('/objects/finalize', response_model=Object)
@inject
async def object_finalize(obj: Object,
                          logic: Logic = Depends(Provide[Container.logic])) -> Object:
    """
    mark objected as completely written
    """
    try:
        return logic.finalize_object(obj)
    except (KeyError, FileNotFoundError):
        raise HTTPException(404, {"detail": "object not found"})



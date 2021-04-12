
from typing import List, Optional, Union
from uuid import UUID

from fastapi import Query
from fastapi import APIRouter, Depends
from pydantic import conint
from dependency_injector.wiring import inject, Provide
from dependency_injector.providers import Callable

from .container import Container
from .models import Object, Bucket

router = APIRouter()


@router.get('/buckets', response_model=List[Bucket])
@inject
async def api_buckets_get(buckets_config: Callable = Depends(Provide[Container.buckets_config])) -> List[Bucket]:
    """ returns all buckets configured """
    return buckets_config()


@router.get('/object', response_model=List[Object])
def get_object(
    search_string: Optional[str] = Query(None, alias='searchString'),
    skip: Optional[conint(ge=0)] = None,
    limit: Optional[conint(ge=0, le=50)] = None,
) -> List[Object]:
    """
    searches for objects
    """
    pass


@router.put('/object', response_model=Union[Object, List[Object]])
def put_object(body: Object = None) -> Union[Object, List[Object]]:
    """  create or update object """
    pass


@router.get('/object/{id}', response_model=Object)
def api_objects_get(id: UUID) -> Object:
    """
    get an object
    """
    pass


@router.delete('/object/{id}', response_model=None)
def api_objects_delete(id: UUID) -> None:
    """
    delets an object
    """
    pass


@router.post('/object/{id}/finalize', response_model=None)
def api_objects_finalize(id: UUID) -> None:
    """
    mark objected as completly written
    """
    pass


@router.post('/object/{id}/rename', response_model=None)
def api_objects_rename(id: UUID) -> None:
    """
    rename object
    """
    pass

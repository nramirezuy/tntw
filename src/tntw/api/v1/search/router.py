from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import status

from ..database import create_indices
from ..database import get_session
from ..dependencies import ElasticsearchClientDep
from . import service


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_session() as elasticsearch_client:
        async for ok, index in create_indices(elasticsearch_client):
            ...
        yield


router = APIRouter(prefix="/search", tags=["Search"], lifespan=lifespan)


@router.put("/movies", status_code=status.HTTP_201_CREATED)
async def update_movies(elasticsearch_client: ElasticsearchClientDep):
    """Update movies index"""
    return await service.update_movies(client=elasticsearch_client)


@router.get("/movies", status_code=status.HTTP_200_OK)
async def search_movies(elasticsearch_client: ElasticsearchClientDep):
    """Search movies"""
    return await service.search_movies(client=elasticsearch_client)

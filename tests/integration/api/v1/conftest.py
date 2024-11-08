from typing import AsyncIterator

import httpx
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tntw.api.v1.config import get_settings


@pytest.fixture
def minimal_environment(monkeypatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")


@pytest.fixture
def settings(minimal_environment) -> None:
    return get_settings()


@pytest_asyncio.fixture
async def elasticsearch_client(settings) -> AsyncIterator[AsyncElasticsearch]:
    database_url = str(settings.DATABASE_URL)
    async with AsyncElasticsearch(hosts=[database_url]) as client:
        yield client


@pytest_asyncio.fixture
async def http_client(settings) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client

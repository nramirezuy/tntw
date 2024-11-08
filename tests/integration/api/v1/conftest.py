from typing import AsyncIterable

import httpx
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from tntw.api.v1.database import get_session


@pytest.fixture
def minimal_environment(monkeypatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")


@pytest.fixture
def elasticsearch_client(minimal_environment) -> AsyncElasticsearch:
    return get_session()


@pytest_asyncio.fixture
async def http_client(
    minimal_environment,
) -> AsyncIterable[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client

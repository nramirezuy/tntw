from typing import AsyncIterator

import pytest
from elasticsearch import AsyncElasticsearch

from tntw.api.v1 import database


@pytest.mark.asyncio
async def test_create_indices(
    elasticsearch_client: AsyncElasticsearch,
) -> None:
    async for ok, index in database.create_indices(elasticsearch_client):
        assert ok
        assert index == "movies"


@pytest.mark.asyncio
async def test_bulk_index(elasticsearch_client: AsyncElasticsearch) -> None:
    async def create_documents() -> AsyncIterator[dict]:
        for year in range(1980, 2025):
            yield {"year": year}
            if not year % 5:
                yield {"year": year}
            if not year % 10:
                yield {"year": year}

    stats = await database.bulk_index(
        documents=create_documents(),
        index="movies",
        client=elasticsearch_client,
    )
    assert stats == (59, 0)
    await elasticsearch_client.indices.refresh(index="movies")
    assert (await elasticsearch_client.count(index="movies"))["count"] == 45
    assert (
        await elasticsearch_client.search(
            index="movies", query={"match": {"year": 2010}}
        )
    )["hits"]["total"]["value"] == 1

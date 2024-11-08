from typing import AsyncIterator

import pytest

from tntw.api.v1 import database


@pytest.mark.asyncio
async def test_create_indices(elasticsearch_client) -> None:
    async for ok, index in database.create_indices(elasticsearch_client):
        assert ok
        assert index == "movies"


@pytest.mark.asyncio
async def test_bulk_index(elasticsearch_client) -> None:
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

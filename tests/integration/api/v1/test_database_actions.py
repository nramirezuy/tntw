import pytest

from tntw.api.v1 import database


@pytest.mark.asyncio
async def test_create_indices(elasticsearch_client) -> None:
    elasticsearch_client = elasticsearch_client.options(request_timeout=30)
    async for ok, index in database.create_indices(elasticsearch_client):
        assert ok
        assert index == "movies"

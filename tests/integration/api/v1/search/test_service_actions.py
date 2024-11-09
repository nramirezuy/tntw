import pytest
from elasticsearch import AsyncElasticsearch

from tntw.api.v1.search import service


@pytest.mark.asyncio
async def test_update_movies(elasticsearch_client: AsyncElasticsearch):
    await service.update_movies(client=elasticsearch_client)
    assert (
        await elasticsearch_client.search(
            index="movies", query={"match": {"year": 2015}}
        )
    )["hits"]["total"]["value"] > 0

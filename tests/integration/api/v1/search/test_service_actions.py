import pytest
from elasticsearch import AsyncElasticsearch


@pytest.mark.asyncio
async def test_update_movies(elasticsearch_client: AsyncElasticsearch):
    # await service.update_movies(client=elasticsearch_client)
    response = await elasticsearch_client.search(
        index="movies", query={"match": {"Year": 2015}}
    )
    print(response)
    raise Exception

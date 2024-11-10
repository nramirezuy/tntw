from typing import Callable

import pytest
from conftest import MoviedataFixture
from elasticsearch import AsyncElasticsearch

from tntw.api.v1.search import service


@pytest.fixture
def moviedata(moviedata_factory: Callable) -> MoviedataFixture:
    mock = moviedata_factory(spec=service.moviedata)
    mock.patch(f"{service.__name__}.moviedata")
    yield mock


@pytest.mark.skip(reason="Requieres external resource")
@pytest.mark.asyncio
async def test_update_movies_external(
    elasticsearch_client: AsyncElasticsearch,
):
    await service.update_movies(client=elasticsearch_client)

    assert (
        await elasticsearch_client.search(
            index="movies", query={"match": {"year": 2015}}
        )
    )["hits"]["total"]["value"] > 0


@pytest.mark.asyncio
async def test_update_movies(
    moviedata: MoviedataFixture, elasticsearch_client: AsyncElasticsearch
):
    data = list(moviedata.generate_data(pages=10))
    year = data[0]["data"][0]["Year"]
    moviedata.all.send(data)
    await service.update_movies(client=elasticsearch_client)
    await elasticsearch_client.indices.refresh(index="movies")

    assert (
        await elasticsearch_client.search(
            index="movies", query={"match": {"year": year}}
        )
    )["hits"]["total"]["value"] > 0


@pytest.mark.asyncio
async def test_search_movies(
    moviedata: MoviedataFixture, elasticsearch_client: AsyncElasticsearch
):
    data = list(moviedata.generate_data(pages=10))
    moviedata.all.send(data)
    await service.update_movies(client=elasticsearch_client)
    await elasticsearch_client.indices.refresh(index="movies")
    response = await service.search_movies(client=elasticsearch_client)

    assert response["hits"]["total"]["value"] > 0

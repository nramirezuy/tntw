from typing import Callable

import pytest
from conftest import MoviedataFixture
from elasticsearch import AsyncElasticsearch

from tntw.api.v1.search import service


@pytest.fixture(autouse=True)
def moviedata(moviedata_factory: Callable) -> MoviedataFixture:
    mock = moviedata_factory(spec=service.moviedata)
    mock.patch(f"{service.__name__}.moviedata")
    yield mock


@pytest.mark.asyncio
async def test_service_update_movies(
    data_factory,
    moviedata: MoviedataFixture,
    elasticsearch_client: AsyncElasticsearch,
) -> None:
    # Would be better to add more tests and mock bulk_index here
    moviedata.all.send(data_factory(pages=10))

    await service.update_movies(client=elasticsearch_client)
    assert moviedata.all.call_count == 1
    assert moviedata.get_client.call_count == 0

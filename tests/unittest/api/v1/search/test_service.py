from typing import Callable

import pytest
from conftest import AsyncElasticsearchFixture
from conftest import MoviedataFixture

from tntw.api.v1.search import service


@pytest.fixture(autouse=True)
def moviedata(moviedata_factory: Callable) -> MoviedataFixture:
    mock = moviedata_factory(spec=service.moviedata)
    mock.patch(f"{service.__name__}.moviedata")
    yield mock


@pytest.mark.asyncio
async def test_service_update_movies(
    moviedata: MoviedataFixture,
    elasticsearch_client: AsyncElasticsearchFixture,
) -> None:
    # Would be better to add more tests and mock bulk_index here
    moviedata.all.send(moviedata.generate_data(pages=10))

    await service.update_movies(client=elasticsearch_client)
    assert moviedata.all.call_count == 1
    assert moviedata.get_client.call_count == 0
    assert elasticsearch_client.options().bulk.call_count == 1


@pytest.mark.asyncio
async def test_service_search_movies_no_parameters(
    moviedata: MoviedataFixture,
    elasticsearch_client: AsyncElasticsearchFixture,
) -> None:
    data = []
    for page in moviedata.generate_data(pages=10):
        for item in page["data"]:
            data.append({k.lower(): v for k, v in item.items()})

    elasticsearch_client.search.send(
        [{"hits": {"total": {"value": len(data)}, "hits": data}}]
    )

    await service.search_movies(client=elasticsearch_client)
    assert elasticsearch_client.search.call_count == 1
    assert elasticsearch_client.search.await_count == 1
    assert elasticsearch_client.search.call_args.kwargs["index"] == "movies"

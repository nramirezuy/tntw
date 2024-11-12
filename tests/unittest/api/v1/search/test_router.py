from typing import Callable
from typing import Iterator

import pytest
from conftest import AsyncElasticsearchFixture
from conftest import MoviedataFixture
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tntw.api.v1.dependencies import get_session
from tntw.api.v1.search import router


@pytest.fixture
def app_client(
    minimal_environment: None, elasticsearch_client: AsyncElasticsearchFixture
) -> Iterator[TestClient]:
    app = FastAPI()
    app.dependency_overrides[get_session] = lambda: elasticsearch_client
    app.include_router(router.router)
    yield TestClient(app=app)


@pytest.fixture(autouse=True)
def moviedata(moviedata_factory: Callable) -> MoviedataFixture:
    mock = moviedata_factory(spec=router.service.moviedata)
    mock.patch("tntw.api.v1.search.service.moviedata")
    yield mock


@pytest.mark.asyncio
async def test_router_update_movies(
    app_client: TestClient, moviedata: MoviedataFixture
) -> None:
    moviedata.all.send(moviedata.generate_data(pages=10))

    response = app_client.put("/search/movies")
    assert response.status_code == 201
    assert moviedata.all.call_count == 1
    assert moviedata.get_client.call_count == 0


@pytest.mark.asyncio
async def test_router_search_movies(
    app_client: TestClient,
    elasticsearch_client: AsyncElasticsearchFixture,
    moviedata: MoviedataFixture,
) -> None:
    data = []
    for page in moviedata.generate_data(pages=10):
        for item in page["data"]:
            data.append({k.lower(): v for k, v in item.items()})

    searches = [{"hits": {"total": {"value": len(data)}, "hits": data}}]
    elasticsearch_client.search.send(searches)

    response = app_client.get("/search/movies")
    assert response.status_code == 200
    assert elasticsearch_client.search.call_count == 1
    assert elasticsearch_client.search.await_count == 1
    assert elasticsearch_client.search.call_args.kwargs["index"] == "movies"
    assert response.json() == searches[0]

from typing import Callable
from typing import Iterator

import pytest
from conftest import MoviedataFixture
from fastapi import FastAPI
from fastapi.testclient import TestClient

from tntw.api.v1.search import router


@pytest.fixture
def app_client(minimal_environment: None) -> Iterator[TestClient]:
    app = FastAPI()
    app.include_router(router.router)
    yield TestClient(app=app)


@pytest.fixture(autouse=True)
def moviedata(moviedata_factory: Callable) -> MoviedataFixture:
    mock = moviedata_factory(spec=router.service.moviedata)
    mock.patch("tntw.api.v1.search.service.moviedata")
    yield mock


@pytest.mark.asyncio
async def test_router_routes(
    data_factory, app_client: TestClient, moviedata: MoviedataFixture
) -> None:
    moviedata.all.send(data_factory(pages=10))

    response = app_client.put("/search/movies")
    assert response.status_code == 201
    assert moviedata.all.call_count == 1
    assert moviedata.get_client.call_count == 0

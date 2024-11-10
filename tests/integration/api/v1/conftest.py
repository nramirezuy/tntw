import random
from collections import deque
from typing import AsyncIterator
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Iterator
from unittest.mock import MagicMock

import httpx
import pytest
import pytest_asyncio
from elasticsearch import AsyncElasticsearch
from pytest_mock.plugin import MockerFixture

from tntw.api.v1.config import get_settings


@pytest.fixture
def minimal_environment(monkeypatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")


@pytest.fixture
def settings(minimal_environment) -> None:
    return get_settings()


@pytest_asyncio.fixture
async def elasticsearch_client(settings) -> AsyncIterator[AsyncElasticsearch]:
    database_url = str(settings.DATABASE_URL)
    async with AsyncElasticsearch(hosts=[database_url]) as client:
        yield client

        # Clean all indices
        for index in await client.indices.get(index="*"):
            await client.indices.delete(index=index)


@pytest_asyncio.fixture
async def http_client(settings) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client


# DUPLICATED CODE! (from: tests/unittest/conftest.py)
class MockedClient(MagicMock):
    def patch(self, target: str) -> None:
        self.mocker.patch(target=target, new=self)

    def _protocol(self) -> Generator[dict | None, Iterable[dict] | None, None]:
        # Could have exposed the deque directly maybe,
        # but this is cooler and I'm having fun (:

        dataq: deque = deque()
        dataq.append(None)

        def unpacker(data) -> dict | None:
            if data is None and len(dataq) == 0:
                return None

            if data is not None:
                dataq.extend(data)

            item = dataq.popleft()
            return item

        data = yield None
        if data is None:
            raise Exception("Send some data first!")

        while True:
            data = yield unpacker(data)

    def make_protocol(
        self,
    ) -> Generator[dict | None, Iterable[dict] | None, None]:
        generator = self._protocol()
        next(generator)  # initate generator // travel to first yield
        return generator


class MoviedataFixture(MockedClient):
    def configure(self, *, spec, mocker) -> None:
        self.mocker = mocker
        self.configure_all(spec=spec, mocker=mocker)

    def configure_all(self, *, spec, mocker) -> None:
        self.all = mocker.MagicMock(spec=spec.all, side_effect=self._all)
        self.all.protocol = self.make_protocol()
        self.all.send = self.all.protocol.send

    def generate_data(self, pages=10) -> Iterator[dict]:
        def name() -> str:
            return " ".join(
                (
                    random.choice(("", "The")),
                    random.choice(
                        ("Funky", "Bright", "Red", "Lazy", "Sleepy")
                    ),
                    random.choice(
                        ("Man", "Woman", "Dog", "Cat", "Super Hero", "Villain")
                    ),
                )
            ).strip()

        for page in range(1, pages + 1):
            yield {
                "data": [
                    {"Title": name(), "Year": random.randint(1980, 2024)}
                ],
                "page": page,
                "total_pages": pages,
            }

    async def _all(self):
        for data in self.all.protocol:
            if data is None:
                break
            yield data


@pytest.fixture
def moviedata_factory(mocker: MockerFixture) -> Iterator[Callable]:
    def factory(*, spec) -> MoviedataFixture:
        mock = MoviedataFixture(spec=spec)
        mock.configure(spec=spec, mocker=mocker)
        return mock

    yield factory


# END DUPLICATED CODE

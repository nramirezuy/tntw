from collections import deque
from typing import Callable
from typing import Generator
from typing import Iterable
from typing import Iterator
from unittest.mock import MagicMock

import pytest
from elasticsearch import AsyncElasticsearch
from pytest import MonkeyPatch
from pytest_mock.plugin import MockerFixture


@pytest.fixture
def minimal_environment(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")


class MoviedataFixture(MagicMock):
    def configure(self, *, spec, mocker) -> None:
        self.mocker = mocker
        self.configure_all(spec=spec, mocker=mocker)

    def configure_all(self, *, spec, mocker) -> None:
        self.all = mocker.MagicMock(spec=spec.all, side_effect=self._all)
        self.all.protocol = self._protocol()
        self.all.send = self.all.protocol.send

    def patch(self, target: str) -> None:
        self.mocker.patch(target=target, new=self)

    def _protocol(self) -> Generator[dict | None, Iterable[dict] | None, None]:
        # Could have exposed the deque directly maybe,
        # but this is cooler and I'm having fun (:
        def _inner_protocol() -> (
            Generator[dict | None, Iterable[dict] | None, None]
        ):
            dataq: deque = deque()

            def unpacker(data) -> dict | None:
                if data is None and len(dataq) == 0:
                    return None

                if data is not None:
                    dataq.extend(data)

                return dataq.popleft()

            data = yield None
            if data is None:
                raise Exception("Send some data first!")

            data = yield unpacker(data)
            while True:
                data = yield unpacker(data)
                if data is None:
                    return

        generator = _inner_protocol()
        next(generator)  # initate generator // travel to first yield
        return generator

    async def _all(self):
        for data in self.all.protocol:
            yield data


@pytest.fixture
def moviedata_factory(mocker: MockerFixture) -> Iterator[Callable]:
    def factory(*, spec) -> MoviedataFixture:
        mock = MoviedataFixture(spec=spec)
        mock.configure(spec=spec, mocker=mocker)
        return mock

    yield factory


@pytest.fixture
def data_factory() -> Callable:
    def factory(pages=10):
        for page in range(1, pages + 1):
            yield {
                "data": [],
                "page": page,
                "total_pages": pages,
            }

    return factory


@pytest.fixture(autouse=True)
def elasticsearch_client(
    mocker: MockerFixture,
) -> Iterator[AsyncElasticsearch]:
    yield mocker.MagicMock(spec=AsyncElasticsearch)

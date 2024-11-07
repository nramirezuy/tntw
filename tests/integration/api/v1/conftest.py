import pytest

from tntw.api.v1.database import get_session


@pytest.fixture
def minimal_environment(monkeypatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")


@pytest.fixture
def elasticsearch_client(minimal_environment) -> None:
    return get_session()

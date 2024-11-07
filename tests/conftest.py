import pytest


@pytest.fixture
def minimal_environment(monkeypatch) -> None:
    monkeypatch.setenv("TNTW_DATABASE_URL", "http://localhost:9200")

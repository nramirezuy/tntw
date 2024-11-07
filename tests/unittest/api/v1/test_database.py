from elasticsearch import AsyncElasticsearch

from tntw.api.v1.database import get_session


def test_get_session_is_async(minimal_environment):
    assert isinstance(get_session(), AsyncElasticsearch)


def test_get_session_is_singleton(minimal_environment):
    assert get_session() is get_session()

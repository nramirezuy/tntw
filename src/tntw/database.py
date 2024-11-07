import functools

from elasticsearch import AsyncElasticsearch

from .config import get_settings


@functools.lru_cache(maxsize=1)
def get_session() -> AsyncElasticsearch:
    settings = get_settings()
    database_url = str(settings.DATABASE_URL)
    # Apparently I only need a single client
    return AsyncElasticsearch(hosts=[database_url])

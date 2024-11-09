import functools
import hashlib
from typing import Any
from typing import AsyncIterator

from elasticsearch import AsyncElasticsearch
from elasticsearch import BadRequestError
from elasticsearch.helpers import async_bulk

from .config import get_settings


@functools.lru_cache(maxsize=1)
def get_session() -> AsyncElasticsearch:
    settings = get_settings()
    database_url = str(settings.DATABASE_URL)
    # Apparently I only need a single client
    return AsyncElasticsearch(hosts=[database_url])


async def create_indices(
    client: AsyncElasticsearch,
) -> AsyncIterator[tuple[bool, str] | None]:
    """Create all necessary indices

    Returns:
        (ok, index): Returns state of the index and index name.
    """
    mappings = {
        "properties": {
            "title": {"type": "wildcard"},
            "year": {"type": "short"},
            "imdb_id": {"type": "keyword"},
        }
    }
    try:
        response = await client.indices.create(
            index="movies", mappings=mappings
        )
        yield response["acknowledged"], response["index"]
    except BadRequestError as exc:
        if exc.error != "resource_already_exists_exception":
            raise
        yield True, "movies"


async def bulk_index(
    documents: AsyncIterator[dict[str, Any]],
    index: str,
    client: AsyncElasticsearch,
) -> tuple[int, int]:
    """Index all documents to :index:

    Returns:
        (succesful, failed): Returns all succesful/failed documents.
    """
    return await async_bulk(
        client=client,
        actions=(
            {
                "_index": index,
                "_id": hashlib.sha256(repr(document).encode()).hexdigest(),
                "_source": document,
            }
            async for document in documents
        ),
        stats_only=True,
    )  # type: ignore

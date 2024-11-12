from elasticsearch import AsyncElasticsearch

from ..crawlers import moviedata
from ..database import bulk_index


async def update_movies(client: AsyncElasticsearch):
    async def genitems():
        async for data in moviedata.all():
            for item in data["data"]:
                yield {k.lower(): v for k, v in item.items()}

    return await bulk_index(
        documents=genitems(), index="movies", client=client
    )


async def search_movies(
    client: AsyncElasticsearch,
    q: str | None = None,
):
    return await client.search(index="movies", q=q)

import functools
import itertools
from typing import AsyncIterator

import httpx


@functools.lru_cache(maxsize=1)
def get_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url="https://jsonmock.hackerrank.com/api/moviesdata/search"
    )


async def all() -> AsyncIterator[dict]:
    client = get_client()
    for page in itertools.count(1):
        response = await client.get("", params={"page": page})
        response.raise_for_status()

        data = response.json()
        yield data

        if data["page"] >= data["total_pages"]:
            break

from typing import Annotated

from fastapi import Depends

from .database import AsyncElasticsearch
from .database import get_session


ElasticsearchClientDep = Annotated[AsyncElasticsearch, Depends(get_session)]

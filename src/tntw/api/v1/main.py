from fastapi import FastAPI

from .search.router import router as search_router


app = FastAPI()

app.include_router(search_router)

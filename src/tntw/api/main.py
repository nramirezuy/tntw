from fastapi import FastAPI

from .v1.main import app as v1_app


app = FastAPI()
app.mount("/v1", v1_app)


@app.get("/v1/openapi.json", name="v1", tags=["Versions"])
@app.get("/v1/docs", name="v1", tags=["Documentations"])
def noop() -> None: ...

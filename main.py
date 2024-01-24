from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends

from config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "database_url": settings.database_url,
    }

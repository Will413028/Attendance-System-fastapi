from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session

from config import Settings
import service, schemas
from database import get_db

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User,
)
def create_customer(
        user: schemas.UserCreateInput, db: Session = Depends(get_db)
):
    return service.create_user(db, user)


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "database_url": settings.database_url,
    }

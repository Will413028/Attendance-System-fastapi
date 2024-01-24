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


@app.get("/users/{id}", response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, id)
    return user


@app.get("/users", response_model=list[schemas.User | None])
def get_all_customers(db: Session = Depends(get_db)):
    return service.get_all_users(db)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_customer(user: schemas.UserCreateInput, db: Session = Depends(get_db)):
    return service.create_user(db, user)


@app.put("/users/{id}", response_model=schemas.User)
def update_customer(id: int, update_data: schemas.UserUpdateInput, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, id)
    return service.update_user(db, update_data, user)


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, id)
    service.delete_customer(db, user)


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "database_url": settings.database_url,
    }

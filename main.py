from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session

import dependencies
import models
import schemas
import service
import jwt
from config import Settings
from database import get_db

app = FastAPI()


@lru_cache
def get_settings():
    return Settings()


@app.get("/users/{id}", response_model=schemas.User)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: dict = Depends(jwt.get_current_user)):
    user = service.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@app.get("/users", response_model=list[schemas.User | None])
def get_all_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(dependency=Depends(dependencies.check_new_user)):
    user, db = dependency
    return service.create_user(db, user)


@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, update_data: schemas.UserUpdateInput, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return service.update_user(db, update_data, user)


@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    service.delete_user(db, user)


@app.post("/login", response_model=schemas.LoginReturn)
def login(user: models.User = Depends(dependencies.authenticate_user)):
    access_token = jwt.create_access_token(data={"sub": user.name, "id": user.id})
    user.token = access_token
    return user

from functools import lru_cache
from typing import Annotated, Optional
from datetime import date

from fastapi import FastAPI, status, Depends, Response, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import dependencies
import db.models as models
import schemas
import service
from utils import jwt
from config import Settings
from db.database import get_db

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


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
def get_all_users(db: Session = Depends(get_db), user_name: Optional[str] = Query(None)):
    return service.get_all_users(db, user_name=user_name)


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
def login(response: Response, user: models.User = Depends(dependencies.authenticate_user)):
    access_token = jwt.create_access_token(data={"sub": user.name, "id": user.id})
    user.token = access_token
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return user


@app.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    response.set_cookie(key="access_token", value="expired", expires=-1)
    return {"message": "Logout successful"}


@app.get("/attendances", response_model=schemas.PaginatedResponse[schemas.AttendanceRecord])
def get_all_attendance_records(db: Session = Depends(get_db), attendance_type: Optional[str] = Query(None), attendance_date: Optional[date] = Query(None), page: int = Query(1), page_size: int = Query(10)):
    return service.get_all_attendance_records(db, attendance_type=attendance_type, attendance_date=attendance_date, page=page, page_size=page_size)


@app.post("/attendances", status_code=status.HTTP_201_CREATED)
def create_attendance(settings: Annotated[Settings, Depends(get_settings)], db: Session = Depends(get_db), current_user: dict = Depends(jwt.get_current_user)):
    return service.create_attendance(db, current_user.id, settings)


@app.put("/attendances/{id}", response_model=schemas.AttendanceRecord)
def update_attendance_record(id: int, update_data: schemas.AttendanceRecordUpdateInput, db: Session = Depends(get_db)):
    attendance_record  = service.get_attendance_record_by_id(db, id)
    if not attendance_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Attendance Record not found')

    return service.update_attendance_record(db, update_data, attendance_record)

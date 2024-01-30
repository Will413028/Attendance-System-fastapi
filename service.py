from typing import Optional
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

import models
import schemas
import utils


def get_user_by_id(db: Session, id: int) -> models.User:
    query = select(models.User).where(models.User.id == id)
    user = db.execute(query).scalar()

    return user


def get_user_by_account(db: Session, account: str) -> models.User:
    query = select(models.User).where(models.User.account == account)
    user = db.execute(query).scalar()

    return user


def get_all_users(db: Session):
    query = select(models.User)

    users = db.execute(query).scalars().all()

    return users


def get_all_attendance_records(db: Session, attendance_type: Optional[str] = None, attendance_date: Optional[date] = None):
    query = select(models.AttendanceRecord)

    if attendance_type:
        query = query.filter(models.AttendanceRecord.attendance_type == attendance_type)

    if attendance_date:
        query = query.filter(func.date(models.AttendanceRecord.attendance_date) == attendance_date)

    attendance_records = db.execute(query).scalars().all()

    return attendance_records


def create_user(db: Session, user: schemas.UserCreateInput):
    user.password = utils.get_password_hash(user.password)
    db_user = models.User(**user.model_dump())

    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User create failed')
    return db_user


def update_user(db: Session, update_data: schemas.UserUpdateInput, user: models.User) -> models.User:
    update_data: dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User update failed')

    return user


def delete_user(db: Session, user: models.User):
    try:
        db.delete(user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User delete failed')
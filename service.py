from typing import Optional
from datetime import datetime, date, timedelta

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


def create_attendance(db: Session, user_id: schemas.AttendanceCreateInput, workday_cut_off_time: str):
    current_time = datetime.now()

    workday = get_workday(current_time, workday_cut_off_time)

    today_attendance_record = get_user_attendance_by_workday(db, user_id, workday)

    if today_attendance_record:
        today_attendance_record.time_out = current_time

        try:
            db.commit()
            db.refresh(today_attendance_record)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Attendance create failed')
    else:
        db_attendance_record = models.AttendanceRecord(attendance_date=workday, user_id=user_id, time_in=current_time)

        db.add(db_attendance_record)
        try:
            db.commit()
            db.refresh(db_attendance_record)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Attendance create failed')

    return 'success'


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


def get_workday(date_time, workday_cutoff_str):

    workday_cutoff = datetime.strptime(workday_cutoff_str, '%H:%M').time()

    if date_time.time() < workday_cutoff:
        workday = date_time.date() - timedelta(days=1)
    else:
        workday = date_time.date()

    return workday


def get_user_attendance_by_workday(db: Session, user_id: int, workday: date) -> models.AttendanceRecord:
    query = select(models.AttendanceRecord).filter(models.AttendanceRecord.user_id == user_id, func.date(models.AttendanceRecord.attendance_date) == workday)

    attendance_record = db.execute(query).scalars().first()

    return attendance_record

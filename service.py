from typing import Optional
from datetime import datetime, date, timedelta
import requests
import math

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

import db.models as models
import schemas
from utils import auth
from utils.decorators import cache_holiday_check
from config import Settings


def get_user_by_id(db: Session, id: int) -> models.User:
    query = select(models.User).where(models.User.id == id)
    user = db.execute(query).scalar()

    return user


def get_user_by_account(db: Session, account: str) -> models.User:
    query = select(models.User).where(models.User.account == account)
    user = db.execute(query).scalar()

    return user


def get_all_users(db: Session, user_name: Optional[str] = None, page: int = 1, page_size: int = 10):
    query = select(models.User)

    if user_name:
        query = query.filter(models.User.name.like(f"%{user_name}%"))

    total_count = db.execute(select(func.count()).select_from(query.subquery())).scalar()

    offset = (page - 1) * page_size

    users = db.execute(query.offset(offset).limit(page_size)).scalars().all()

    total_pages = (total_count + page_size - 1) // page_size

    return {
        "total_count": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "data": users
    }


def get_all_attendance_records(db: Session, attendance_type: Optional[str] = None, attendance_date: Optional[date] = None, page: int = 1, page_size: int = 10):
    query = select(models.AttendanceRecord)

    if attendance_type:
        query = query.filter(models.AttendanceRecord.attendance_type == attendance_type)

    if attendance_date:
        query = query.filter(func.date(models.AttendanceRecord.attendance_date) == attendance_date)

    total_count = db.execute(select(func.count()).select_from(query.subquery())).scalar()

    offset = (page - 1) * page_size

    attendance_records = db.execute(query.offset(offset).limit(page_size)).scalars().all()

    total_pages = (total_count + page_size - 1) // page_size

    return {
        "total_count": total_count,
        "total_pages": total_pages,
        "current_page": page,
        "data": attendance_records
    }


def create_user(db: Session, user: schemas.UserCreateInput):
    user.password = auth.get_password_hash(user.password)
    db_user = models.User(**user.model_dump())

    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()

        error_message = str(e)
        print(error_message)

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User create failed: {error_message}'
        )

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


def get_attendance_record_by_id(db: Session, id: int) -> models.AttendanceRecord:
    query = select(models.AttendanceRecord).where(models.AttendanceRecord.id == id)
    attendance_record = db.execute(query).scalar()

    return attendance_record


def create_attendance(db: Session, user_id: schemas.AttendanceRecordUpdateInput, config: Settings):
    message = None

    current_time = datetime.now()

    workday = get_workday(current_time, config.workday_cut_off_time)

    if is_weekend(workday) or is_holiday(workday, config.country, config.holidays_api_key, config.holidays_api_url):
        raise HTTPException(status_code=400, detail="Cannot record attendance on holidays")

    today_attendance_record = get_user_attendance_by_workday(db, user_id, workday)

    if today_attendance_record:

        today_attendance_record.time_out = current_time
        
        user_is_leave_early = is_leave_early(today_attendance_record.time_in, config.minimum_working_hours, current_time)

        if user_is_leave_early:
            today_attendance_record.attendance_type = 'Early Leave'
            message = 'User early leave'
        else:
            today_attendance_record.attendance_type = 'Present'
            message = 'User Present'

        try:
            db.commit()
            db.refresh(today_attendance_record)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Attendance create failed')
    else:
        db_attendance_record = models.AttendanceRecord(attendance_date=workday, user_id=user_id, time_in=current_time, attendance_type= 'On Time')

        db.add(db_attendance_record)
        try:
            db.commit()
            db.refresh(db_attendance_record)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Attendance create failed')
    return message


def update_attendance_record(db: Session, update_data: schemas.AttendanceRecordUpdateInput, attendance_record: models.AttendanceRecord) -> models.AttendanceRecord:
    update_data: dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(attendance_record, key, value)

    try:
        db.commit()
        db.refresh(attendance_record)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Attendance Record update failed')

    return attendance_record


def get_workday(date_time, workday_cutoff_str) -> date:

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


def is_leave_early(time_in: datetime, minimum_working_hours: int, current_time: datetime) -> bool:

    working_hours = (current_time - time_in).total_seconds() / 3600

    return working_hours < minimum_working_hours


@cache_holiday_check
def is_holiday(date: date, country: str, holidays_api_key: str, holidays_api_url: str) -> bool:
    params = {
        "api_key": holidays_api_key,
        "country": country,
        "year": date.year,
        "month": date.month,
        "day": date.day,
    }
    try:
        response = requests.get(holidays_api_url, params=params)
        response.raise_for_status()
        data = response.json()
        holidays = data.get('response', {}).get('holidays', [])

        return len(holidays) > 0
    except requests.RequestException as e:
        print(e)
        return False


def is_weekend(date: date) -> bool:
    print(date.weekday())
    return date.weekday() >= 5


def calculate_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371
    return c * r

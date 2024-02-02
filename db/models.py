from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    name = mapped_column(String(128), index=True)
    account = mapped_column(String(128), index=True)
    password = mapped_column(String(128))
    email = mapped_column(String(128), index=True)
    role = mapped_column(String(64))
    phone = mapped_column(String(64))
    error_times = mapped_column(Integer, default=0)
    attendance_records = relationship("AttendanceRecord", back_populates="user")


class AttendanceRecord(Base):
    __tablename__ = 'attendance_records'

    user_id = mapped_column(Integer, ForeignKey('users.id'))
    attendance_date = mapped_column(DateTime)
    time_in = mapped_column(DateTime)
    time_out = mapped_column(DateTime)
    attendance_type = mapped_column(String(32))
    user = relationship("User", back_populates="attendance_records")

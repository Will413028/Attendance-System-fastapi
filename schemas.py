from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime
from typing import Optional


class DateTimeBase(BaseModel):
    created_at: str
    updated_at: str

    @validator("created_at", "updated_at",  pre=True)
    def datetime_to_str(cls, v: datetime):
        if isinstance(v, datetime):
            return datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
        return str(v)


class User(DateTimeBase):
    id: int
    name: str
    account: str
    password: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class UserCreateInput(BaseModel):
    name: str = Field(max_length=30, title="User name")
    account: str = Field(max_length=100, title="Account")
    password: str = Field(max_length=64, title="Password")
    email: EmailStr
    phone: str = Field(max_length=20, title="Phone Number")


class UserUpdateInput(BaseModel):
    name: Optional[str] = Field(max_length=30, title="User name")
    account: Optional[str] = Field(max_length=100, title="Account")
    password: Optional[str] = Field(max_length=30, title="Password")
    email: Optional[EmailStr]
    phone: Optional[str] = Field(max_length=20, title="Phone Number")


class LoginInput(BaseModel):
    account: Optional[str] = Field(max_length=100, title="Account")
    password: Optional[str] = Field(max_length=30, title="Password")


class LoginReturn(User):
    token: str


class AttendanceRecord(DateTimeBase):
    id: int
    attendance_date: datetime
    time_in: datetime
    time_out: Optional[datetime] = None
    attendance_type: str
    user_id: int
    user: User

    class Config:
        from_attributes = True


class AttendanceRecordUpdateInput(BaseModel):
    attendance_date: Optional[datetime] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    attendance_type: Optional[str] = None

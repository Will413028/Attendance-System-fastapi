from pydantic import BaseModel, Field, validator
from datetime import datetime


class DateTimeBase(BaseModel):
    created_at: str
    updated_at: str

    @validator("created_at", "updated_at", pre=True)
    def datetime_to_str(cls, v: datetime):
        if isinstance(v, datetime):
            return datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
        return str(v)


class UserCreateInput(BaseModel):
    name: str = Field(max_length=30, title="User name")
    account: str = Field(max_length=100, title="Account")
    password: str = Field(max_length=30, title="Password")
    email: str = Field(max_length=50, title="Email")
    phone: str = Field(max_length=20, title="Phone Number")


class User(DateTimeBase):
    id: int
    name: str
    account: str
    password: str
    email: str
    phone: str

    class Config:
        from_attributes = True

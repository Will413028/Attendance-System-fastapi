from pydantic import BaseModel, Field


class UserCreateInput(BaseModel):
    name: str = Field(max_length=30, title="User name")
    account: str = Field(max_length=100, title="Account")
    password: str = Field(max_length=30, title="Password")
    email: str = Field(max_length=50, title="Email")
    phone: str = Field(max_length=20, title="Phone Number")


class User(BaseModel):
    id: int
    name: str
    account: str
    password: str
    email: str
    phone: str

    class Config:
        orm_mode = True

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from database import Base


class User(Base):
    __tablename__ = 'user'

    name = mapped_column(String(128), index=True)
    account = mapped_column(String(128), index=True)
    password = mapped_column(String(128))
    email = mapped_column(String(128), index=True)
    role = mapped_column(String(64))
    phone = mapped_column(String(64))
    error_times = mapped_column(Integer, default=0)

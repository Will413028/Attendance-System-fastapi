from sqlalchemy import Integer, String, Column

from database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    account = Column(String(128), index=True)
    password = Column(String(128))
    email = Column(String(128), index=True)
    role = Column(String(64))
    phone = Column(String(64))
    error_times = Column(Integer)


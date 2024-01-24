from sqlalchemy import Integer, String, Column

from database import Base


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(128), index=True)
    email = Column(String(128), index=True)
    phone = Column(String(64), index=True)
    password = Column(String(128), index=True)

    def as_dict(self):
        user_dict = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return user_dict

    def __init__(self, user_name, password, email=None, phone=None):
        self.user_name = user_name
        self.password = password
        self.email = email
        self.phone = phone

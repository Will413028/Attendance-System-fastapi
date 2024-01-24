from database import Base
from models import User


def auto_create_missing_table(engine):
    Base.metadata.create_all(engine)

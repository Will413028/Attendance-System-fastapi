from db.database import Base
from db.models import User


def auto_create_missing_table(engine):
    Base.metadata.create_all(engine)

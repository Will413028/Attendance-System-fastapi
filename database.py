from sqlalchemy import create_engine, DateTime, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.sql import func

from config import Settings

settings = Settings()

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

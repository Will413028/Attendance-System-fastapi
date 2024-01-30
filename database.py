from sqlalchemy import create_engine, DateTime, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.sql import func
from google.cloud.sql.connector import Connector

from config import Settings


class Base(DeclarativeBase):
    id = mapped_column(Integer, primary_key=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )


settings = Settings()

print(settings)

if settings.environment == 'PRODUCTION':
    connector = Connector()

    def getconn():
        conn = connector.connect(
            settings.instance_connection_name,
            "pymysql",
            user=settings.db_user,
            password=settings.db_pass,
            db=settings.db_name
        )
        return conn

    engine = create_engine("mysql+pymysql://", creator=getconn)
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

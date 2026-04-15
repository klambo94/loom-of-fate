from typing import Any, Generator

from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)



class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from agentgear.server.app.config import get_settings

settings = get_settings()

def _normalize_sqlite_url(url: str) -> str:
    if not url.startswith("sqlite"):
        return url
    prefix = "sqlite:///"
    path = url[len(prefix) :] if url.startswith(prefix) else url.removeprefix("sqlite:")
    path = os.path.expanduser(path)
    p = Path(path)
    if not p.is_absolute():
        p = Path.cwd() / p
    p.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{p}"


db_url = _normalize_sqlite_url(settings.database_url)

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

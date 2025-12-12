from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from reviewhound.config import Config

engine = None
SessionLocal = None


def get_engine():
    global engine
    if engine is None:
        db_url = Config.get_database_url()
        if "/:memory:" not in db_url:
            db_path = Path(Config.DATABASE_PATH)
            db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(db_url, echo=False)
    return engine


def get_session_factory():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(bind=get_engine())
    return SessionLocal


@contextmanager
def get_session() -> Session:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db():
    from reviewhound.models import Base
    Base.metadata.create_all(get_engine())

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import config

if config.DATABASE_DSN and "sqlite" in config.DATABASE_DSN:  # pragma: no cover
    kwargs = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool}
else:  # pragma: no cover
    kwargs = {}

engine = create_engine(config.DATABASE_DSN, **kwargs)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, binds={Base: engine})


@contextmanager
def SessionManager():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def ping_db():
    with SessionManager() as db_session:
        db_session.execute("SELECT 1", bind=engine)

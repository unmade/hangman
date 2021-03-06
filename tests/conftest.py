import pytest
from pytest_factoryboy import register
from starlette.testclient import TestClient

from app import config, db
from app.main import create_app

from . import factories

register(factories.HangmanFactory)


@pytest.fixture
def client():
    return TestClient(create_app())


@pytest.fixture(autouse=True)
def create_schema_for_in_memory_sqlite(request):
    if config.DATABASE_DSN == "sqlite://":  # pragma: no cover
        db.Base.metadata.create_all(bind=db.engine)

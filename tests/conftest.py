import pytest
from pytest_factoryboy import register
from starlette.testclient import TestClient

from app.main import create_app

from . import factories

register(factories.HangmanFactory)


@pytest.fixture
def client():
    return TestClient(create_app())

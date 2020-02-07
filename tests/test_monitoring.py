from unittest import mock

from sqlalchemy.exc import SQLAlchemyError
from starlette.testclient import TestClient


def test_ping(client: TestClient):
    response = client.get("/api/ping")
    assert response.json() == {"status": "OK"}


def test_ping_db(client: TestClient):
    response = client.get("/api/ping/db")
    assert response.json() == {"status": "OK"}


def test_status_when_db_fails(client: TestClient):
    side_effect = SQLAlchemyError(code="e3q8")  # OperationalError
    with mock.patch("app.db.ping_db", side_effect=side_effect) as ping_db_mock:
        response = client.get("/api/ping/db")
    assert response.json() == {"status": "ERROR"}
    assert ping_db_mock.called

from starlette.testclient import TestClient


def test_ping(client: TestClient):
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

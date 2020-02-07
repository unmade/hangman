from starlette.testclient import TestClient


def test_start_game(client: TestClient):
    response = client.post("/api/game", json={"word": "order", "max_attempts": 5})

    content = response.json()
    content.pop("game_uid")
    assert content == {
        "letters": ["_", "_", "_", "_", "_"],
        "lives": 5,
        "score": 0,
        "completed": False,
    }
    assert response.status_code == 201


def test_start_game_with_invalid_word(client: TestClient):
    response = client.post("/api/game", json={"word": "bad_word", "max_attempts": 5})
    assert response.json()["detail"][0]["type"] == "value_error"
    assert response.json()["detail"][0]["loc"] == ["body", "game_config", "word"]
    assert response.status_code == 422

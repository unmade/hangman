import uuid

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


def test_guess_letter(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order")
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "r"})
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["_", "r", "_", "_", "r"],
        "lives": 5,
        "score": 100,
        "completed": False,
    }


def test_guess_letter_in_a_row(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order")
    client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "r"})
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "o"})
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["o", "r", "_", "_", "r"],
        "lives": 5,
        "score": 200,
        "completed": False,
    }


def test_guess_word(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order")
    response = client.put(
        f"/api/game/{hangman.game_uid}", json={"word_or_letter": "order"}
    )
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["o", "r", "d", "e", "r"],
        "lives": 5,
        "score": 400,
        "completed": True,
    }


def test_guess_letter_for_non_existing_game(client: TestClient):
    game_uid = uuid.uuid4()
    response = client.put(f"/api/game/{game_uid}", json={"word_or_letter": "o"})
    assert response.json()["detail"] == f"Game with '{game_uid}' not found."
    assert response.status_code == 404


def test_guess_letter_incorrect(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order")
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "a"})
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["_", "_", "_", "_", "_"],
        "lives": 4,
        "score": 0,
        "completed": False,
    }


def test_guess_same_letter_second_time(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order", known_letters="r")
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "r"})
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["_", "r", "_", "_", "r"],
        "lives": 5,
        "score": 100,
        "completed": False,
    }


def test_guess_letter_incorrect_game_over(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order", attempt_count=4, max_attempts=5)
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "a"})
    assert response.json()["detail"] == "Game Over"
    assert response.status_code == 400


def test_guess_letter_game_complete(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order", known_letters="orde")
    response = client.put(f"/api/game/{hangman.game_uid}", json={"word_or_letter": "a"})
    assert response.json()["detail"] == "Game Completed"
    assert response.status_code == 400


def test_get_game(client: TestClient, hangman_factory):
    hangman = hangman_factory(word="order")
    response = client.get(f"/api/game/{hangman.game_uid}")
    assert response.json() == {
        "game_uid": str(hangman.game_uid),
        "letters": ["_", "_", "_", "_", "_"],
        "lives": 5,
        "score": 0,
        "completed": False,
    }
    assert response.status_code == 200


def test_get_non_existing_game(client: TestClient):
    game_uid = uuid.uuid4()
    response = client.get(f"/api/game/{game_uid}")
    assert response.json()["detail"] == f"Game with '{game_uid}' not found."
    assert response.status_code == 404

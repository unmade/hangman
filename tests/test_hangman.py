import pytest

from app.hangman import GameOver, Hangman, WrongGuess


def test_hangman_string_representation():
    hangman = Hangman("order")
    assert str(hangman) == "_ _ _ _ _"


def test_hangman_string_representation_with_known_letters():
    hangman = Hangman("order", known_letters={"r"})
    assert str(hangman) == "_ r _ _ r"


@pytest.mark.parametrize(
    ["word", "known_letters", "completed"],
    [
        ("order", set(), False),
        ("order", {"r"}, False),
        ("order", {"o", "r", "d", "e"}, True),
    ],
)
def test_hangman_completed(word, known_letters, completed):
    hangman = Hangman(word, known_letters=known_letters)
    assert hangman.completed is completed


@pytest.mark.parametrize(["attempt_count", "lives"], [(0, 5), (3, 2)])
def test_hangman_lives(attempt_count, lives):
    hangman = Hangman("order", attempt_count=attempt_count)
    assert hangman.lives == lives


@pytest.mark.parametrize(["attempt_count", "game_over"], [(0, False), (5, True)])
def test_hangman_is_game_over(attempt_count, game_over):
    hangman = Hangman("order", attempt_count=attempt_count)
    assert hangman.is_game_over() is game_over


@pytest.mark.parametrize(
    ["word", "known_letters", "score"],
    [
        ("order", set(), 0),
        ("order", {"o"}, 100),
        ("order", {"r"}, 100),
        ("order", {"o", "r"}, 200),
        ("order", {"o", "r", "d", "e"}, 400),
        ("print", {"p", "r", "i", "n", "t"}, 625),
    ],
)
def test_score(word, known_letters, score):
    hangman = Hangman(word, known_letters=known_letters)
    assert hangman.score == score


@pytest.mark.parametrize(
    ["word", "attempt_count", "score"],
    [("print", 0, 625), ("print", 2, 375), ("print", 4, 125), ("print", 5, 0)],
)
def test_score_depends_on_attempt(word, attempt_count, score):
    hangman = Hangman(word, known_letters=set(word), attempt_count=attempt_count)
    assert hangman.score == score


def test_hangman_guess_existing_letter():
    hangman = Hangman("order")
    assert hangman.guess("r") == "_ r _ _ r"


def test_hangman_guess_word():
    hangman = Hangman("order")
    assert hangman.guess("order") == "o r d e r"


def test_hangman_guess_wrong_letter():
    hangman = Hangman("order")
    assert hangman.attempt_count == 0

    with pytest.raises(WrongGuess):
        hangman.guess("a")

    assert hangman.attempt_count == 1


def test_hangman_guess_wrong_letter_and_game_over():
    hangman = Hangman("order", attempt_count=4)
    assert hangman.attempt_count == 4

    with pytest.raises(GameOver):
        hangman.guess("a")

    assert hangman.attempt_count == 5

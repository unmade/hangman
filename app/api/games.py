from uuid import UUID

from fastapi import APIRouter, HTTPException

from app import crud, db
from app.hangman import GameOver, Hangman, WrongGuess
from app.schemas.game import Game, GameConfig, Guess

router = APIRouter()


@router.post("/game", status_code=201, response_model=Game)
def start_game(game_config: GameConfig):
    """Start a new game of Hangman"""
    hangman = Hangman(word=game_config.word, max_attempts=game_config.max_attempts)
    with db.SessionManager() as db_session:
        crud.games.create(db_session, hangman)
    return Game.from_hangman(hangman)


@router.put("/game/{game_uid}", response_model=Game)
def guess_word_or_letter(game_uid: UUID, guess: Guess):
    """Guess letter or the whole word"""
    with db.SessionManager() as db_session:
        game = crud.games.get(db_session, game_uid)

    if game is None:
        raise HTTPException(
            status_code=404, detail=f"Game with '{game_uid}' not found."
        )

    hangman = game.load()

    try:
        hangman.guess(guess.word_or_letter)
    except GameOver as exc:
        raise HTTPException(status_code=400, detail="Game Over") from exc
    except WrongGuess:
        pass
    finally:
        with db.SessionManager() as db_session:
            crud.games.update(db_session, game, hangman)

    return Game.from_hangman(hangman)

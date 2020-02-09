from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import Session

from app import config, crud, db
from app.db.game import Game as GameModel
from app.hangman import Completed, Hangman, NoLives, WrongGuess
from app.schemas.game import Game, GameConfig, Guess

router = APIRouter()


def get_game_or_404(db_session: Session, game_uid: UUID) -> GameModel:
    game = crud.games.get(db_session, game_uid)
    if not game:
        raise HTTPException(404, detail=f"Game with '{game_uid}' not found.")
    return game


@router.post("/game", status_code=201, response_model=Game)
def start_game(
    game_config: GameConfig = Body(..., example={"lives": config.HANGMAN_LIVES})
):
    """Start a new game of Hangman"""
    hangman = Hangman(word=game_config.word, max_attempts=game_config.lives)
    with db.SessionManager() as db_session:
        crud.games.create(db_session, hangman)
    return Game.from_hangman(hangman)


@router.put(
    "/game/{game_uid}",
    response_model=Game,
    responses={
        400: {"description": "Either the Game is over or completed "},
        404: {"description": "Can't find the Game with specified 'game_uid'"},
    },
)
def guess_word_or_letter(game_uid: UUID, guess: Guess):
    """Guess letter or the whole word"""
    with db.SessionManager() as db_session:
        game = get_game_or_404(db_session, game_uid)
        hangman = game.load()

        try:
            hangman.guess(guess.word_or_letter)
        except NoLives as exc:
            raise HTTPException(status_code=400, detail="Game Over") from exc
        except Completed as exc:
            raise HTTPException(status_code=400, detail="Game Completed") from exc
        except WrongGuess:
            pass
        finally:
            crud.games.update(db_session, game, hangman)

        return Game.from_hangman(hangman)


@router.get(
    "/game/{game_uid}",
    response_model=Game,
    responses={404: {"description": "Can't find the Game with specified 'game_uid'"}},
)
def get_game(game_uid: UUID):
    """Returns game with specified game_uid"""
    with db.SessionManager() as db_session:
        game = get_game_or_404(db_session, game_uid)
    return Game.from_hangman(game.load())

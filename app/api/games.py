from fastapi import APIRouter

from app import crud, db
from app.hangman import Hangman
from app.schemas.game import Game, GameConfig

router = APIRouter()


@router.post("/game", status_code=201, response_model=Game)
def start_game(game_config: GameConfig):
    """Start a new game of Hangman"""
    hangman = Hangman(word=game_config.word, max_attempts=game_config.max_attempts)
    with db.SessionManager() as db_session:
        game = crud.games.create(db_session, hangman)
    return Game(
        game_uid=game.game_uid,
        letters=list(hangman),
        lives=hangman.lives,
        score=hangman.score,
        completed=hangman.completed,
    )

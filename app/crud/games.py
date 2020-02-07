from sqlalchemy.orm import Session

from app.db.game import Game
from app.hangman import Hangman


def create(db_session: Session, hangman: Hangman) -> Game:
    game = Game(word=hangman.word, max_attempts=hangman.max_attempts)
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game

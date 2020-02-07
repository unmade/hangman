from typing import Optional, cast
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.game import Game
from app.hangman import Hangman


def create(db_session: Session, hangman: Hangman) -> Game:
    game = Game.save(hangman)
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game


def get(db_session: Session, game_uid: UUID) -> Optional[Game]:
    game = db_session.query(Game).filter(Game.game_uid == str(game_uid)).first()
    return cast(Optional[Game], game)


def update(db_session: Session, game: Game, hangman: Hangman) -> Game:
    game = Game.save(hangman, game=game)
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game

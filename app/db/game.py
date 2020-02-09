from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import Column, Integer, String

from app.db import Base
from app.hangman import Hangman


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    game_uid = Column(String(36), unique=True, default=generate_uuid)
    word = Column(String, nullable=False)
    known_letters = Column(String, default="", nullable=False)
    score = Column(Integer, default=0, nullable=False)
    max_attempts = Column(Integer, nullable=False)
    attempt_count = Column(Integer, default=0, nullable=False)

    @classmethod
    def save(cls, hangman: Hangman, game: Optional[Game] = None) -> Game:
        if game is None:
            game = Game(game_uid=str(hangman.uid))
        assert game.game_uid == str(hangman.uid)
        fields = ("word", "score", "max_attempts", "attempt_count")
        for field in fields:
            if getattr(game, field) != getattr(hangman, field):
                setattr(game, field, getattr(hangman, field))
        known_letters = "".join(hangman.known_letters)
        if game.known_letters != known_letters:
            game.known_letters = known_letters
        return game

    def load(self) -> Hangman:
        return Hangman(
            uid=uuid.UUID(self.game_uid),
            word=self.word,
            max_attempts=self.max_attempts,
            attempt_count=self.attempt_count,
            known_letters=set(iter(self.known_letters)),
        )

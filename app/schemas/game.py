from typing import List

from pydantic import UUID4, BaseModel, validator

from app import config


class GameConfig(BaseModel):
    word: str
    max_attempts: int

    @validator("word")
    def check_word_allowance(cls, v):
        if v not in config.ALLOWED_WORDS:
            msg = f"'{v}' is not a valid choice. Must be one of: {config.ALLOWED_WORDS}"
            raise ValueError(msg)
        return v


class Game(BaseModel):
    game_uid: UUID4
    letters: List[str]
    lives: int
    score: int
    completed: bool

    @classmethod
    def from_hangman(cls, hangman):
        return cls(
            game_uid=hangman.uid,
            letters=list(hangman),
            lives=hangman.lives,
            score=hangman.score,
            completed=hangman.completed,
        )


class Guess(BaseModel):
    word_or_letter: str

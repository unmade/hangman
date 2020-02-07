import random
from typing import List, Optional

from pydantic import UUID4, BaseModel, Field, validator

from app import config


class GameConfig(BaseModel):
    word: Optional[str] = Field(
        None,
        title="The word",
        description=(
            "The word to guess. "
            f"If not provided will be chosen randomly from {config.HANGMAN_WORDS}"
        ),
    )
    max_attempts: int = Field(
        5,
        title="Number of attempts",
        description="How much user can ask letters that don't exist",
        gt=0,
    )

    @validator("word", pre=True, always=True)
    def choose_random_word_if_not_provided(cls, v):
        if v is None:
            return random.choice(config.HANGMAN_WORDS)
        return v

    @validator("word")
    def check_word_allowance(cls, v):
        words = config.HANGMAN_WORDS
        if v not in words:
            msg = f"'{v}' is not a valid choice. Must be one of: {words}"
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

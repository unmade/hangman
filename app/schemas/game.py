from __future__ import annotations

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
        min_length=3,
    )
    lives: int = Field(
        config.HANGMAN_LIVES,
        title="Total number of attempts",
        description="How many times user can ask for letters that are not in the word",
        gt=0,
    )

    @validator("word", pre=True, always=True)
    def choose_random_word_if_not_provided(cls, v: str) -> str:
        if v is None:
            return random.choice(config.HANGMAN_WORDS)
        return v

    @validator("word")
    def check_word_allowance(cls, v: str) -> str:
        words = config.HANGMAN_WORDS
        if v.lower() not in [word.lower() for word in words]:
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
    def from_hangman(cls, hangman) -> Game:
        return cls(
            game_uid=hangman.uid,
            letters=list(hangman),
            lives=hangman.lives,
            score=hangman.score,
            completed=hangman.completed,
        )


class Guess(BaseModel):
    word_or_letter: str = Field(
        ...,
        title="Letter or the whole word",
        description="A letter from the word or the whole word",
        min_length=1,
    )

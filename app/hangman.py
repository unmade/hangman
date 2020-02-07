from dataclasses import dataclass, field
from typing import Iterator, Set
from uuid import UUID, uuid4


class HangmanError(Exception):
    pass


class WrongGuess(HangmanError):
    pass


class GameOver(HangmanError):
    pass


@dataclass
class Hangman:
    word: str
    uid: UUID = field(default_factory=uuid4)
    max_attempts: int = 5
    attempt_count: int = 0
    known_letters: Set[str] = field(default_factory=set)

    def __str__(self) -> str:
        return " ".join(self)

    def __iter__(self) -> Iterator[str]:
        return (letter if letter in self.known_letters else "_" for letter in self.word)

    @property
    def completed(self) -> bool:
        return "_" not in self

    @property
    def lives(self) -> int:
        return self.max_attempts - self.attempt_count

    @property
    def score(self) -> int:
        word_score = len(set(self.word)) * len(self.word)
        return word_score * len(self.known_letters) * self.lives

    def is_game_over(self) -> bool:
        return self.lives < 1

    def guess(self, word_or_letter: str) -> str:
        if word_or_letter in self.word:
            self.known_letters.update(iter(word_or_letter))
            return str(self)
        self.attempt_count += 1
        if self.is_game_over():
            raise GameOver
        raise WrongGuess

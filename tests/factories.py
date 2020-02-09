import factory
from factory import fuzzy

from app import config, db
from app.db.game import Game


class HangmanFactory(factory.alchemy.SQLAlchemyModelFactory):
    word = fuzzy.FuzzyChoice(config.HANGMAN_WORDS)
    known_letters = ""
    attempt_count = 0
    max_attempts = config.HANGMAN_LIVES

    class Meta:
        model = Game
        sqlalchemy_session = db.SessionLocal()
        sqlalchemy_session_persistence = "commit"

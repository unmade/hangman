import factory
from factory import fuzzy

from app import config, db
from app.db.game import Game


class HangmanFactory(factory.alchemy.SQLAlchemyModelFactory):
    game_uid = factory.Faker("uuid4")
    word = fuzzy.FuzzyChoice(config.HANGMAN_WORDS)
    known_letters = ""
    attempt_count = 0
    max_attempts = 5

    class Meta:
        model = Game
        sqlalchemy_session = db.SessionLocal()
        sqlalchemy_session_persistence = "commit"

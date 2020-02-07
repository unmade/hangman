import uuid

from sqlalchemy import Column, Integer, String

from app.db import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True)
    game_uid = Column(String(32), unique=True, default=generate_uuid)
    word = Column(String)
    known_letters = Column(String, default="")
    score = Column(Integer, default=0)
    max_attempts = Column(Integer)
    attempt_count = Column(Integer, default=0)

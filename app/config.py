import os


def _get_bool(key: str) -> bool:
    value = os.getenv(key)
    if value:
        return value.lower() in ["true", "1", "t"]
    return False


APP_NAME = os.getenv("APP_NAME", "Hangman")
APP_VERSION = os.getenv("APP_VERSION")

APP_DEBUG = _get_bool("APP_DEBUG")

DATABASE_DSN = os.getenv("DATABASE_DSN")

ALLOWED_WORDS = ["3dhubs", "marvin", "print", "filament", "order", "layer"]

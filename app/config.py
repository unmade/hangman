import os
from typing import List, Optional


def _get_bool(key: str) -> bool:
    value = os.getenv(key)
    if value is not None:
        return value.lower() in ["true", "1", "t"]
    return False


def _get_list(key: str, default: Optional[List[str]] = None) -> List[str]:
    value = os.getenv(key)
    if value is not None:
        return value.split(",")
    else:
        if default is not None:
            return default
    return []


APP_NAME = os.getenv("APP_NAME", "Hangman")
APP_VERSION = os.getenv("APP_VERSION")

APP_DEBUG = _get_bool("APP_DEBUG")

DATABASE_DSN = os.environ["DATABASE_DSN"]

HANGMAN_WORDS = _get_list(
    "HANGMAN_WORDS",
    default=["3dhubs", "marvin", "print", "filament", "order", "layer"],
)
HANGMAN_LIVES = int(os.getenv("HANGMAN_LIVES", "5"))

SENTRY_DSN = os.getenv("SENTRY_DSN")

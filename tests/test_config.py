from unittest import mock

import pytest

from app import config


@pytest.mark.parametrize(
    ["given", "expected"],
    [
        ("True", True),
        ("true", True),
        ("1", True),
        ("0", False),
        ("False", False),
        (None, False),
    ],
)
def test_get_bool(given, expected):
    with mock.patch("os.getenv", return_value=given):
        value = config._get_bool("DEBUG")
    assert value == expected

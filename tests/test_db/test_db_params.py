from sqlalchemy.pool import StaticPool

from app.db import get_db_params


def test_db_params_for_sqlite():
    params = get_db_params("sqlite://")
    assert params == {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }


def test_db_params_for_postgres():
    params = get_db_params("postgres://user:password@host:port/name")
    assert params == {}

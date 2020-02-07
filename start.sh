#! /usr/bin/env sh
set -e

alembic upgrade head
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app

# Hangman

This is simple REST API to play Hangman game

[![build](https://github.com/unmade/hangman/workflows/Lint%20and%20Test/badge.svg)](https://github.com/unmade/hangman/blob/master/.github/workflows/lint-and-test.yml)
[![build](https://github.com/unmade/hangman/workflows/Deploy/badge.svg)](https://github.com/unmade/hangman/blob/master/.github/workflows/deploy.yml)

## Documentation

Check out interactive documentation [here](https://apihangman.herokuapp.com/docs)

# Development

## Running locally

Create a new virtual environment:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements/base.txt -r requirements/test.txt
```

Install pre-commit hooks:

```bash
pre-commit install
```

Set the path to db:
```bash
export DATABASE_DSN=sqlite:///./test.db
```

Run the app:

```bash
uvicorn app.main:app --reload
```

## Testing

To run test just type:

```bash
pytest --cov
```

## Running in Docker

## Docker

```bash
docker build . -t "${IMAGE_NAME}"
docker run --rm --env DATABASE_DSN=${DATABASE_DSN} -p 8000:80 "${IMAGE_NAME}"
```

## Adding new requirements

This project relies on [pip-tools](https://github.com/jazzband/pip-tools) to manage requirements.
To add a new one update one of the *.in files in [requirements](requirements) directory,
and then run:

```bash
pip-compile requirements/{updated_file}.in
```

To sync with your env:

```bash
pip-sync requirements/base.txt requirements/test.txt requirements/prod.txt
```

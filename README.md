# Hangman

This is simple REST API to play Hangman game

[![build](https://github.com/unmade/hangman/workflows/Lint%20and%20Test/badge.svg)](https://github.com/unmade/hangman/blob/master/.github/workflows/lint-and-test.yml)
[![build](https://github.com/unmade/hangman/workflows/Deploy/badge.svg)](https://github.com/unmade/hangman/blob/master/.github/workflows/deploy.yml)
[![codecov](https://codecov.io/gh/unmade/hangman/branch/master/graph/badge.svg)](https://codecov.io/gh/unmade/hangman)

## Configuration

App can be configured with environment variables

### App

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
|APP_NAME           | - | Hangman | Specifies app name |
|APP_VERSION        | - | -       | Specifies app version. This env is set during build |
|APP_DEBUG          | - | False   | Whether to run app in debug mode |

### Databases

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
|DATABASES_DSN | + | - | Database DSN. Examples: `sqlite:///./test.db`, `postgresql://user:password@host:port/name` |

### Game

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
|HANGMAN_WORDS | - | "3dhubs,marvin,print,filament,order,layer" | String of comma-separated words to use in the game |
|HANGMAN_MAX_ATTEMPTS | - | 5 | Specifies how much times user can ask letters that don't exist |

### Sentry

|Name     | Required | Default | Description|
|:--------|:-------- |:------- |:-----------|
|SENTRY_DSN | - | - | Sentry DSN |


## Documentation

Check out interactive documentation [here](https://apihangman.herokuapp.com/docs)

## Development

### Running locally

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

### Testing

To run test just type:

```bash
DATABASE_DSN=sqlite:// pytest --cov
```

### Running in Docker

```bash
docker build . -t "${IMAGE_NAME}"
docker run --rm --env DATABASE_DSN=${DATABASE_DSN} -p 8000:80 "${IMAGE_NAME}"
```

### Adding new requirements

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

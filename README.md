# Hangman

# Local Development

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

Run the app:

```bash
uvicorn app.main:app --reload
```

# HubSpot OAuth Integration

## How to run

To run first must set 2 environment variables `CLIENT_ID` and `CLIENT_SECRET`
then:

```bash
python db upgrade  # only the first time
python runner.py
```

## Install

```bash
pip install -r requirements.txt
```

### Dev install

```bash
pip install -r dev-requirements.txt
```

## TODO

- More test cases
- Add pre-commit and hooks to flake8, black and mypy
- Docstrings
- A root swagger
- Dockerfile to install everything automatically (python requirements) and including a MySQL server and the migrations.

# DefinIT database

## Run tests
```
cd src
python -m pytest
```

## Generate Markdown database
```
cd src
python -m definit_db.generate_db_md
```

## Build and upload the package
Upgrade version in `pyproject.toml` and `src/definit_db/__init__.py` before running the commands below.

```
(just once) python -m pip install requirements-dev.txt

(optional cleanup) rm -rf dist/ build/ src/*.egg-info/

python -m build

python -m twine upload dist/*
```

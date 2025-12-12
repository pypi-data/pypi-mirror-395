# types-pymob-guts-base

Stub‑only distribution that provides type hints for the **pymob** package extensions used in **guts-base** and derived projects.

This package follows **PEP 561** and contains `.pyi` files that mirror the public API of `pymob`.  
Install it alongside the real `pymob` library to enable static type checking with tools such as **mypy**, **pyright**, or **pyre**.

```bash
pip install pymob          # original library
pip install guts-base
pip install types-pymob    # type‑stub package
```

## Build and upload to pypi

cd /export/home/fschunck/projects/types-pymob-guts-base/

```bash
# 1. Install build tools
python3 -m pip install --quiet build twine python-dotenv

# 2. Build the package
python3 -m build

# 3. Load the token from .env
export $(grep -v '^#' .env | xargs)   # sets TWINE_PASSWORD in the shell

# 4. Upload
twine upload --config-file .pypirc dist/*
```

python3 -m twine upload dist/*

## License
MIT © 2025

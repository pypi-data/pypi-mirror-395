# singlejson
![GitHub issues](https://img.shields.io/github/issues/IgnyteX-Labs/singlejson) ![PyPI](https://img.shields.io/pypi/v/singlejson)

A very simple set of utilities for working with JSON in Python.

View the [documentation](https://ignytex-labs.github.io/singlejson/) here.

## Features:
* Easy loading of JSON files
* Only one instance for each opened file
* _This library doesn't feature much more, just the basics_

## Installation:
Install singlejson using pip
```shell
pip install singlejson
```

## Usage:
Loading JSON from file:
```python
import singlejson

file = singlejson.load('file.json')  # Load file.json
# Returns a JSONfile object which has the json property
file.json["fun"] = True  # Edit some values in the JSONfile
```
But if we try to load the same file from the filesystem again, we get the same object:
```python
file2 = singlejson.load('file.json')
print(file2.json["fun"])  # will output True
```
To save the file back to the disk we call ``file.save()``<br>
Maybe you don't want your program to save file contents only upon successful execution, then you just have to call ``singlejson.sync()`` at the end of your program to save **all** changes to the filesystem.

If the requested file doesn't exist, the file and its parent directories will be created and the "default" values will be written to the file.
Should the root "node" of your JSON be a List, you may specify that the default to save is an empty list using ``singlejson.load(file, default="[]")``

## Building the documentation locally

The docs are configured to install via an optional dependency group in `pyproject.toml` (PEP 621). You don’t need a separate `requirements.txt`.

Quick steps:

```bash
# From the project root
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[docs]

# Build HTML docs into docs/_build/html
python -m sphinx -b html docs/source docs/_build/html
```

Notes:
- The Sphinx theme is `furo`. Versions are declared under `[project.optional-dependencies].docs` in `pyproject.toml`.
- For a clean test, use a fresh virtual environment as shown above (preferred over uninstalling global packages).

### Contributing:
This is just a fun project of mine mainly to try out python packaging. If you would like to contribute or have a feature-request, please [open an issue or pull request](https://github.com/Qrashi/singlejson/issues/new).

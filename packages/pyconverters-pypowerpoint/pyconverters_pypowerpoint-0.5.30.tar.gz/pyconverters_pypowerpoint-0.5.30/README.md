# pyconverters_pypowerpoint

[![license](https://img.shields.io/github/license/oterrier/pyconverters_pypowerpoint)](https://github.com/oterrier/pyconverters_pypowerpoint/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_pypowerpoint/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_pypowerpoint/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_pypowerpoint)](https://codecov.io/gh/oterrier/pyconverters_pypowerpoint)
[![docs](https://img.shields.io/readthedocs/pyconverters_pypowerpoint)](https://pyconverters_pypowerpoint.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_pypowerpoint)](https://pypi.org/project/pyconverters_pypowerpoint/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_pypowerpoint)](https://pypi.org/project/pyconverters_pypowerpoint/)

Convert OCRized PDF to text using [PyPowerPoint](https://github.com/pypowerpoint/PyPowerPoint)

## Installation

You can simply `pip install pyconverters_pypowerpoint`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_pypowerpoint
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.

# Sensitivity Estimation for Gravitational-Wave Observatories

Easily build the noise and sensitivity curves for your favorite
gravitational-wave detector!

This package provides tools to build time and frequency-dependent noise
covariance matrices under the assumption of local stationnarity; to compute the
response of a gravitational-wave detector with an arbitrary number of links, and
sky average the response; to transform the noise and the signal to an arbitrary
set of observables; and finally, to compute the optimal sensitivity for a given
set of observables.

## Install

The package is available on PyPI. You can install it with

```bash
pip install segwo
```

The documentation for the latest stable release can be found
[here](https://j2b.bayle.gitlab.io/segwo).

## Contributing

### Report an issue

We use the issue-tracking management system associated with the project provided
by Gitlab. If you want to report a bug or request a feature, open an issue at
<https://gitlab.com/j2b.bayle/segwo/-/issues>. You may also thumb-up
or comment on existing issues.

### Development environment

This project uses Poetry 2 for dependency management. To install the
dependencies and the project itself, run the following command:

```bash
poetry install
```

We recommend you install pre-commit hooks to detect errors before you even
commit.

```bash
pre-commit install
```

You can now run commands inside a dedicated virtual environment by running

```bash
poetry run <your-command>
```

Refer to the [Poetry documentation](https://python-poetry.org/docs/) for more
information.

### Syntax

We enforce PEP 8 (Style Guide for Python Code) with Pylint syntax checking, and
code formatting with Black. Both are implemented in the continuous integration
system, and merge requests cannot be merged if it fails. Pre-commit hooks will
also run Black before you commit.

You can run them locally with

```bash
poetry run pylint segwo
poetry run black .
```

### Unit tests

Correction of the code is checked by the pytest testing framework. It is
implemented in the continuous integration system, but we recommend you run the
tests locally before you commit, with

```bash
poetry run pytest
```

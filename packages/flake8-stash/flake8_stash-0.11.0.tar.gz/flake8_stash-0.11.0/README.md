# flake8-stash

A collection of [flake8](https://github.com/pycqa/flake8) checks.

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ghazi-git/flake8-stash/tests.yml?branch=main&label=Tests&logo=GitHub)](https://github.com/ghazi-git/flake8-stash/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/flake8-stash)](https://pypi.org/project/flake8-stash/)
[![PyPI](https://img.shields.io/pypi/pyversions/flake8-stash?logo=python&logoColor=white)](https://pypi.org/project/flake8-stash/)
[![PyPI - License](https://img.shields.io/pypi/l/flake8-stash)](https://github.com/ghazi-git/flake8-stash/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## List of checks

- **STA011**: The use of `fields = '__all__'` in model forms is not allowed. List the fields one by one instead.
- **STA012**: The use of `exclude` in model forms is not allowed. Use `fields` instead.
- **STA021**: The use of `fields = '__all__'` in model serializers is not allowed. List the fields one by one instead.
- **STA022**: The use of `exclude` in model serializers is not allowed. Use `fields` instead.
- **STA031**: The use of `fields = '__all__'` in filtersets is not allowed. List the fields one by one instead.
- **STA032**: The use of `exclude` in filtersets is not allowed. Use `fields` instead.
- **STA041**: The use of `fields = '__all__'` is not allowed. List the fields one by one instead.
- **STA042**: The use of `exclude` is not allowed. Use `fields` instead.

## Installation

Install with `pip`

```shell
pip install flake8-stash
```

## Usage with pre-commit

```yaml
repos:
      - repo: https://github.com/pycqa/flake8
    rev: '6.0.0'
    hooks:
      - id: flake8
        additional_dependencies: [ "flake8-stash==0.11.0" ]
```

## License

This project is [MIT licensed](LICENSE).

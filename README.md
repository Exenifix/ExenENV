# ExenENV
Environment variables verifier and type converter.

## Installation
Library is available for installation from PyPI
```shell
$ pip install exenenv
```

## Basic Usage
```python
import os
from exenenv import EnvironmentProfile

os.environ["REQUIRED_VARIABLE"] = "20"  # assume it's set to this


class Environment(EnvironmentProfile):
    REQUIRED_VARIABLE: int
    DEFAULT_VALUE_VARIABLE: float = 30.0


env = Environment()
env.load()

print(f"{env.REQUIRED_VARIABLE=}\n{env.DEFAULT_VALUE_VARIABLE=}")
```
```
env.REQUIRED_VARIABLE=20
env.DEFAULT_VALUE_VARIABLE=30.0
```

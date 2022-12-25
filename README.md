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

## Using EnvVars

```python
import os
from exenenv import EnvironmentProfile, EnvVar

os.environ.update({
    "REQUIRED_VAR": "10",
    "ALT_NAME_VAR": "40",
    "CONVERTER_VAR": "gamer,coder,python"
})  # assume our environment is this


class Environment(EnvironmentProfile):
    REQUIRED_VAR: int
    DEFAULT_VALUE_VAR: str = EnvVar(default=20)
    OTHER_VAR: int = EnvVar(env_name="ALT_NAME_VAR")
    CONVERTER_VAR: list[str] = EnvVar(converter=lambda x: x.split(","))


env = Environment()
env.load()

print(f"""\
{env.REQUIRED_VAR=}
{env.DEFAULT_VALUE_VAR=}
{env.OTHER_VAR=}
{env.CONVERTER_VAR=}
""")
```
```
env.REQUIRED_VAR=10
env.DEFAULT_VALUE_VAR=20
env.OTHER_VAR=40
env.CONVERTER_VAR=['gamer', 'coder', 'python']
```

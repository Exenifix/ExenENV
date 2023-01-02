import os

import pytest

from exenenv import ConversionError, EnvironmentProfile, EnvVar, UnloadedVariables


def test_load():
    class Environment(EnvironmentProfile):
        DEFAULT_UNSET: int = 1
        DEFAULT_SET: int = 2
        SET: float

    os.environ.update({"DEFAULT_SET": "5", "SET": "4.2"})
    env = Environment()
    env.load()
    assert env.DEFAULT_UNSET == 1
    assert env.DEFAULT_SET == 5
    assert env.SET == 4.2


def test_unloaded():
    class Environment(EnvironmentProfile):
        MISSING: str
        NOT_MISSING: int

    os.environ.update({"NOT_MISSING": "10"})
    env = Environment()
    unloaded = env.load(raise_exc=False)
    assert unloaded == {"MISSING"}
    assert env.NOT_MISSING == 10

    with pytest.raises(UnloadedVariables):
        env.load()


def test_bad_type():
    class Environment(EnvironmentProfile):
        BAD_TYPE: int

    os.environ.update({"BAD_TYPE": "very bad"})
    env = Environment()
    with pytest.raises(ConversionError):
        env.load()


def test_bool():
    class Environment(EnvironmentProfile):
        BOOL: bool

    os.environ.update({"BOOL": "true"})
    env = Environment()
    env.load()
    assert env.BOOL is True


def test_envvar():
    class Environment(EnvironmentProfile):
        DEFAULT_VAR: int = EnvVar(default=10)
        alt_name_var: int = EnvVar(env_name="VAR")
        CONVERTER_VAR: list[str] = EnvVar(converter=lambda x: x.split(","))

    os.environ.update({"VAR": "40", "CONVERTER_VAR": "one,two"})
    env = Environment()
    env.load()
    assert env.DEFAULT_VAR == 10
    assert env.alt_name_var == 40
    assert env.CONVERTER_VAR == ["one", "two"]


def test_union():
    class Environment(EnvironmentProfile):
        UNION_VAR: int | str
        OPTIONAL_VAR: float | None = None

    os.environ.update({"UNION_VAR": "union"})
    env = Environment()
    env.load()
    assert env.UNION_VAR == "union"
    assert env.OPTIONAL_VAR is None

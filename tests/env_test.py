import os

import pytest

from exenenv import ConversionError, EnvironmentProfile, UnloadedVariables


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

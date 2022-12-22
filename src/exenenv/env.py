import os
from dataclasses import dataclass
from typing import Any, Callable

from .errors import ConversionError, UnloadedVariables

MISSING = object()


@dataclass
class _EnvVar:
    name: str
    default_value: Any
    type: Callable


class EnvironmentProfile:
    _env_vars: list[_EnvVar]

    def __init_subclass__(cls, **kwargs) -> None:
        cls._env_vars = [
            _EnvVar(field, getattr(cls, field, MISSING), _type) for field, _type in cls.__annotations__.items()
        ]
        for var in cls._env_vars:
            if var.default_value is not MISSING:
                setattr(cls, var.name, var.default_value)

    def load(self, raise_exc: bool = True) -> set[str]:
        """Load environment variables from `os.environ` into class and ensure presence of required ones.

        :param raise_exc: Whether to raise `UnloadedVariables` if required variables are not set.

        :returns: Set of missing environment variables names.

        :raises ConversionError: failed to apply type to value
        :raises UnloadedVariables: variables with unset default values are not set
        """
        unloaded = set()
        for var in self._env_vars:
            value = os.getenv(var.name, None)
            if value is None and var.default_value is MISSING:
                unloaded.add(var.name)
            elif value is not None:
                try:
                    setattr(self, var.name, var.type(value))
                except Exception:
                    raise ConversionError(value, var.type)

        if raise_exc and len(unloaded) > 0:
            raise UnloadedVariables(unloaded)

        return unloaded

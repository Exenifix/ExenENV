import os
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from .convertors import conv_bool
from .errors import ConversionError, UnloadedVariables

T = TypeVar("T")
MISSING = object()


@dataclass
class _EnvVar:
    name: str
    default_value: Any
    type: Callable


class EnvVar:
    def __init__(
        self, *, default: Any = MISSING, converter: Callable[[str], T] | None = None, env_name: str | None = None
    ):
        """Environment variable class to configure variable conversion and loading.

        :param default: The default value to assign if the variable is unset.
        :param converter: Converter function that converts the string to required type.
            Attribute typehint is used if unspecified.
        :param env_name: Name of environment variable to search for. Attribute's name by default."""
        self.default = default
        self.converter = converter
        self.env_name = env_name

    def convert(self, arg: str) -> T:
        return self.converter(arg)

    @property
    def required(self) -> bool:
        return self.default is MISSING


class EnvironmentProfile:
    _env_vars: list[_EnvVar]

    def __init_subclass__(cls, **kwargs) -> None:
        cls._env_vars: dict[str, EnvVar] = {}
        for name, _type in cls.__annotations__.items():
            if _type is bool:
                _type = conv_bool
            default = getattr(cls, name, MISSING)
            if isinstance(default, EnvVar):
                default.converter = default.converter or _type
                default.env_name = default.env_name or name
                cls._env_vars[name] = default
            else:
                cls._env_vars[name] = EnvVar(default=default, converter=_type, env_name=name)

        for name, var in cls._env_vars.items():
            if not var.required:
                setattr(cls, name, var.default)

    def load(self, raise_exc: bool = True) -> set[str]:
        """Load environment variables from `os.environ` into class and ensure presence of required ones.

        :param raise_exc: Whether to raise `UnloadedVariables` if required variables are not set.

        :returns: Set of missing environment variables names.

        :raises ConversionError: failed to apply type to value
        :raises UnloadedVariables: variables with unset default values are not set
        """
        unloaded = set()
        for name, var in self._env_vars.items():
            value = os.getenv(var.env_name, None)
            if value is None and var.required:
                unloaded.add(var.env_name)
            elif value is not None:
                try:
                    setattr(self, name, var.convert(value))
                except Exception:
                    raise ConversionError(value, var.converter)

        if raise_exc and len(unloaded) > 0:
            raise UnloadedVariables(unloaded)

        return unloaded

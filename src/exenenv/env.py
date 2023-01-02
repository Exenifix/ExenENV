import os
import typing
from types import UnionType
from typing import Any, Callable, TypeVar

from .convertors import conv_bool
from .errors import BadConverter, ConversionError, UnionConversionError, UnloadedVariables

T = TypeVar("T")
MISSING = object()


class EnvVar:
    def __init__(
        self, *, default: Any = MISSING, converter: Callable[[str], T] | UnionType = None, env_name: str | None = None
    ):
        """
        Environment variable class to configure variable conversion and loading.

        :param default: The default value to assign if the variable is unset.
        :param converter: Union of callables or a single callable that converts the string to required type.
            Attribute typehint is used if unspecified.
        :param env_name: Name of environment variable to search for. Attribute's name by default.
        :raise TypeError: Bad ``converter`` type.
        """
        if converter is not None and not callable(converter) and not isinstance(converter, UnionType):
            raise BadConverter(converter)

        self.default = default
        self.converter = converter
        self.env_name = env_name

    def convert(self, arg: str) -> T:
        if callable(self.converter):
            return self.converter(arg)
        if isinstance(self.converter, UnionType):
            exceptions: list[Exception] = []
            for t in self.converter.__args__:
                try:
                    conv = t if t is not bool else conv_bool
                    return conv(arg)
                except Exception as e:
                    exceptions.append(e)
            raise UnionConversionError(arg, self.converter, exceptions)
        raise BadConverter(self.converter)

    @property
    def required(self) -> bool:
        return self.default is MISSING


class EnvironmentProfile:
    _env_vars: list[EnvVar]

    def __init_subclass__(cls, **kwargs) -> None:
        cls._env_vars: dict[str, EnvVar] = {}
        for name, _type in typing.get_type_hints(cls).items():
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
                except (UnionConversionError, BadConverter) as e:
                    raise e
                except Exception:
                    raise ConversionError(value, typing.cast(var.converter, Callable[[str], Any]))

        if raise_exc and len(unloaded) > 0:
            raise UnloadedVariables(unloaded)

        return unloaded

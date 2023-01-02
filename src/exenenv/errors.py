from types import UnionType
from typing import Any, Callable, Iterable


class ConversionError(Exception):
    def __init__(self, value: str, _type: Callable):
        super().__init__("Failed to convert `%s` with function `%s`" % (value, _type.__name__))


class UnionConversionError(Exception):
    def __init__(self, value: str, t: UnionType, exceptions: list[Exception]):
        super().__init__("Failed to convert `%s` to any of types of `%s`" % (value, t))
        self.exceptions = exceptions


class UnloadedVariables(Exception):
    def __init__(self, variables: Iterable[str]):
        super().__init__("Unset ENV variables: %s" % ", ".join(variables))
        self.variables = variables


class BadConverter(Exception):
    def __init__(self, converter: Any):
        super().__init__("Invalid converter %s, must be a callable or Union" % converter)

from typing import Any, Callable, Iterable


class ConversionError(Exception):
    def __init__(self, value: Any, _type: Callable):
        super().__init__("Cannot convert `%s` to type `%s`" % (value, _type))


class UnloadedVariables(Exception):
    def __init__(self, variables: Iterable[str]):
        super().__init__("Unset ENV variables: %s" % ", ".join(variables))
        self.variables = variables

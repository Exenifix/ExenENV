from typing import Any, Callable, Iterable


class ConversionError(Exception):
    def __init__(self, value: Any, _type: Callable):
        super().__init__("Failed to convert `%s` with function `%s`" % (value, _type.__name__))


class UnloadedVariables(Exception):
    def __init__(self, variables: Iterable[str]):
        super().__init__("Unset ENV variables: %s" % ", ".join(variables))
        self.variables = variables

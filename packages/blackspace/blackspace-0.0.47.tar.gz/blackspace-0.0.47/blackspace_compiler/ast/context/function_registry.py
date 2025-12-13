from contextlib import contextmanager

from ..definitions.function import FunctionSignature


class FunctionRegistry:
    def __init__(self) -> None:
        self._functions: list[FunctionSignature] = []
        self._labels: dict[str, int] = {}
        self._current_function: FunctionSignature | None = None

    def register_function(self, function: FunctionSignature, label_id: int) -> None:
        if any(fn.name == function.name for fn in self._functions):
            raise RuntimeError(f"Function '{function.name}' is already registered.")

        self._functions.append(function)
        self._labels[function.name] = label_id

    def get_function_definition(self, function_name: str) -> FunctionSignature | None:
        for function in self._functions:
            if function.name == function_name:
                return function
        return None

    def get_function_label(self, function_name: str) -> int:
        """
        Get the label ID for the given function name.
        Should not be called unless the function is known to exist by using
        `get_function_definition` first.
        """
        return self._labels[function_name]

    @contextmanager
    def function_context(self, function: FunctionSignature):
        if self._current_function is not None:
            raise RuntimeError("Nested function definitions are not supported.")
        self._current_function = function
        try:
            yield
        finally:
            self._current_function = None

    @property
    def current_function(self) -> FunctionSignature | None:
        return self._current_function

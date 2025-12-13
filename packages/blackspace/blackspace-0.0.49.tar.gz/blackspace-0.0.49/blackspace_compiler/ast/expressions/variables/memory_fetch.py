from ....whitespace.snippets import FETCH
from ...context import EvaluationContext, IssueLevel
from ...types.complex.memory import MemoryType
from ...types.primitives.void import VoidType
from ...types.type import Type
from ..expression import Expression


class MemoryFetch(Expression):
    def __init__(self, inner_expr) -> None:
        super().__init__()
        self._inner_expr = inner_expr

    def __repr__(self) -> str:
        return f"resolve({self._inner_expr})"

    def get_type(self, context: EvaluationContext) -> Type:
        inner_type = self._inner_expr.get_type(context)
        if isinstance(inner_type, MemoryType):
            return inner_type.of
        return VoidType()

    def evaluate(self, context: EvaluationContext) -> str:
        arr_type = self._inner_expr.get_type(context)
        if not isinstance(arr_type, MemoryType):
            context.register_issue(
                IssueLevel.ERROR,
                self._inner_expr,
                f"Type '{arr_type}' is not dereferenceable.",
            )
            return ""

        res = ""
        res += self._inner_expr.evaluate(context)
        res += FETCH

        return res

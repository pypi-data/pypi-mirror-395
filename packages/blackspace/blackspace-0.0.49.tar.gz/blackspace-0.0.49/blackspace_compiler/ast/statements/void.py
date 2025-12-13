from ...whitespace.snippets import POP
from ..context import EvaluationContext
from ..expressions.expression import Expression
from .statement import Statement


class VoidStatement(Statement):
    """A void statement evaluates an expression and discards its result."""

    def __init__(self, expression: Expression) -> None:
        super().__init__()
        self.expression = expression

    def evaluate(self, context: EvaluationContext):
        return self.expression.evaluate(context) + POP

from ...context import EvaluationContext
from ...types.primitives.int import IntegerType
from ..expression import Expression
from ..literals.int import IntLiteral


class SizeofExpression(Expression):
    def __init__(self, inner_expression: Expression):
        super().__init__()
        self.inner_expression = inner_expression

    def __repr__(self):
        return f"sizeof({self.inner_expression})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext) -> str:
        inner_type = self.inner_expression.get_type(context)
        size = inner_type.get_size()
        return IntLiteral(size).evaluate(context)

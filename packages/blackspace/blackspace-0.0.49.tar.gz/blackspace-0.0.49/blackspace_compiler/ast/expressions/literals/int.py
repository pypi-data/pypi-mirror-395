from ....whitespace.snippets import PUSH
from ...context import EvaluationContext
from ...types.primitives.int import IntegerType
from ..expression import Expression


class IntLiteral(Expression):

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __repr__(self):
        return str(self.value)

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext) -> str:
        return PUSH(self.value)

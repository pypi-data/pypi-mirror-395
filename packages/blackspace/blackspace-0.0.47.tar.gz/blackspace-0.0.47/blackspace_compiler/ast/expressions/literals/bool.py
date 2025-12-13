from ....whitespace.snippets import PUSH
from ...context import EvaluationContext
from ...types.primitives.bool import BooleanType
from ..expression import Expression


class TrueLiteral(Expression):

    def __repr__(self):
        return "TRUE"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext) -> str:
        return PUSH(1)


class FalseLiteral(Expression):

    def __repr__(self):
        return "FALSE"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext) -> str:
        return PUSH(0)

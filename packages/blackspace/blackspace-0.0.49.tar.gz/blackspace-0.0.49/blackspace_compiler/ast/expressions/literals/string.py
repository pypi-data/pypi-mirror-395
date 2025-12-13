import json

from ...context import EvaluationContext
from ...context.heap.helpers import place_const_data_on_heap
from ...types.complex.string import StringType
from ..expression import Expression


class StringLiteral(Expression):
    def __init__(self, value: str) -> None:
        super().__init__()
        self._value = value

    def __repr__(self):
        return json.dumps(self._value)

    def get_type(self, context: EvaluationContext):
        return StringType()

    def evaluate(self, context: EvaluationContext) -> str:
        return place_const_data_on_heap(context, list(ord(c) for c in self._value))

from ....whitespace.snippets import ADD, DIVIDE, MODULO, MULTIPLY, SUBTRACT
from ...context import EvaluationContext
from ...types.primitives.int import IntegerType
from .operator import BinaryOperator


class AddOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} + {self.right_side})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())
        return self._evaluate_both_sides(context) + ADD


class SubtractOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} - {self.right_side})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())
        return self._evaluate_both_sides(context) + SUBTRACT


class MultiplyOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} * {self.right_side})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())
        return self._evaluate_both_sides(context) + MULTIPLY


class DivideOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} / {self.right_side})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())
        return self._evaluate_both_sides(context) + DIVIDE


class ModuloOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} % {self.right_side})"

    def get_type(self, context):
        return IntegerType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())
        return self._evaluate_both_sides(context) + MODULO

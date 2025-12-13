from ....whitespace.snippets import JUMP, JUMP_IF_NEG, JUMP_IF_ZERO, LABEL, SUBTRACT, SWAP
from ...context import EvaluationContext
from ...types.primitives.bool import BooleanType
from ...types.primitives.int import IntegerType
from ..literals.bool import FalseLiteral, TrueLiteral
from .operator import BinaryOperator


class EqualOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} == {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_same_type(context)

        label_equals = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SUBTRACT
            + JUMP_IF_ZERO(label_equals)
            + FalseLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_equals)
            + TrueLiteral().evaluate(context)
            + LABEL(label_end)
        )


class NotEqualOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} != {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_same_type(context)

        label_equals = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SUBTRACT
            + JUMP_IF_ZERO(label_equals)
            + TrueLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_equals)
            + FalseLiteral().evaluate(context)
            + LABEL(label_end)
        )


class GreaterThanOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} > {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())

        label_greater = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SWAP
            + SUBTRACT
            + JUMP_IF_NEG(label_greater)
            + FalseLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_greater)
            + TrueLiteral().evaluate(context)
            + LABEL(label_end)
        )


class GreaterOrEqualThanOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} >= {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())

        label_less = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SUBTRACT
            + JUMP_IF_NEG(label_less)
            + TrueLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_less)
            + FalseLiteral().evaluate(context)
            + LABEL(label_end)
        )


class LessThanOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} < {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())

        label_less = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SUBTRACT
            + JUMP_IF_NEG(label_less)
            + FalseLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_less)
            + TrueLiteral().evaluate(context)
            + LABEL(label_end)
        )


class LessOrEqualThanOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} <= {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, IntegerType())

        label_greater = context.label_registry.new_label()
        label_end = context.label_registry.new_label()

        return (
            self._evaluate_both_sides(context)
            + SWAP
            + SUBTRACT
            + JUMP_IF_NEG(label_greater)
            + TrueLiteral().evaluate(context)
            + JUMP(label_end)
            + LABEL(label_greater)
            + FalseLiteral().evaluate(context)
            + LABEL(label_end)
        )

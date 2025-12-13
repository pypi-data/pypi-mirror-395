from ....whitespace.snippets import JUMP, JUMP_IF_ZERO, LABEL
from ...context import EvaluationContext
from ...types.primitives.bool import BooleanType
from ..literals.bool import FalseLiteral, TrueLiteral
from .operator import BinaryOperator, UnaryOperator


class NotOperator(UnaryOperator):
    def __repr__(self):
        return f"!{self.inner_expression}"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_inner_as_type(context, BooleanType())

        false_label = context.label_registry.new_label()
        end_label = context.label_registry.new_label()

        return (
            self.inner_expression.evaluate(context)
            + JUMP_IF_ZERO(false_label)
            + FalseLiteral().evaluate(context)
            + JUMP(end_label)
            + LABEL(false_label)
            + TrueLiteral().evaluate(context)
            + LABEL(end_label)
        )


class AndOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} && {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, BooleanType())

        false_label = context.label_registry.new_label()
        end_label = context.label_registry.new_label()

        return (
            self.left_side.evaluate(context)
            + JUMP_IF_ZERO(false_label)
            + self.right_side.evaluate(context)
            + JUMP_IF_ZERO(false_label)
            + TrueLiteral().evaluate(context)
            + JUMP(end_label)
            + LABEL(false_label)
            + FalseLiteral().evaluate(context)
            + LABEL(end_label)
        )


class OrOperator(BinaryOperator):
    def __repr__(self):
        return f"({self.left_side} || {self.right_side})"

    def get_type(self, context):
        return BooleanType()

    def evaluate(self, context: EvaluationContext):
        self._enforce_both_sides_as_type(context, BooleanType())

        check_right_side_label = context.label_registry.new_label()
        false_label = context.label_registry.new_label()
        end_label = context.label_registry.new_label()

        return (
            self.left_side.evaluate(context)
            + JUMP_IF_ZERO(check_right_side_label)
            + TrueLiteral().evaluate(context)
            + JUMP(end_label)
            + LABEL(check_right_side_label)
            + self.right_side.evaluate(context)
            + JUMP_IF_ZERO(false_label)
            + TrueLiteral().evaluate(context)
            + JUMP(end_label)
            + LABEL(false_label)
            + FalseLiteral().evaluate(context)
            + LABEL(end_label)
        )

from abc import ABC

from ...context import EvaluationContext, IssueLevel
from ...types.type import Type
from ...utils.error_message import type_error
from ..expression import Expression


class Operator(Expression, ABC):
    pass


class UnaryOperator(Operator, ABC):
    def __init__(self, inner_expr: Expression):
        super().__init__()
        self.inner_expression = inner_expr

    def _enforce_inner_as_type(self, context: EvaluationContext, type: Type) -> None:
        inner_type = self.inner_expression.get_type(context)
        if inner_type != type:
            context.register_issue(
                IssueLevel.ERROR,
                self.inner_expression,
                type_error(type, inner_type, self),
            )


class BinaryOperator(Operator, ABC):
    def __init__(self, left_side: Expression, right_side: Expression):
        super().__init__()
        self.left_side = left_side
        self.right_side = right_side

    def _evaluate_both_sides(self, context: EvaluationContext) -> str:
        return self.left_side.evaluate(context) + context.with_incremented_stack(
            lambda c: self.right_side.evaluate(c)
        )

    def _enforce_both_sides_as_type(self, context: EvaluationContext, type: Type) -> None:
        left_side_type = self.left_side.get_type(context)
        if self.left_side.get_type(context) != type:
            context.register_issue(
                IssueLevel.ERROR,
                self.left_side,
                type_error(type, left_side_type, self.left_side),
            )

        right_side_type = self.right_side.get_type(context)
        if self.right_side.get_type(context) != type:
            context.register_issue(
                IssueLevel.ERROR,
                self.right_side,
                type_error(type, right_side_type, self.right_side),
            )

    def _enforce_both_sides_as_same_type(self, context: EvaluationContext) -> None:
        left_side_type = self.left_side.get_type(context)
        right_side_type = self.right_side.get_type(context)
        if left_side_type != right_side_type:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                "Type mismatch between left and right side of operation: "
                f"{left_side_type} vs {right_side_type}",
            )

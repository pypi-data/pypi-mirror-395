from __future__ import annotations

from ...whitespace.snippets import JUMP, JUMP_IF_ZERO, LABEL
from ..context import EvaluationContext, IssueLevel
from ..expressions.expression import Expression
from ..types.primitives.bool import BooleanType
from ..utils.error_message import type_error
from ..utils.indent import indent
from .statement import Statement


class ConditionStatement(Statement):
    def __init__(
        self, condition: Expression, if_true: Statement, if_false: Statement | None = None
    ):
        super().__init__()
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def __repr__(self) -> str:
        res = f"if {self.condition} then\n"
        res += indent(repr(self.if_true))
        if self.if_false:
            res += f"\nelse\n{indent(repr(self.if_false))}"
        return res

    def evaluate(self, context: EvaluationContext):
        condition_type = self.condition.get_type(context)
        if condition_type != BooleanType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(BooleanType(), condition_type, self),
            )

        res = self.condition.evaluate(context)
        if self.if_false:
            if_false_label = context.label_registry.new_label()
            end_label = context.label_registry.new_label()

            res += (
                JUMP_IF_ZERO(if_false_label)
                + self.if_true.evaluate(context)
                + JUMP(end_label)
                + LABEL(if_false_label)
                + self.if_false.evaluate(context)
                + LABEL(end_label)
            )
        else:
            end_label = context.label_registry.new_label()

            res += JUMP_IF_ZERO(end_label) + self.if_true.evaluate(context) + LABEL(end_label)

        return res

from abc import ABC

from ...whitespace.snippets import JUMP, JUMP_IF_ZERO, LABEL
from ..context import EvaluationContext, IssueLevel
from ..expressions.expression import Expression
from ..types.primitives.bool import BooleanType
from ..utils.error_message import type_error
from .statement import Statement


class LoopStatement(Statement, ABC):
    def __init__(self):
        pass


class WhileLoopStatement(LoopStatement):
    def __init__(self, condition: Expression, body: Statement):
        super().__init__()
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"while {self.condition}: {self.body}"

    def evaluate(self, context: EvaluationContext) -> str:
        condition_type = self.condition.get_type(context)
        if condition_type != BooleanType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(BooleanType(), condition_type, self),
            )

        loop_start_label = context.label_registry.new_label()
        loop_end_label = context.label_registry.new_label()

        return (
            LABEL(loop_start_label)
            + self.condition.evaluate(context)
            + JUMP_IF_ZERO(loop_end_label)
            + self.body.evaluate(context)
            + JUMP(loop_start_label)
            + LABEL(loop_end_label)
        )


class DoWhileStatement(LoopStatement):
    def __init__(self, condition: Expression, body: Statement):
        super().__init__()
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"do {self.body} while {self.condition}"

    def evaluate(self, context: EvaluationContext) -> str:
        condition_type = self.condition.get_type(context)
        if condition_type != BooleanType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(BooleanType(), condition_type, self),
            )

        loop_start_label = context.label_registry.new_label()
        loop_end_label = context.label_registry.new_label()

        return (
            LABEL(loop_start_label)
            + self.body.evaluate(context)
            + self.condition.evaluate(context)
            + JUMP_IF_ZERO(loop_end_label)
            + JUMP(loop_start_label)
            + LABEL(loop_end_label)
        )


class ForLoopStatement(LoopStatement):
    def __init__(
        self,
        initializer: Statement,
        condition: Expression,
        increment: Statement,
        body: Statement,
    ):
        super().__init__()
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

    def __repr__(self):
        return f"for ({self.initializer}; {self.condition}; {self.increment}) {self.body}"

    def evaluate(self, context: EvaluationContext) -> str:
        condition_type = self.condition.get_type(context)
        if condition_type != BooleanType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(BooleanType(), condition_type, self),
            )

        loop_start_label = context.label_registry.new_label()
        loop_end_label = context.label_registry.new_label()

        return (
            self.initializer.evaluate(context)
            + LABEL(loop_start_label)
            + self.condition.evaluate(context)
            + JUMP_IF_ZERO(loop_end_label)
            + self.body.evaluate(context)
            + self.increment.evaluate(context)
            + JUMP(loop_start_label)
            + LABEL(loop_end_label)
        )

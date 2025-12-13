from ...whitespace.snippets import STORE
from ..context import EvaluationContext, IssueLevel
from ..context.evaluation_context import increment_stack
from ..expressions.expression import Expression
from ..types.complex.memory import MemoryType
from ..utils.error_message import type_error
from .statement import Statement


class AssignmentStatement(Statement):
    def __init__(self, target: Expression, value: Expression) -> None:
        super().__init__()
        self._target = target
        self._value = value

    def __repr__(self):
        return f"{self._target} = {self._value}"

    def evaluate(self, context: EvaluationContext) -> str:
        target_type = self._target.get_type(context)
        if not isinstance(target_type, MemoryType):
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Invalid assignment target: cannot assign to expression of type '{target_type}'.",
            )
            return ""

        inner_target_type = target_type.of
        value_type = self._value.get_type(context)
        if inner_target_type != value_type:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(inner_target_type, value_type, self),
            )
            return ""

        res = self._target.evaluate(context)
        with increment_stack(context):
            res += self._value.evaluate(context)
        res += STORE

        return res

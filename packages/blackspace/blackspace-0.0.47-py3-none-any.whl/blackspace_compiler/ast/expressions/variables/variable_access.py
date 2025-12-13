from ...context import EvaluationContext, IssueLevel
from ...context.stack.helpers import get_datastack_location
from ...definitions.function import VariableOffset
from ...types.complex.memory import MemoryType
from ...types.primitives.void import VoidType
from ...types.type import Type
from ..expression import Expression


class VariableAccess(Expression):
    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def __repr__(self):
        return self._name

    def _get_variable_definition(self, context: EvaluationContext) -> VariableOffset | None:
        if not context.function_registry.current_function:
            return None
        return context.function_registry.current_function.get_variable(self._name)

    def get_type(self, context: EvaluationContext) -> Type:
        definition = self._get_variable_definition(context)
        if definition is None:
            return VoidType()
        return MemoryType(definition.definition.type)

    def evaluate(self, context: EvaluationContext) -> str:
        definition = self._get_variable_definition(context)
        if not definition:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Variable '{self._name}' is not defined.",
            )
            return ""

        res = get_datastack_location(context, definition.offset)
        return res

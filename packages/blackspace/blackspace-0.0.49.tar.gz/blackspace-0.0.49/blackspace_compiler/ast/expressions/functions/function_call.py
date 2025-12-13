from ....whitespace.snippets import CALL, FETCH, PUSH, STORE, SWAP
from ...context import EvaluationContext, IssueLevel
from ...context.evaluation_context import increment_stack, reset_stack
from ...context.heap.consts import FUNCTION_PARAMETER_REGISTERS, REGISTER_A
from ...context.stack.helpers import (
    enter_new_stack,
    exit_stack,
    get_datastack_location,
    silently_allocate_on_datastack,
)
from ...debugstatement import debug_statement
from ...types.primitives.void import VoidType
from ..expression import Expression


class FunctionCall(Expression):
    def __init__(self, name: str, parameters: list[Expression]) -> None:
        super().__init__()
        self._name = name
        self._parameters = parameters

    def __repr__(self):
        return f"{self._name}(" + ", ".join(repr(p) for p in self._parameters) + ")"

    def get_type(self, context):
        function_def = context.function_registry.get_function_definition(self._name)
        if function_def:
            return function_def.return_type
        else:
            return VoidType()

    def evaluate(self, context: EvaluationContext) -> str:
        function_def = context.function_registry.get_function_definition(self._name)
        if not function_def:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Function '{self._name}' is not defined.",
            )
            return ""

        if len(function_def.parameters) != len(self._parameters):
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Function '{self._name}' expects {len(function_def.parameters)} parameters, "
                f"but {len(self._parameters)} were given.",
            )
            return ""

        for i in range(min(len(self._parameters), len(function_def.parameters))):
            expected_type = function_def.parameters[i].type
            actual_type = self._parameters[i].get_type(context)
            if actual_type != expected_type:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    f"Parameter {i + 1} of function '{self._name}' expects type "
                    f"'{expected_type}', but got type '{actual_type}'.",
                )
                return ""

        if len(function_def.parameters) > len(FUNCTION_PARAMETER_REGISTERS):
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Function '{self._name}' has too many parameters "
                f"(max {len(FUNCTION_PARAMETER_REGISTERS)}), "
                f"currently only functions with up to {len(FUNCTION_PARAMETER_REGISTERS)} "
                "parameters are supported.",
            )
            return ""

        function_label = context.function_registry.get_function_label(self._name)

        res = ""
        res += debug_statement("Function Call: " + self._name)

        # Evaluate parameters and store them in registers
        for i in range(len(self._parameters)):
            if self._parameters[i].get_type(context).get_size() != 1:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    "Currently only parameters of size 1 are supported.",
                )
                return ""

            res += PUSH(FUNCTION_PARAMETER_REGISTERS[i])
            with increment_stack(context):
                res += self._parameters[i].evaluate(context)
            res += STORE

        # Set up new stack frame
        res += enter_new_stack(context)
        with reset_stack(context):
            # Allocate space for function variables
            total_var_size = sum(v.type.get_size() for v in function_def.variables)
            res += silently_allocate_on_datastack(context, total_var_size)

            # Copy parameters into variables in new stack frame
            function_def.assert_correct_variable_configuration()
            for i, param in enumerate(function_def.parameters):
                matching_var = function_def.get_variable(param.name)
                if not matching_var:
                    continue  # This should not happen due to earlier checks
                res += get_datastack_location(context, matching_var.offset)
                res += PUSH(FUNCTION_PARAMETER_REGISTERS[i]) + FETCH + STORE

            # Call the function
            res += CALL(function_label)

            res += debug_statement("Returned from function: " + self._name)

            # Safely store return value
            res += PUSH(REGISTER_A) + SWAP + STORE

        # Dispose of stack frame
        res += exit_stack(context)

        # Move return value back to stack
        res += PUSH(REGISTER_A) + FETCH

        return res

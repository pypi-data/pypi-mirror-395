from ...whitespace.printstr import print_str
from ...whitespace.snippets import END, LABEL, PUSH, RETURN
from ..context import EvaluationContext, IssueLevel
from ..definitions.function import FunctionSignature
from ..expressions.expression import Expression
from ..types.primitives.void import VoidType
from .statement import Statement


class FunctionBodyStatement(Statement):

    def __init__(self, signature: FunctionSignature, body: Statement) -> None:
        super().__init__()
        self._signature = signature
        self._body = body

    def __repr__(self):
        res = f"{self._signature.return_type} "
        res += f"{self._signature.name}("
        res += ", ".join(str(param.name) for param in self._signature.parameters)
        res += f") {self._body}"
        return res

    def evaluate(self, context: EvaluationContext) -> str:
        entry_label = context.label_registry.new_label()
        context.function_registry.register_function(self._signature, entry_label)

        # Stack frame and initial variables are set up by the caller.
        # We just need to generate the body here.

        res = LABEL(entry_label)

        with context.function_registry.function_context(self._signature):
            res += self._body.evaluate(context)

        if self._signature.return_type == VoidType():
            # According to the calling convention, void function should still return a value,
            # so we push a dummy 0 before returning.
            res += PUSH(0) + RETURN
        else:
            # Non-void functions should return a value before reaching the end.
            # If the function body reaches here, it's an error in the source code.
            # TODO: Optimize this error by only having it once in the program, and jumping to it.
            res += print_str("Error: Non-void function did not return a value.\n")
            res += END

        return res


class ReturnStatement(Statement):

    def __init__(self, value: Expression | None):
        super().__init__()
        self._value = value

    def __repr__(self):
        if self._value is None:
            return "return"
        return f"return {self._value}"

    def evaluate(self, context: EvaluationContext) -> str:
        if not context.function_registry.current_function:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                "Return statement outside of a function.",
            )
            return ""
        function_definition = context.function_registry.current_function

        if function_definition.return_type == VoidType():
            if self._value is not None:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    "Void function should not return a value.",
                )
                return ""

            return PUSH(0) + RETURN
        else:
            if self._value is None:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    "Non-void function must return a value.",
                )
                return ""
            value_type = self._value.get_type(context)
            if value_type != function_definition.return_type:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    f"Return type mismatch: expected {function_definition.return_type}, "
                    f"got {value_type}.",
                )
                return ""

            return self._value.evaluate(context) + RETURN

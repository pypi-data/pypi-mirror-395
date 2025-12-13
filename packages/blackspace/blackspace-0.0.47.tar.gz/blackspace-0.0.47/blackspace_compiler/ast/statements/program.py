from ...whitespace.snippets import END
from ..context import EvaluationContext, IssueLevel
from ..context.heap.helpers import initialize_heap
from ..context.stack.helpers import enter_first_stack
from ..debugstatement import debug_statement
from ..expressions.functions.function_call import FunctionCall
from ..types.primitives.void import VoidType
from .statement import Statement
from .void import VoidStatement


class Program(Statement):
    def __init__(self, statement: Statement, entry_function: str = "main"):
        super().__init__()
        self._statement = statement
        self._entry_function = entry_function

    def __repr__(self):
        return f"Program {self._statement}"

    def evaluate(self, context: EvaluationContext) -> str:
        # Evaluating the main statement block first is needed,
        # since that will register all functions
        statement_code = self._statement.evaluate(context)

        entry_function = context.function_registry.get_function_definition(self._entry_function)
        if not entry_function:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Entry function '{self._entry_function}' is not defined.",
            )
            return ""
        if len(entry_function.parameters) > 0:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Entry function '{self._entry_function}' must not have parameters.",
            )
            return ""
        if entry_function.return_type != VoidType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Entry function '{self._entry_function}' must have return type 'void'.",
            )
            return ""

        res = ""

        # initialize the heap
        res += initialize_heap(context)

        # set up the first stack
        res += enter_first_stack(context)

        # imitate function call to main function
        res += debug_statement(f"Calling entry function '{self._entry_function}'")
        res += VoidStatement(FunctionCall(name=self._entry_function, parameters=[])).evaluate(
            context
        )

        res += END

        res += debug_statement("Program statement:")
        res += statement_code

        return res

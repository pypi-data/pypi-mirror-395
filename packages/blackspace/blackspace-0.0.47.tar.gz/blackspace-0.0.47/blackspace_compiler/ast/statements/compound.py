from ..context import EvaluationContext
from ..utils.indent import indent
from .statement import Statement


class CompoundStatement(Statement):
    """A compound statement is a sequence of statements executed in order."""

    def __init__(self, statements: list[Statement]) -> None:
        super().__init__()
        self.statements = statements

    def __repr__(self):
        res = "{\n"
        for stmt in self.statements:
            res += indent(repr(stmt)) + "\n"
        res += "}"
        return res

    def evaluate(self, context: EvaluationContext):
        code = ""
        for statement in self.statements:
            code += statement.evaluate(context)
        return code

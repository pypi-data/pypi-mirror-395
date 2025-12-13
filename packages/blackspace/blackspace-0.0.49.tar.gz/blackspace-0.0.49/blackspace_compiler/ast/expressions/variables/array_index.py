from ....whitespace.printstr import print_str
from ....whitespace.snippets import ADD, DUPLICATE, PRINT_NUMBER, PUSH
from ...context import EvaluationContext, IssueLevel
from ...context.evaluation_context import increment_stack
from ...debugstatement import debug_instructions
from ...types.complex.array import ArrayType
from ...types.complex.memory import MemoryType
from ...types.complex.string import StringType
from ...types.primitives.int import IntegerType
from ...types.primitives.void import VoidType
from ...types.type import Type
from ...utils.error_message import type_error
from ..expression import Expression


class ArrayIndex(Expression):
    def __init__(self, array: Expression, index: Expression) -> None:
        super().__init__()
        self._array = array
        self._index = index

    def __repr__(self) -> str:
        return f"{self._array}[{self._index}]"

    def get_type(self, context: EvaluationContext) -> Type:
        arr_type = self._array.get_type(context)

        if isinstance(arr_type, ArrayType):
            return MemoryType(arr_type.of)
        elif isinstance(arr_type, StringType):
            return MemoryType(IntegerType())

        return VoidType()

    def evaluate(self, context: EvaluationContext) -> str:
        arr_type = self._array.get_type(context)
        if not isinstance(arr_type, (ArrayType, StringType)):
            context.register_issue(
                IssueLevel.ERROR,
                self._array,
                f"Type '{arr_type}' is not indexable.",
            )
            return ""

        index_type = self._index.get_type(context)
        if index_type != IntegerType():
            context.register_issue(
                IssueLevel.ERROR,
                self,
                type_error(IntegerType(), index_type, self._index),
            )
            return ""

        res = ""
        res += self._array.evaluate(context)
        with increment_stack(context):
            res += self._index.evaluate(context)
        res += PUSH(1) + ADD + ADD

        res += debug_instructions(
            print_str("Accessing array item at ") + DUPLICATE + PRINT_NUMBER + print_str("\n")
        )

        return res

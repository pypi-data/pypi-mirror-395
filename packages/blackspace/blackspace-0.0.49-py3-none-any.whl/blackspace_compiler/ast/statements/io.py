from enum import Enum

from ...whitespace.snippets import (
    ADD,
    COPY,
    DUPLICATE,
    FETCH,
    JUMP,
    JUMP_IF_ZERO,
    LABEL,
    POP,
    PRINT_CHAR,
    PRINT_NUMBER,
    PUSH,
    SUBTRACT,
    SWAP,
)
from ..context import EvaluationContext, IssueLevel
from ..expressions.expression import Expression
from ..types.complex.array import ArrayType
from ..types.complex.memory import MemoryType
from ..types.complex.string import StringType
from ..types.primitives.bool import BooleanType
from ..types.primitives.int import IntegerType
from .statement import Statement


class PrintMode(Enum):
    Number = 1
    Character = 2


class PrintStatement(Statement):

    def __init__(self, expression: Expression, print_mode: PrintMode = PrintMode.Number) -> None:
        super().__init__()
        self._expression = expression
        self._print_mode = print_mode

    def __repr__(self) -> str:
        return f"Print {self._expression} as {self._print_mode}"

    def evaluate(self, context: EvaluationContext) -> str:
        expr_type = self._expression.get_type(context)

        res = ""

        if expr_type == IntegerType() or expr_type == BooleanType():
            res += self._expression.evaluate(context)

            if self._print_mode == PrintMode.Character:
                res += PRINT_CHAR
            else:
                res += PRINT_NUMBER

        elif expr_type == StringType() or isinstance(expr_type, ArrayType):
            res += self._expression.evaluate(context)
            # In array/string types, the evaluated data points to the heap address where
            # the actual data is stored. The first location on the heap is the length of the data,
            # followed by the actual data items.

            res += DUPLICATE + DUPLICATE + FETCH + PUSH(1) + ADD + ADD
            # Stack: [start_address, end_address_exclusive]

            print_loop_start_label = context.label_registry.new_label()
            print_loop_end_label = context.label_registry.new_label()

            res += LABEL(print_loop_start_label)

            # increment the start address
            res += SWAP + PUSH(1) + ADD + SWAP

            # check if we've reached the end
            res += COPY(1) + COPY(1) + SUBTRACT + JUMP_IF_ZERO(print_loop_end_label)

            # fetch and print the current item
            res += COPY(1) + FETCH

            if self._print_mode == PrintMode.Character:
                res += PRINT_CHAR
            else:
                res += PRINT_NUMBER

            res += JUMP(print_loop_start_label)
            res += LABEL(print_loop_end_label)
            res += POP + POP

        elif isinstance(expr_type, MemoryType):
            res += self._expression.evaluate(context)
            res += PRINT_NUMBER

        else:
            context.register_issue(
                IssueLevel.ERROR,
                self,
                f"Cannot print expression of type {expr_type}",
            )

        return res

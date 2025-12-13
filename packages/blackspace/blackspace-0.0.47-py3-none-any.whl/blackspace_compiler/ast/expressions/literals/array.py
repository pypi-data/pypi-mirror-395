from ....whitespace.printstr import print_str
from ....whitespace.snippets import ADD, DUPLICATE, POP, PRINT_NUMBER, PUSH, STORE
from ...context import EvaluationContext, IssueLevel
from ...context.evaluation_context import increment_stack
from ...context.heap.helpers import allocate_data_on_heap
from ...debugstatement import debug_instructions, debug_statement
from ...types.complex.array import ArrayType
from ...types.primitives.void import VoidType
from ...types.type import Type
from ...utils.error_message import type_error
from ..expression import Expression


class ArrayLiteral(Expression):
    def __init__(self, items: list[Expression]) -> None:
        super().__init__()
        self._items = items

    def __repr__(self):
        return "[" + ", ".join(repr(item) for item in self._items) + "]"

    def get_type(self, context: EvaluationContext) -> Type:
        inner_type = self._items[0].get_type(context) if self._items else VoidType()
        return ArrayType(inner_type)

    def evaluate(self, context: EvaluationContext):
        first_item_type = self._items[0].get_type(context) if self._items else VoidType()
        for item in self._items:
            item_type = item.get_type(context)
            if item_type != first_item_type:
                context.register_issue(
                    IssueLevel.ERROR,
                    self,
                    type_error(first_item_type, item_type, item),
                )

        # get the starting location of the heap
        res = allocate_data_on_heap(context, len(self._items))

        res += debug_statement(f"Allocating array with {len(self._items)} items")

        res += DUPLICATE
        for i, item in enumerate(self._items):
            res += PUSH(1) + ADD + DUPLICATE

            res += debug_instructions(
                print_str("[") + DUPLICATE + PRINT_NUMBER + print_str("] = ")
            )

            with increment_stack(context, 3):
                res += item.evaluate(context)

            res += debug_instructions(DUPLICATE + PRINT_NUMBER + print_str("\n"))

            res += STORE
        res += POP

        return res

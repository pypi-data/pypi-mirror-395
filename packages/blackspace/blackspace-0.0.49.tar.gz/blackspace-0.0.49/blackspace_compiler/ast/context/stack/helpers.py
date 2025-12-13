from __future__ import annotations

from typing import TYPE_CHECKING

from ....whitespace.snippets import ADD, COPY, DUPLICATE, FETCH, POP, PUSH, STORE
from ...debugstatement import debug_statement
from ..heap.consts import FIRST_PROGRAM_STACK_HEAP_ADDRESS

if TYPE_CHECKING:
    from ..evaluation_context import EvaluationContext


# A function stack is a stack frame used during the evaluation of functions.
# When entering a function, a new stack frame is created to hold local variables and state.
# When exiting a function, the stack frame is removed, and control returns to the previous stack.
# The data of the stack frames is stored on the runtime heap.
# The stack data store location is pushed to the whitespace stack.


def _get_datastack_location(context: EvaluationContext) -> str:
    """Get the heap location of the current data stack."""
    return COPY(context.stack_offset)


def enter_first_stack(context: EvaluationContext) -> str:
    """Enter the first stack of the execution context."""
    _ = context  # Unused
    return (
        debug_statement("Entering first stack")
        + PUSH(FIRST_PROGRAM_STACK_HEAP_ADDRESS)
        + DUPLICATE
        + PUSH(1)
        + STORE
    )


def enter_new_stack(context: EvaluationContext) -> str:
    """Enter a new stack in the execution context. Assumes there is already at least one stack."""
    # Get the location of the current stack, get the length of the current stack,
    # add them together to the the start of the new stack.
    # Push 1 to the new stack to indicate its length is starting at 1.
    res = debug_statement(f"Entering new stack with stack offset {context.stack_offset}")
    res += _get_datastack_location(context)
    res += DUPLICATE + FETCH + ADD
    res += DUPLICATE + PUSH(1) + STORE
    return res


def exit_stack(context: EvaluationContext) -> str:
    """Exit the current stack in the execution context."""
    _ = context  # Unused
    return debug_statement(f"Exiting stack with stack offset {context.stack_offset}") + POP


def silently_allocate_on_datastack(context: EvaluationContext, length: int) -> str:
    """
    Allocate data on the current data stack.
    The starting location of the data is NOT pushed onto the whitespace stack.
    """
    res = _get_datastack_location(context)
    res += DUPLICATE + FETCH + PUSH(length) + ADD + STORE
    return res


def get_datastack_location(context: EvaluationContext, offset: int) -> str:
    """
    Get the heap location of the current data stack plus the given offset.
    **Skips the first element of the data stack, which is the length of the stack.**
    The resulting location is pushed onto the whitespace stack.
    The context stack offset is NOT incremented, that is the responsibility of the caller.
    """
    offset += 1  # Skip the length element
    res = _get_datastack_location(context)
    if offset != 0:
        res += PUSH(offset) + ADD
    return res

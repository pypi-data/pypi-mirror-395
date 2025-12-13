from __future__ import annotations

from typing import TYPE_CHECKING

from ....whitespace.snippets import ADD, DUPLICATE, FETCH, PUSH, STORE, SWAP
from ...debugstatement import debug_statement
from .consts import FREE_HEAP_ALLOCATION_COUNTER, FREE_HEAP_START

if TYPE_CHECKING:
    from ..evaluation_context import EvaluationContext


def initialize_heap(context: EvaluationContext) -> str:
    """
    Initialize the heap by setting up the heap allocation counter.
    This function should be called once at the start of the program execution.
    """
    _ = context  # Unused
    return (
        debug_statement("Initializing heap")
        + PUSH(FREE_HEAP_ALLOCATION_COUNTER)
        + PUSH(FREE_HEAP_START)
        + STORE
    )


def place_const_data_on_heap(context: EvaluationContext, data: list[int]) -> str:
    """
    Place constant data on the heap and return the starting address.
    This can be used for string literals or other constant data.
    The context stack offset is NOT incremented, that is the responsibility of the caller.
    """
    _ = context  # Unused

    # get the current free heap location address
    res = (
        debug_statement(f"Placing {len(data)} long const data on heap")
        + PUSH(FREE_HEAP_ALLOCATION_COUNTER)
        + FETCH
        + DUPLICATE
    )

    data = [len(data)] + data  # prepend length

    for i in range(len(data)):
        res += DUPLICATE
        res += PUSH(data[i]) + STORE
        res += PUSH(1) + ADD
    res += PUSH(FREE_HEAP_ALLOCATION_COUNTER) + SWAP + STORE
    return res


def allocate_data_on_heap(context: EvaluationContext, size: int) -> str:
    """
    Allocate space on the heap for a given size and return the starting address.
    The first word at that address will contain the size of the allocated block.
    The context stack offset is NOT incremented, that is the responsibility of the caller.
    """
    _ = context  # Unused

    # get the current free heap location address
    res = (
        debug_statement(f"Allocating {size} long space on heap")
        + PUSH(FREE_HEAP_ALLOCATION_COUNTER)
        + FETCH
    )

    # on the free location, first store the size
    res += DUPLICATE + PUSH(size) + STORE

    # increment the free heap location by size + 1
    res += DUPLICATE + PUSH(size + 1) + ADD
    res += PUSH(FREE_HEAP_ALLOCATION_COUNTER) + SWAP + STORE

    return res

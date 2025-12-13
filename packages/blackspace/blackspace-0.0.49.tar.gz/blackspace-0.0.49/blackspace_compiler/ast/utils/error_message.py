from ..node import AstNode
from ..types.type import Type


def type_error(expected_type: Type, acutal_type: Type, node: AstNode) -> str:
    _ = node  # Unused for now, but could be used for more detailed error messages
    return f"Expected type {expected_type}, but got {acutal_type}."

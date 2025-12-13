from dataclasses import dataclass

from ..types.type import Type


@dataclass
class VariableDefinition:
    name: str
    type: Type
    is_mutable: bool

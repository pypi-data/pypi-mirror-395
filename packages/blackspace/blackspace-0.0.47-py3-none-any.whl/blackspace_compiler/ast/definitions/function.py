from __future__ import annotations

from dataclasses import dataclass

from ..types.type import Type
from .variable import VariableDefinition


@dataclass
class ParameterDefinition:
    name: str
    type: Type


@dataclass
class FunctionSignature:
    name: str
    parameters: list[ParameterDefinition]
    return_type: Type
    variables: list[VariableDefinition]

    def assert_correct_variable_configuration(self) -> None:
        """
        Validates that the function variable setup is correct according to the parameters.
        Each parameter will be stored into a variable by the same name. The first N variables
        must match the N parameters.
        """
        if len(self.variables) < len(self.parameters):
            raise RuntimeError(
                f"Function '{self.name}' has fewer variables ({len(self.variables)}) "
                f"than parameters ({len(self.parameters)})."
            )
        for i in range(len(self.parameters)):
            param = self.parameters[i]
            var = self.variables[i]
            if param.name != var.name:
                raise RuntimeError(
                    f"Function '{self.name}' parameter {i} name '{param.name}' does not match "
                    f"variable name '{var.name}'."
                )
            if param.type != var.type:
                raise RuntimeError(
                    f"Function '{self.name}' parameter {i} type '{param.type}' does not match "
                    f"variable type '{var.type}'."
                )

    def get_variable(self, name: str) -> VariableOffset | None:
        offset = 0
        for variable in self.variables:
            if variable.name == name:
                return VariableOffset(definition=variable, offset=offset)
            else:
                offset += variable.type.get_size()
        return None


@dataclass
class VariableOffset:
    definition: VariableDefinition
    offset: int

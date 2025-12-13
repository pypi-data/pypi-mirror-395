from abc import ABC, abstractmethod

from ..context import EvaluationContext
from ..node import AstNode
from ..types.type import Type


class Expression(AstNode, ABC):

    @abstractmethod
    def get_type(self, context: EvaluationContext) -> Type:
        pass

    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> str:
        pass

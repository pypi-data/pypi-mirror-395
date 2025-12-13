from abc import ABC, abstractmethod

from ..context import EvaluationContext
from ..node import AstNode


class Statement(AstNode, ABC):
    @abstractmethod
    def evaluate(self, context: EvaluationContext) -> str:
        pass

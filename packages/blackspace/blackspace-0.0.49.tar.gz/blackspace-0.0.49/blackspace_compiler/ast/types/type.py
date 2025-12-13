from abc import ABC, abstractmethod


class Type(ABC):

    @abstractmethod
    def get_size(self) -> int:
        """Gets the size of the data in heap cells."""
        pass

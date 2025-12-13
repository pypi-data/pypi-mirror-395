from ..type import Type


class MemoryType(Type):
    def __init__(self, of: Type):
        super().__init__()
        self.of = of

    def __repr__(self):
        return f"Memory<{self.of}>"

    def __eq__(self, value):
        return isinstance(value, MemoryType) and self.of == value.of

    def get_size(self):
        return 1

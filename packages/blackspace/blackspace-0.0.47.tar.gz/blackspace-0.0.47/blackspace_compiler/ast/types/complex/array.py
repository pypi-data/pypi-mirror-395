from ..type import Type


class ArrayType(Type):
    def __init__(self, of: Type):
        super().__init__()
        self.of = of

    def __repr__(self):
        return f"Array<{self.of}>"

    def __eq__(self, value):
        return isinstance(value, ArrayType) and self.of == value.of

    def get_size(self):
        return 1

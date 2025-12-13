from ..type import Type


class IntegerType(Type):
    def __repr__(self):
        return "Integer"

    def __eq__(self, value):
        return isinstance(value, IntegerType)

    def get_size(self):
        return 1

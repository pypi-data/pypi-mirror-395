from ..type import Type


class BooleanType(Type):
    def __repr__(self):
        return "Boolean"

    def __eq__(self, value):
        return isinstance(value, BooleanType)

    def get_size(self):
        return 1

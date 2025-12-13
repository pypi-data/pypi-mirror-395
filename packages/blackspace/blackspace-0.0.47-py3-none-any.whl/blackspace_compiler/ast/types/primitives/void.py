from ..type import Type


class VoidType(Type):
    def __repr__(self):
        return "Void"

    def __eq__(self, value):
        return isinstance(value, VoidType)

    def get_size(self):
        return 0

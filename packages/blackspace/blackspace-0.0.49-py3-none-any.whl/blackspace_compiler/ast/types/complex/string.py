from ..type import Type


class StringType(Type):
    def __repr__(self):
        return "String"

    def __eq__(self, value):
        return isinstance(value, StringType)

    def get_size(self):
        return 1

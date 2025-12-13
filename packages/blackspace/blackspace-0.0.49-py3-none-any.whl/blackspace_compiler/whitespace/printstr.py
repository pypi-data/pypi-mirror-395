from .snippets import PRINT_CHAR, PUSH


def print_str(value: str) -> str:
    res = ""
    for char in value:
        res += PUSH(ord(char))
        res += PRINT_CHAR
    return res

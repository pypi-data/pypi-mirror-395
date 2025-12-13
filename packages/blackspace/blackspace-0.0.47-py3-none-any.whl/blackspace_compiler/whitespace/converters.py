from .tokens import LF, SPACE, TAB


def to_ws_number(value: int) -> str:
    ret = ""
    if value >= 0:
        ret += SPACE
    else:
        ret += TAB
        value = -value

    binary = bin(value)[2:]
    for bit in binary:
        if bit == "0":
            ret += SPACE
        else:
            ret += TAB

    ret += LF

    return ret

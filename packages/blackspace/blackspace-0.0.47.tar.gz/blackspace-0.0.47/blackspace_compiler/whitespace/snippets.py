from .converters import to_ws_number
from .tokens import LF, SPACE, TAB

PUSH = lambda n: SPACE + SPACE + to_ws_number(n)  # noqa: E731
POP = SPACE + LF + LF
SWAP = SPACE + LF + TAB
DUPLICATE = SPACE + LF + SPACE
COPY = lambda n: SPACE + TAB + SPACE + to_ws_number(n)  # noqa: E731
SLIDE = lambda n: SPACE + TAB + LF + to_ws_number(n)  # noqa: E731

ADD = TAB + SPACE + SPACE + SPACE
SUBTRACT = TAB + SPACE + SPACE + TAB
MULTIPLY = TAB + SPACE + SPACE + LF
DIVIDE = TAB + SPACE + TAB + SPACE
MODULO = TAB + SPACE + TAB + TAB

FETCH = TAB + TAB + TAB
STORE = TAB + TAB + SPACE

LABEL = lambda n: LF + SPACE + SPACE + to_ws_number(n)  # noqa: E731
CALL = lambda n: LF + SPACE + TAB + to_ws_number(n)  # noqa: E731
JUMP = lambda n: LF + SPACE + LF + to_ws_number(n)  # noqa: E731
JUMP_IF_ZERO = lambda n: LF + TAB + SPACE + to_ws_number(n)  # noqa: E731
JUMP_IF_NEG = lambda n: LF + TAB + TAB + to_ws_number(n)  # noqa: E731
RETURN = LF + TAB + LF
END = LF + LF + LF

PRINT_CHAR = TAB + LF + SPACE + SPACE
PRINT_NUMBER = TAB + LF + SPACE + TAB
READ_CHAR = TAB + LF + TAB + SPACE
READ_NUMBER = TAB + LF + TAB + TAB

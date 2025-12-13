from ..whitespace.printstr import print_str

ENABLE_DEBUG = False


def debug_statement(text: str) -> str:
    if not ENABLE_DEBUG:
        return ""
    return (
        code_comment(f"DEBUG: {text}")
        + print_str(f"DEBUG: {text}\n")
        + code_comment("// end of debug statement print")
    )


def debug_instructions(instructions: str) -> str:
    if not ENABLE_DEBUG:
        return ""
    return instructions


def code_comment(text: str) -> str:
    if "\n" in text:
        raise ValueError("Code comments cannot contain newlines")
    if "\t" in text:
        raise ValueError("Code comments cannot contain tabs")
    return text.replace(" ", "·")

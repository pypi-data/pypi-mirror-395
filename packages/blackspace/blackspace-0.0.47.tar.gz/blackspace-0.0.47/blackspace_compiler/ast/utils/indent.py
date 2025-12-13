def indent(text: str, indent_str: str = "  ") -> str:
    """Indents all lines in the given text with the given intent string."""
    lines = text.splitlines()
    indented_lines = [f"{indent_str}{line}" for line in lines]
    return "\n".join(indented_lines)

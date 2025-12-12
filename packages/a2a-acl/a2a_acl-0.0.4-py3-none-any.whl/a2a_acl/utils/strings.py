def neutralize_str(s: str) -> str:
    """Add quotes to a string."""
    return '"' + s + '"'


def clear(s: str):
    """Remove quotes from a string."""
    if s.startswith('"') and s.endswith('"'):
        return s.removeprefix('"').removesuffix('"')
    elif s.startswith("'") and s.endswith("'"):
        return s.removeprefix("'").removesuffix("'")
    else:
        return s

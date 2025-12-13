def validate_hex(inp: str):
    if all(c in '0123456789abcdef' for c in inp.lower()) and len(inp) == 6:
        return True
    return False
def escape_key(key: str, escape="\\", sep="."):
    """Escape separators inside keys."""
    return key.replace(escape, escape + escape).replace(sep, escape + sep)


def unescape_key(key: str, escape="\\", sep="."):
    """Unescape separators."""
    i = 0
    out = []
    while i < len(key):
        if key[i] == escape:
            i += 1
            if i < len(key):
                out.append(key[i])
        else:
            out.append(key[i])
        i += 1
    return "".join(out)


def validate_path(path: str) -> bool:
    """Make sure path is syntactically valid."""
    if ".." in path:
        return False
    return True

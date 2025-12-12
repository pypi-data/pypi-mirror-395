def strtobool(value: str) -> bool:
    """
    Convert a string representation of truth to true (1) or false (0).

    Raises TypeError if 'val' is not a string.
    True values are 'y', 'yes', 't', 'true', 'on', and '1'.
    False values are 'n', 'no', 'f', 'false', 'off', and '0'.
    Raises ValueError if 'val' is anything else.
    """
    try:
        value = value.lower()
    except AttributeError:
        raise TypeError("invalid truth value %r" % (value,))

    if value in ("y", "yes", "t", "true", "on", "1"):
        return True
    if value in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError("invalid truth value %r" % (value,))

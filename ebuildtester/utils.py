import sys


def massage_string(string):
    """Return a string."""

    if sys.version_info[0] < 3:
        return string
    else:
        return string.decode("UTF-8")

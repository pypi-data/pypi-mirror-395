import os


def ensure_trailing_slash(val, delimiter: str = None):
    if delimiter is None:
        delimiter = os.sep
    v2 = val.strip()
    if not v2.endswith(delimiter):
        v2 = v2 + delimiter
    return v2


def ensure_trailing_slash_url(val):
    return ensure_trailing_slash(val, '/')


def ensure_beginning_slash_url(val):
    v = val.strip()
    if not v.startswith('/'):
        v = '/' + v
    return v


def remove_trailing_slash_url(val):
    v = val.strip()
    if v.endswith('/'):
        v = v[:-1]
    return v

from functools import wraps
from typing import Callable, Optional


def with_fallback(f: Optional[Callable] = None, fallback=None, exceptions=Exception):
    def wrapper(fun):
        @wraps(fun)
        def wrapped(*args, **kwargs):
            try:
                return fun(*args, **kwargs)
            except exceptions:
                return fallback

        if exceptions is not None:
            return wrapped
        else:
            return fun

    if f is None:
        return wrapper
    else:
        return wrapper(f)

import functools
from collections.abc import Generator
from typing import Iterator


class ContextIterator(Generator):
    """Can wrap an iterator or generator to ensure cleanup when used as a context manager."""

    def __init__(self, it: Iterator):
        self._it = it

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._it)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if hasattr(self._it, "close"):
            return self._it.close()

    def send(self, value):
        if hasattr(self._it, "send"):
            return self._it.send(value)

    def throw(self, *args):
        if hasattr(self._it, "throw"):
            return self._it.throw(*args)


def contextiterator(iterator):
    """Decorator that allows to use an iterator or generator as a context manager.
    This ensures that the iterator is closed when exiting the context manager.
    """

    @functools.wraps(iterator)
    def wrapper(*args, **kw):
        return ContextIterator(iterator(*args, **kw))

    return wrapper

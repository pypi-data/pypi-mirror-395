from abc import ABCMeta

from .abstract import AbstractSpan


class DefaultSpan(AbstractSpan, metaclass=ABCMeta):
    __slots__ = ('_start', '_end')

    def __init__(self, start: int, end: int, *, nullable=False):
        self._start = start
        self._end = end

        if not (0 <= self._start <= self._end):
            raise Exception(f"Incorrect span range [{self._start}; {self._end})")
        if not nullable and self._start == self._end:
            raise Exception("Incorrect span range")

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def length(self) -> int:
        return self._end - self._start

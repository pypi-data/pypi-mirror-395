from functools import total_ordering
from typing import Tuple

from .default import DefaultSpan


@total_ordering
class Span(DefaultSpan):
    __slots__ = ()

    def __init__(self, start: int, end: int):
        super().__init__(start, end)

    def shift(self, shift: int) -> 'Span':
        if not shift:
            return self
        return Span(self._start + shift, self._end + shift)

    def _as_tuple(self) -> Tuple[int, int]:
        return self._start, self._end

    def __eq__(self, other):
        if not isinstance(other, Span):
            return NotImplemented
        return other._as_tuple() == self._as_tuple()

    def __lt__(self, other):
        if not isinstance(other, Span):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def __repr__(self):
        return repr(self._as_tuple())

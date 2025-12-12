from functools import total_ordering

from .default import DefaultSpan


@total_ordering
class NullableSpan(DefaultSpan):
    __slots__ = ()

    def __init__(self, start: int, end: int):
        super().__init__(start, end, nullable=True)

    def shift(self, shift: int) -> 'NullableSpan':
        return NullableSpan(self._start + shift, self._end + shift)

    def _as_tuple(self) -> tuple[int, int]:
        return self.start, self.end

    def __eq__(self, other):
        if not isinstance(other, NullableSpan):
            return NotImplemented
        return other._as_tuple() == self._as_tuple()

    def __hash__(self):
        return hash(self._as_tuple())

    def __repr__(self):
        return repr(self._as_tuple())

    def __lt__(self, other):
        if not isinstance(other, NullableSpan):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()

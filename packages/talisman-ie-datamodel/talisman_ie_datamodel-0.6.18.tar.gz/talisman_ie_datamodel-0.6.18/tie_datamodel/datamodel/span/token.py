from typing import Optional

from .span import Span


class Token(Span):
    __slots__ = (
        '_label', '_parent'
    )

    def __init__(self, start: int, end: int, label: Optional[str] = None, parent: Optional[Span] = None):
        if (label is None) != (parent is None):
            raise ValueError
        super().__init__(start, end)
        self._label = label
        self._parent = parent

    @property
    def is_root(self) -> bool:
        return self._parent is None

    @property
    def parent(self) -> Optional[tuple[str, Span]]:
        if self.is_root:
            return None
        return self._label, self._parent

    def shift(self, shift: int) -> 'Token':
        if not shift:
            return self
        return Token(self._start + shift, self._end + shift, self._label, self._parent.shift(shift) if self._parent is not None else None)

    @classmethod
    def from_span(cls, span: Span, label: Optional[str], parent: Optional[Span]):
        return cls(span.start, span.end, label, parent)

from abc import ABCMeta, abstractmethod
from typing import TypeVar

_AbstractSpan = TypeVar('_AbstractSpan', bound='AbstractSpan')


class AbstractSpan(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def start(self) -> int:
        pass

    @property
    @abstractmethod
    def end(self) -> int:
        pass

    @property
    def length(self) -> int:
        return self.end - self.start

    @abstractmethod
    def shift(self: _AbstractSpan, shift: int) -> _AbstractSpan:
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    def coincides(self, obj: 'AbstractSpan') -> bool:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return self.start == obj.start and self.end == obj.end

    def intersects(self, obj: 'AbstractSpan') -> bool:
        return self._distance(obj) < 0

    def distance(self, obj: 'AbstractSpan') -> int:
        return max(0, self._distance(obj))

    def _distance(self, obj: 'AbstractSpan') -> int:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return max(self.start, obj.start) - min(self.end, obj.end)

    def contains(self, obj: 'AbstractSpan') -> bool:
        if not isinstance(obj, AbstractSpan):
            raise TypeError(f"expected {AbstractSpan}, got {type(obj)}")
        return self.start <= obj.start and self.end >= obj.end

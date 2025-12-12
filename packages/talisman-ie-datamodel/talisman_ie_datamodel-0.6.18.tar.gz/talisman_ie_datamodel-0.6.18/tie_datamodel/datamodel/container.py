from itertools import tee
from operator import attrgetter
from typing import Callable, FrozenSet, Generic, Iterable, Iterator, List, Sequence, Tuple, TypeVar

from intervaltree import IntervalTree

from .span import AbstractSpan

_SpansMeta = TypeVar('_SpansMeta', bound=AbstractSpan)


class SpanContainer(Sequence[_SpansMeta], Generic[_SpansMeta]):
    __slots__ = ('_spans', '_sorted_spans', '_interval_tree')

    def __init__(self, spans: Iterable[_SpansMeta], *, spans_sorted: bool = False):
        if isinstance(spans, SpanContainer):
            self._spans = spans._spans
            self._sorted_spans = spans._sorted_spans
            self._interval_tree = spans._interval_tree
            return

        if spans_sorted:
            self._sorted_spans = LazyEvalWrapper(lambda: tuple(spans))
            self._sorted_spans.evaluate()
            self._spans = LazyEvalWrapper(self._init_spans_from_sorted_spans)
        else:
            self._spans = LazyEvalWrapper(lambda: frozenset(spans))
            self._spans.evaluate()
            self._sorted_spans = LazyEvalWrapper(self._init_sorted_spans_from_spans)

        self._interval_tree = LazyEvalWrapper(self._initialize_interval_tree)

    def _init_spans_from_sorted_spans(self) -> FrozenSet[_SpansMeta]:
        return frozenset(self._sorted_spans.value)

    def _init_sorted_spans_from_spans(self) -> Tuple[_SpansMeta, ...]:
        return tuple(sorted(self._spans.value))

    def _initialize_interval_tree(self) -> IntervalTree:
        return IntervalTree.from_tuples((span.start, span.end, idx) for idx, span in enumerate(self._sorted_spans.value))

    def spans_at(self, span: AbstractSpan) -> Tuple[_SpansMeta, ...]:
        indices = self.spans_indices_at(span)
        return tuple(self._sorted_spans.value[idx] for idx in indices)

    def spans_indices_at(self, span: AbstractSpan) -> List[int]:
        intervals = self._interval_tree.value.overlap(span.start, span.end)
        return sorted(map(attrgetter('data'), intervals))

    def spans_contained_in(self, span: AbstractSpan) -> Tuple[_SpansMeta, ...]:
        indices = self.spans_indices_contained_in(span)
        return tuple(self._sorted_spans.value[idx] for idx in indices)

    def spans_indices_contained_in(self, span: AbstractSpan) -> List[int]:
        intervals = self._interval_tree.value.envelop(span.start, span.end)
        return sorted(map(attrgetter('data'), intervals))

    def iterate_objects_with_same_spans(self) -> Iterator[Tuple[_SpansMeta, ...]]:
        if not len(self._sorted_spans.value):
            return

        stack = [self._sorted_spans.value[0]]
        for span in self._sorted_spans.value[1:]:
            if span.coincides(stack[0]):
                stack.append(span)
            else:
                yield tuple(stack)
                stack = [span]

        yield tuple(stack)

    def has_overlap(self) -> bool:
        if not self._sorted_spans.value:
            return False

        previous, current = tee(self._sorted_spans.value)
        next(current, None)

        for p, c in zip(previous, current):
            if p.end_idx > c.start_idx:
                return True

        return False

    def __len__(self):
        if self._sorted_spans.evaluated:
            return len(self._sorted_spans.value)
        return len(self._spans.value)

    def __getitem__(self, idx) -> _SpansMeta:
        return self._sorted_spans.value[idx]

    def __contains__(self, item: _SpansMeta):
        return item in self._spans.value

    def __eq__(self, other):
        if not isinstance(other, SpanContainer):
            return NotImplemented

        if self._sorted_spans.evaluated and other._sorted_spans.evaluated:
            return self._sorted_spans.value == self._sorted_spans.value

        return self._spans.value == other._spans.value

    def __hash__(self):
        return hash(self._spans.value)

    def __repr__(self):
        return repr(self._sorted_spans.value)


_T = TypeVar('_T')


class LazyEvalWrapper(Generic[_T]):
    """
    Straight clear version of cached property. Can be used with __slots__-containing classes.
    func, *args, **kwargs references are hold until .value is requested and initialized.

    *args and **kwargs can be specified in __init__ to make LazyEvalWrapper picklable (if func, *args, **kwargs are picklable).
    """
    __slots__ = ('_func', '_func_args', '_func_kwargs', '_evaluated', '_value')

    def __init__(self, func: Callable[..., _T], *args, **kwargs):
        self._func = func
        self._func_args = args
        self._func_kwargs = kwargs

        self._evaluated = False
        self._value = None

    def evaluate(self):
        if self._evaluated:
            return

        self._value = self._func(*self._func_args, **self._func_kwargs)
        self._evaluated = True
        self._func, self._func_args, self._func_kwargs = None, None, None

    @property
    def evaluated(self) -> bool:
        return self._evaluated

    @property
    def value(self) -> _T:
        self.evaluate()
        return self._value

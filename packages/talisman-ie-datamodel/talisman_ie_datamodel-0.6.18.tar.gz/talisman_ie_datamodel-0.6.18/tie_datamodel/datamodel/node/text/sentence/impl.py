from functools import total_ordering
from typing import Iterable, Iterator, Optional

from tie_datamodel.datamodel.container import SpanContainer
from tie_datamodel.datamodel.span import AbstractSpan, Span, Token


@total_ordering
class Sentence(AbstractSpan, SpanContainer[Span]):
    __slots__ = ('_sentence_span',)

    def __init__(
            self,
            span: AbstractSpan, tokens: Iterable[Span],
            *, tokens_sorted: bool = False, validate: bool = True
    ):
        SpanContainer[Span].__init__(self, tokens, spans_sorted=tokens_sorted)
        AbstractSpan.__init__(self)

        self._sentence_span = span

        if validate:
            self._validate()

    def _validate(self):
        if not len(self._sorted_spans.value):
            raise Exception("Sentence must contain at least one token")

        if not (self.start <= self._sorted_spans.value[0].start < self._sorted_spans.value[-1].end <= self.end):
            raise Exception("Provided tokens not in sentence start-end")

        # TODO: add validation for intersecting tokens

    @property
    def start(self) -> int:
        return self._sentence_span.start

    @property
    def end(self) -> int:
        return self._sentence_span.end

    @property
    def length(self) -> int:
        return self._sentence_span.length

    def shift(self, shift: int) -> 'Sentence':
        if not shift:
            return self

        if self._sorted_spans.evaluated:
            tokens = self._sorted_spans.value
            tokens_sorted = True
        else:
            tokens = self._spans.value
            tokens_sorted = False

        return self.__class__(
            self._sentence_span.shift(shift),
            (s.shift(shift) for s in tokens),
            tokens_sorted=tokens_sorted, validate=False
        )

    def _as_tuple(self, *, use_sorted_spans: bool = False):
        return self._sentence_span, (self._sorted_spans.value if use_sorted_spans else self._spans.value)

    def __eq__(self, other):
        if not isinstance(other, Sentence):
            return NotImplemented

        both_sorted = self._sorted_spans.evaluated and other._sorted_spans.evaluated
        return self._as_tuple(use_sorted_spans=both_sorted) == other._as_tuple(use_sorted_spans=both_sorted)

    def __lt__(self, other):
        if not isinstance(other, Sentence):
            return NotImplemented
        return self._sentence_span < other._sentence_span

    def __hash__(self):
        return hash(self._as_tuple())

    def __repr__(self):
        return repr(self._as_tuple(use_sorted_spans=self._sorted_spans.evaluated))


@total_ordering
class SentenceWithSyntax(Sentence):
    __slots__ = (
        '_root', '_children', '_parents'
    )

    def __init__(
            self,
            span: AbstractSpan, tokens: Iterable[Span],
            root: int,
            parents: tuple[Optional[tuple[str, int]], ...],
            children: tuple[frozenset[int], ...],
            *, tokens_sorted: bool = False, validate: bool = True
    ):
        self._root = root
        self._parents = parents
        self._children = children

        super().__init__(span, tokens, tokens_sorted=tokens_sorted, validate=validate)

    def _validate(self):
        super()._validate()

        if self._root is not None:
            if not (len(self) == len(self._parents) == len(self._children)):
                raise ValueError
            if not 0 <= self._root <= len(self):
                raise ValueError
            if self._parents[self._root] is not None:
                raise ValueError

    def shift(self, shift: int) -> 'SentenceWithSyntax':
        if not shift:
            return self

        if self._sorted_spans.evaluated:
            tokens = self._sorted_spans.value
            tokens_sorted = True
        else:
            tokens = self._spans.value
            tokens_sorted = False

        return self.__class__(
            self._sentence_span.shift(shift),
            (s.shift(shift) for s in tokens),
            self._root, self._parents, self._children,
            tokens_sorted=tokens_sorted, validate=False
        )

    @property
    def root(self) -> Token:
        return Token.from_span(self[self._root], None, None)

    def children(self, token: Span) -> Iterator[Token]:
        indices = self.spans_indices_at(token)
        if len(indices) != 1 or not token.coincides(super().__getitem__(indices[0])):
            raise ValueError
        return map(self.__getitem__, self._children[indices[0]])

    def __getitem__(self, idx) -> Token:
        if idx == self._root:
            return Token.from_span(self._sorted_spans.value[idx], None, None)
        label, parent = self._parents[idx]
        return Token.from_span(super().__getitem__(idx), label, super().__getitem__(parent))

    def _as_tuple(self, *, use_sorted_spans: bool = False):
        return self.start, self.end, (self._sorted_spans.value if use_sorted_spans else self._spans.value)

    def __eq__(self, other):
        if not isinstance(other, SentenceWithSyntax):
            return NotImplemented

        both_sorted = self._sorted_spans.evaluated and other._sorted_spans.evaluated
        return self._as_tuple(use_sorted_spans=both_sorted) == other._as_tuple(use_sorted_spans=both_sorted) and \
            self._parents == other._parents

    def __lt__(self, other):
        if not isinstance(other, Sentence):
            return NotImplemented
        return self._sentence_span < other._sentence_span

    def __hash__(self):
        return hash((self._sentence_span, self._spans.value))

    def __repr__(self):
        return repr(self._as_tuple(use_sorted_spans=self._sorted_spans.evaluated))

    @classmethod
    def from_sentence(cls, sentence: Sentence, tree: tuple[Optional[tuple[str, int]], ...]) -> 'SentenceWithSyntax':
        if len(sentence) != len(tree):
            raise ValueError
        root = None
        children = [set() for _ in range(len(sentence))]
        for i, parent in enumerate(tree):
            if parent is None:
                if root is not None:
                    raise ValueError
                root = i
            else:
                children[parent[1]].add(i)
        if root is None:
            raise ValueError
        return cls(
            span=sentence._sentence_span,
            tokens=sentence,
            root=root, parents=tree,
            children=tuple(map(frozenset, children))
        )

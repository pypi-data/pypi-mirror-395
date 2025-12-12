from dataclasses import dataclass, field
from functools import total_ordering
from typing import Optional

from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.span import AbstractSpan, Span


@total_ordering
@dataclass(frozen=True)
class Mention(TextNodeMention):
    confidence: Optional[float] = field(default=None, compare=False)

    def tuple(self):
        return self.node_id, self.start, self.end, self.confidence if self.confidence is not None else 1.0

    def __repr__(self):
        return repr(self.tuple())

    def __hash__(self):
        return hash(self.tuple())

    def __eq__(self, other):
        if not isinstance(other, Mention):
            return NotImplemented
        return self.tuple() == other.tuple()

    def __lt__(self, other):
        if not isinstance(other, Mention):
            return NotImplemented
        return self.tuple() < other.tuple()


class MentionSpan(Span):
    __slots__ = (
        '_confidence',
    )

    def __init__(self, start: int, end: int, confidence: Optional[float] = None):
        super().__init__(start, end)
        self._confidence = confidence

    @classmethod
    def from_span(cls, span: AbstractSpan, confidence: Optional[float] = None) -> 'MentionSpan':
        return cls(span.start, span.end, confidence=confidence)

    @classmethod
    def from_mention(cls, mention: Mention) -> 'MentionSpan':
        return cls(mention.start, mention.end, mention.confidence)

    def mention(self, node: TextNode) -> Mention:
        return Mention(node, self._start, self._end, self._confidence)

    @property
    def confidence(self) -> Optional[float]:
        return self._confidence

    def with_confidence(self, confidence: float, force: bool = False) -> 'MentionSpan':
        if self._confidence is not None and not force:
            raise Exception("Mention already provides confidence")

        return self.from_span(self, confidence)

    def without_confidence(self) -> 'MentionSpan':
        return self.from_span(self, confidence=None)

    def shift(self, shift: int) -> 'MentionSpan':
        if not shift:
            return self
        return MentionSpan(self._start + shift, self._end + shift, self._confidence)

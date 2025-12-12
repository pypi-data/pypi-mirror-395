from itertools import starmap
from typing import Optional, Tuple

from pydantic import BaseModel

from tie_datamodel.datamodel.span import AbstractSpan, Span
from .impl import Sentence, SentenceWithSyntax

SpanJSONModel = tuple[int, int]  # [start, end) span
ParentModel = Optional[tuple[str, int]]  # label, parent token id


class SentenceJSONModel(BaseModel):
    span: SpanJSONModel
    tokens: Tuple[SpanJSONModel, ...]
    tree: Optional[tuple[ParentModel, ...]] = None

    def to_sentence(self) -> Sentence | SentenceWithSyntax:
        sentence = Sentence(Span(*self.span), starmap(Span, self.tokens))
        if self.tree is not None:
            return SentenceWithSyntax.from_sentence(sentence, self.tree)
        return sentence

    @classmethod
    def build(cls, sentence: Sentence | SentenceWithSyntax):
        tree = None
        if isinstance(sentence, SentenceWithSyntax):
            tree = sentence._parents
        return cls.model_construct(
            span=build_span_json_model(sentence),
            tokens=tuple(map(build_span_json_model, sentence)),
            tree=tree
        )


def build_span_json_model(span: AbstractSpan) -> SpanJSONModel:
    return span.start, span.end

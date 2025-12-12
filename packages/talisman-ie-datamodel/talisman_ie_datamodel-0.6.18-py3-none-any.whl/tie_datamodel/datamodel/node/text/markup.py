from itertools import chain
from typing import Dict, FrozenSet, Iterable, Iterator, Optional, Type, TypeVar

from immutabledict import immutabledict
from tdm.abstract.datamodel import AbstractMarkup

from tie_datamodel.datamodel.container import SpanContainer
from tie_datamodel.datamodel.span import AbstractSpan, Span
from .abstract import AbstractTIENode
from .chain import CoreferenceChain
from .chain.mention import MentionSpan
from .model import TIEMarkupModel
from .sentence import Sentence

_TIENodeMarkup = TypeVar('_TIENodeMarkup', bound='TIENodeMarkup')


class TIENodeMarkup(AbstractMarkup, AbstractTIENode):
    __slots__ = (
        '_sentences', '_chains', '_key_sentence_idx'
    )

    def __init__(
            self,
            sentences: Optional[Iterable[Sentence]] = None,
            chains: Optional[Dict[str, tuple[MentionSpan, ...]]] = None,
            key_sentence_idx: Optional[int] = None
    ):
        self._sentences = SpanContainer(sentences) if sentences is not None else None
        self._chains = dict(chains) if chains is not None else None
        self._key_sentence_idx = key_sentence_idx

    @property
    def markup(self) -> immutabledict:
        return TIEMarkupModel.build(self._sentences, self._chains, self._key_sentence_idx).immutabledict()

    @classmethod
    def from_markup(cls: Type[_TIENodeMarkup], markup: 'AbstractMarkup') -> _TIENodeMarkup:
        model: TIEMarkupModel = TIEMarkupModel.model_validate(markup.markup)
        return cls(model.get_sentences(), model.get_coref_chains(), model.get_key_sentence_idx())

    @property
    def has_language(self) -> bool:
        raise NotImplementedError

    def language(self) -> str:
        raise NotImplementedError

    @property
    def has_sentences(self) -> bool:
        return self._sentences is not None

    @property
    def sentences(self) -> SpanContainer[Sentence]:
        if self._sentences is None:
            raise AttributeError
        return self._sentences

    @property
    def tokens(self) -> Iterator[Span]:
        if self._sentences is None:
            raise AttributeError
        return chain.from_iterable(self.sentences)

    def with_sentences(self: _TIENodeMarkup, sentences: Iterable[Sentence]) -> _TIENodeMarkup:
        return TIENodeMarkup(sentences, self._chains, self._key_sentence_idx)

    @property
    def has_chains(self) -> bool:
        return self._chains is not None

    def chains_for(self, span: AbstractSpan) -> dict[str, FrozenSet[MentionSpan]]:  # here changed return value. postprocessing is needed
        # inefficient implementation
        if self._chains is None:
            raise AttributeError
        mention = MentionSpan.from_span(span)
        return {
            key: mentions for key, mentions in self._chains.items() if mention in mentions
        }

    @property
    def chains(self) -> immutabledict[str, FrozenSet[MentionSpan]]:  # here changed return value. postprocessing is needed
        if self._chains is None:
            raise AttributeError
        return immutabledict(self._chains)

    def with_chains(self: _TIENodeMarkup, chains: Iterable[CoreferenceChain]) -> _TIENodeMarkup:
        if self._chains is not None and any(c.id in self._chains for c in chains):
            raise ValueError

        return TIENodeMarkup(
            sentences=self._sentences,
            chains={
                **(self._chains or {}),
                **{cchain.id: tuple(map(MentionSpan.from_mention, cchain)) for cchain in chains if cchain.mentions}
            },
            key_sentence_idx=self._key_sentence_idx
        )

    def without_chains(self: _TIENodeMarkup) -> _TIENodeMarkup:
        return TIENodeMarkup(self._sentences, None, self._key_sentence_idx)

    @property
    def key_sentence_idx(self) -> int:
        return self._key_sentence_idx

    @property
    def has_key_sentence_idx(self) -> bool:
        return self._key_sentence_idx is not None

    def with_key_sentence_idx(self: _TIENodeMarkup, key_sentence_idx: int) -> _TIENodeMarkup:
        return TIENodeMarkup(self._sentences, self._chains, key_sentence_idx)

from abc import ABCMeta
from itertools import chain
from typing import FrozenSet, Iterable, Mapping, Sequence, Tuple

from tdm.abstract.datamodel import AbstractMarkup
from tdm.datamodel.nodes import TextNode
from tdm.wrapper.node import AbstractNodeWrapper, composite_markup, generate_wrapper, post_process, validate

from tie_datamodel.datamodel.container import SpanContainer
from .abstract import AbstractTIENode
from .chain import CoreferenceChain
from .chain.mention import MentionSpan
from .markup import TIENodeMarkup
from .sentence import Sentence


@composite_markup(ie=TIENodeMarkup)
class _CompositeMarkup(AbstractMarkup, AbstractTIENode, metaclass=ABCMeta):
    pass


@generate_wrapper(_CompositeMarkup)
class TIETextNode(TextNode, AbstractTIENode, AbstractNodeWrapper[TextNode], metaclass=ABCMeta):
    @property
    def has_language(self) -> bool:
        return self.metadata.language is not None

    @property
    def language(self) -> str:
        if not self.has_language:
            raise AttributeError
        return self.metadata.language

    @validate(AbstractTIENode.with_sentences)
    def _validate_sentences(self, sentences: Sequence[Sentence]) -> dict:
        sentences = SpanContainer(sentences)
        if len(sentences) and sentences[-1].end > len(self.content):
            raise ValueError
        return {"sentences": sentences}

    @validate(AbstractTIENode.with_chains)
    def _validate_chains(self, chains: Iterable[CoreferenceChain]) -> dict:
        chains = tuple(c.for_node(self) for c in chains)
        if any(mention.end > len(self.content) for mention in chain.from_iterable(chains)):
            raise ValueError
        return {"chains": chains}

    @post_process(AbstractTIENode.chains_for)
    @post_process(AbstractTIENode.chains)
    def _transform_chains(self, cchains: Mapping[str, FrozenSet[MentionSpan]]) -> Tuple[CoreferenceChain, ...]:
        return tuple(
            CoreferenceChain((m.mention(self) for m in mentions), id_)
            for id_, mentions in cchains.items()
        )

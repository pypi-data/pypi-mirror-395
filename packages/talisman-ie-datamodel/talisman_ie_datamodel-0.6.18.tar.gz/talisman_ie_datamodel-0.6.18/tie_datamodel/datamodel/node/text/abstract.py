from abc import ABCMeta, abstractmethod
from typing import Iterable, Iterator, Tuple, TypeVar

from tdm.wrapper.node import getter, modifier

from tie_datamodel.datamodel.container import SpanContainer
from tie_datamodel.datamodel.span import Span
from tie_datamodel.datamodel.span.abstract import AbstractSpan
from .chain import CoreferenceChain
from .sentence import Sentence

_AbstractTIENode = TypeVar('_AbstractTIENode', bound='AbstractTIENode')


class AbstractTIENode(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def has_language(self) -> bool:
        pass

    @property
    @abstractmethod
    def language(self) -> str:
        pass

    # segmentation methods

    @property
    @abstractmethod
    def has_sentences(self) -> bool:
        pass

    @property
    @abstractmethod
    def sentences(self) -> SpanContainer[Sentence]:
        pass

    @property
    @abstractmethod
    def tokens(self) -> Iterator[Span]:
        pass

    @modifier
    @abstractmethod
    def with_sentences(self: _AbstractTIENode, sentences: Iterable[Sentence]) -> _AbstractTIENode:
        """
        :param sentences: sentences to be added to the document content
        :return:
        """
        pass

    # coreference chains

    @property
    @abstractmethod
    def has_chains(self) -> bool:
        pass

    @getter
    @abstractmethod
    def chains_for(self, span: AbstractSpan) -> Tuple[CoreferenceChain, ...]:
        pass

    @property
    @abstractmethod
    def chains(self) -> Tuple[CoreferenceChain, ...]:
        pass

    @modifier
    @abstractmethod
    def with_chains(self: _AbstractTIENode, chains: Iterable[CoreferenceChain]) -> _AbstractTIENode:
        """
        :param chains: chains to be set
        :return:
        """
        pass

    @modifier
    @abstractmethod
    def without_chains(self: _AbstractTIENode) -> _AbstractTIENode:
        pass

    @property
    @abstractmethod
    def key_sentence_idx(self) -> int:
        pass

    @property
    @abstractmethod
    def has_key_sentence_idx(self) -> bool:
        pass

    @modifier
    @abstractmethod
    def with_key_sentence_idx(self: _AbstractTIENode, key_sentence_idx: int) -> _AbstractTIENode:
        pass

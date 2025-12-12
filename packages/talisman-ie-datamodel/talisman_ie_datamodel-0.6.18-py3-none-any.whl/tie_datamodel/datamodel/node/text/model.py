from itertools import starmap
from typing import Dict, FrozenSet, Iterable, Mapping, Optional

from tdm.abstract.datamodel.markup.model import AbstractMarkupModel

from .chain.mention import MentionSpan
from .chain.model import CoreferenceChainModel
from .sentence import Sentence
from .sentence.model import SentenceJSONModel


class TIEMarkupModel(AbstractMarkupModel):
    sentences: Optional[tuple[SentenceJSONModel, ...]] = None
    chains: Optional[tuple[CoreferenceChainModel, ...]] = None
    key_sentence_idx: Optional[int] = None

    @classmethod
    def build(
            cls,
            sentences: Optional[Iterable[Sentence]] = None,
            chains: Mapping[str, FrozenSet[MentionSpan]] = None,
            key_sentence_idx: Optional[int] = None
    ) -> 'TIEMarkupModel':
        return cls.model_construct(
            sentences=tuple(map(SentenceJSONModel.build, sentences)) if sentences is not None else None,
            chains=tuple(starmap(CoreferenceChainModel.build, chains.items())) if chains is not None else None,
            key_sentence_idx=key_sentence_idx
        )

    def get_sentences(self) -> Optional[Iterable[Sentence]]:
        if self.sentences is None:
            return None
        return (sentence_model.to_sentence() for sentence_model in self.sentences)

    def get_coref_chains(self) -> Optional[Dict[str, FrozenSet[MentionSpan]]]:
        if self.chains is None:
            return None
        return dict(map(CoreferenceChainModel.to_coref_chain, self.chains))

    def get_key_sentence_idx(self) -> Optional[int]:
        return self.key_sentence_idx

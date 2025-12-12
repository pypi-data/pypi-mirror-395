from typing import FrozenSet, Iterable, Tuple, Union

from pydantic import BaseModel

from .mention import MentionSpan

MentionModel = Union[Tuple[int, int], Tuple[int, int, float]]


class CoreferenceChainModel(BaseModel):
    id: str
    mentions: Tuple[MentionModel, ...]

    def to_coref_chain(self) -> tuple[str, FrozenSet[MentionSpan]]:
        return self.id, frozenset(MentionSpan(*mention) for mention in self.mentions)

    @classmethod
    def build(cls, id_: str, chain: Iterable[MentionSpan]):
        return cls.model_construct(id=id_, mentions=tuple(map(build_mention_model, sorted(chain))))


def build_mention_model(mention: MentionSpan) -> MentionModel:
    if mention.confidence is not None:
        return mention.start, mention.end, mention.confidence
    return mention.start, mention.end

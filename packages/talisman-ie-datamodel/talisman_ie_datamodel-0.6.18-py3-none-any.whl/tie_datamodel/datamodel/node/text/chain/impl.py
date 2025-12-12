from hashlib import md5
from typing import Iterable, Iterator, Optional

from tdm.datamodel.nodes import TextNode
from typing_extensions import Self

from .mention import Mention


class CoreferenceChain(Iterable[Mention]):
    __slots__ = ('_id', '_mentions')

    def __init__(self, mentions: Iterable[Mention], id_: Optional[str] = None):
        self._mentions = tuple(sorted(mentions))
        self._id = id_ if id_ is not None else self._generate_id(self._mentions)

    def __iter__(self) -> Iterator[Mention]:
        return iter(self._mentions)

    def __eq__(self, other):
        if not isinstance(other, CoreferenceChain):
            return NotImplemented
        return self._mentions == other._mentions

    def __hash__(self):
        return hash(self._mentions)

    @property
    def mentions(self) -> tuple[Mention, ...]:
        return self._mentions

    def for_node(self, node_or_id: TextNode | str) -> Self:
        if isinstance(node_or_id, TextNode):
            node_or_id = node_or_id.id
        if not isinstance(node_or_id, str):
            raise TypeError
        return CoreferenceChain(filter(lambda m: m.node_id == node_or_id, self._mentions), id_=self._id)

    @property
    def id(self) -> str:
        return self._id

    @staticmethod
    def _generate_id(mentions: tuple[Mention, ...]) -> str:
        # actually we need some deterministic id generation here to guarantee document equality
        return md5(repr(mentions).encode('utf-8')).hexdigest()

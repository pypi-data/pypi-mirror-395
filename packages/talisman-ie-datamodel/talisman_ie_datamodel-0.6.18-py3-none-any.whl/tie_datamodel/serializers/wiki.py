from typing import TextIO

from tdm import TalismanDocument
from tdm.datamodel.facts import MentionFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.utils import dfs

from tp_interfaces.serializers.abstract import AbstractSerializer, AsyncTextIO


class WikiFormatNERCSerializer(AbstractSerializer):
    """
    Serializes documents with named entity annotations into a custom inline format.

    Each entity is represented as `[text|LABEL]` directly within the document text,
    where `text` is the entity span and `LABEL` is the entity type (e.g., PERSON, ORG, LOC).

    This format is inspired by wiki-style markup but uses a pipe '|' to separate the entity text
    from its label. It is designed for readability and ease of manual editing or review.

    Example:
        Input:  "Barack Obama was born in Honolulu."
        Entities: [(0, 12, "PERSON"), (25, 33, "LOC")]
        Output: "[Barack Obama|PERSON] was born in [Honolulu|LOC]."
    """

    def __init__(self, skip_intersections: bool = True):
        self._skip_intersections = skip_intersections

    def serialize(self, doc: TalismanDocument, stream: TextIO):
        stream.write('\n\n'.join(self._doc_to_str(doc)))

    async def aserialize(self, doc: TalismanDocument, stream: AsyncTextIO):
        await stream.write('\n\n'.join(self._doc_to_str(doc)))

    def _doc_to_str(self, doc: TalismanDocument) -> list[str]:
        result = []
        for node in dfs(doc, type_=TextNode):
            result.append(self._serialize_node(doc, node))
        return result

    def _serialize_node(self, doc: TalismanDocument, node: TextNode) -> str:
        def text_mention_filter(mention: MentionFact) -> bool:
            return isinstance(mention.mention, TextNodeMention)

        def key_extractor(mention: MentionFact) -> tuple[int, int]:
            return mention.mention.start, -mention.mention.end

        text = node.content
        mentions = sorted(doc.related_facts(node, MentionFact, filter_=text_mention_filter), key=key_extractor)

        result = []
        pointer = 0

        for mention in mentions:
            start = mention.mention.start
            end = mention.mention.end
            if start < pointer:
                if self._skip_intersections:
                    continue
                else:
                    raise ValueError
            result.append(text[pointer:start])
            result.append(f"[{text[start:end]}|{mention.value.str_type_id}]")
            pointer = end
        result.append(text[pointer:])

        return ''.join(result)

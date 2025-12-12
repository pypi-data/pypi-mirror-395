from collections import defaultdict
from functools import singledispatch
from pathlib import Path
from typing import AsyncIterator, Iterable

import aiofiles
from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractNode
from tdm.datamodel.facts import MentionFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import KeyNode, TextNode
from tdm.utils import dfs

from tie_datamodel.serializers.jsonl import AbstractJSONLinesSerializer
from tp_interfaces.serializers.abstract import AbstractPathSerializer


class JSONArrayPathSerializer(AbstractPathSerializer):
    def __init__(self, serializer: AbstractJSONLinesSerializer):
        self._serializer = serializer

    def serialize(self, docs: Iterable[TalismanDocument], path: Path):
        first = True
        with path.open("w", encoding="utf-8") as f:
            f.write("[")
            for doc in docs:
                if not first:
                    f.write(',')
                first = False
                f.write('\n')
                self._serializer.serialize(doc, f)
            f.write("\n]")

    async def aserialize(self, docs: AsyncIterator[TalismanDocument], path: Path):
        first = True
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write("[")
            async for doc in docs:
                if not first:
                    await f.write(',')
                first = False
                await f.write('\n')
                await self._serializer.aserialize(doc, f)
            await f.write("\n]")


class LabelStudioSerializer(AbstractJSONLinesSerializer):
    def __init__(
            self,
            predictions: bool = True
    ):
        self._markup_key = "predictions" if predictions else "annotations"

    def _doc_to_dict(self, doc: TalismanDocument) -> dict:
        text = []
        pointer = 0
        nodes_mapping: list[dict] = []
        markup: list[dict] = []

        for node in dfs(doc, doc.main_root):
            node_text, node_annotations = _parse_node(node, doc, pointer)
            text.append(node_text)
            markup.extend(node_annotations)
            nodes_mapping.append({"node": node.id, "span": [pointer, pointer + len(node_text)]})
            pointer += len(node_text)

        return {
            "data": {
                "doc_id": doc.id,
                "text": ''.join(text),
                "annotations": len(markup)
            },
            self._markup_key: [{
                "result": markup
            }],
            "meta": {
                "nodes_mapping": nodes_mapping
            }
        }


@singledispatch
def _parse_node(node: AbstractNode, doc: TalismanDocument, pointer: int) -> tuple[str, list[dict]]:
    return "", []


@_parse_node.register(KeyNode)
def _(node: KeyNode, doc: TalismanDocument, pointer: int) -> tuple[str, list[dict]]:
    return node.content + '\n\n', []


@_parse_node.register(TextNode)
def _(node: TextNode, doc: TalismanDocument, pointer: int) -> tuple[str, list[dict]]:
    text = node.content + '\n\n'
    markup: dict[tuple[int, int], set[str]] = defaultdict(set)
    for fact in doc.related_facts(node, MentionFact):
        mention = fact.mention
        if not isinstance(mention, TextNodeMention):
            continue
        mention: TextNodeMention
        markup[(mention.start + pointer, mention.end + pointer)].add(fact.value.str_type_id)

    return text, [_serialize_mention(span, labels) for span, labels in markup.items()]


def _serialize_mention(span: tuple[int, int], labels: set[str], text: str = None) -> dict:
    result = {
        "value": {
            "start": span[0],
            "end": span[1],
            "labels": list(labels)
        },
        "from_name": "label",
        "to_name": "text",
        "type": "labels"
    }
    if text:
        result["text"] = text
    return result

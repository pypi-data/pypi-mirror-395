import json
from pathlib import Path
from typing import Iterable, Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import FactStatus
from tdm.datamodel.facts import AtomValueFact, MentionFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue

from tp_interfaces.readers.abstract import AbstractReader


class LabelStudioDocumentReader(AbstractReader):
    def __init__(self, path_to_json: Path):
        AbstractReader.__init__(self, path_to_json)

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        with filepath.open('r', encoding='utf-8') as f:
            raw_data = json.load(f)

        for raw_object in raw_data:
            yield self._parse_document(raw_object)

    def _parse_document(self, raw_object: dict) -> TalismanDocument:
        doc_id = raw_object['data'].get('doc_id')
        if doc_id is None:  # `doc_id` field is not required by format, so if it is missed, we use object id
            doc_id = str(raw_object["id"])

        text_node = TextNode(raw_object['data']['text'])

        document = DefaultDocumentFactory.create_document(id_=doc_id)
        document = document.with_main_root(text_node, update=True)
        document = document.with_facts(self._parse_annotations(text_node, raw_object["annotations"]), update=True)
        return document

    def _parse_annotations(self, node: TextNode, all_annotations: list[dict]) -> Iterable[MentionFact]:
        # now we unite all the annotations, but in future there could be different collision resolution strategies
        for annotations in all_annotations:
            if annotations["was_cancelled"]:
                continue
            for annotation in annotations["result"]:
                for label in annotation["value"]["labels"]:
                    yield MentionFact(
                        FactStatus.APPROVED,
                        TextNodeMention(node, annotation["value"]["start"], annotation["value"]["end"]),
                        AtomValueFact(FactStatus.APPROVED, label, StringValue(annotation["value"]["text"]))
                    )

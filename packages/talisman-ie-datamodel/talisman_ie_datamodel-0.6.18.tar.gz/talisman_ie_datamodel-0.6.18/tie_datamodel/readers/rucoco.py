import json
from pathlib import Path
from typing import Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, TIETextNode
from tp_interfaces.readers.abstract import AbstractReader, MultiFilePathConstructor


class RuCoCoDocumentReader(AbstractReader):
    def __init__(self, path_to_dir: Path):
        super().__init__(path_to_dir)

    @property
    def path_constructor(self):
        return MultiFilePathConstructor()

    @staticmethod
    def read_doc(filepath: Path) -> Iterator[TalismanDocument]:
        doc_id = filepath.stem
        node_id = filepath.stem
        with filepath.open("r", encoding="utf-8") as f:
            doc_json = json.load(f)

        raw_text = doc_json['text']

        node = TIETextNode.wrap(TextNode(raw_text, node_id))

        chains = [CoreferenceChain([Mention(node, start, end) for start, end in chain]) for chain in doc_json['entities']]

        yield DefaultDocumentFactory.create_document(id_=doc_id).with_main_root(node.with_chains(chains), update=True)

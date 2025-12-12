import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterator

from tdm import DefaultDocumentFactory
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, TIETextNode
from tp_interfaces.readers.abstract import AbstractPathConstructor, AbstractReader

logger = logging.getLogger(__name__)


class RuevalPathConstructor(AbstractPathConstructor):
    def get_data_paths(self, filepath: Path, **kwargs) -> Iterator[Dict[str, Path]]:
        chains_dir = filepath / "Chains"
        texts_dir = filepath / "Texts"
        for directory in chains_dir, texts_dir:
            if not directory.exists() or not directory.is_dir():
                raise Exception(f"Path {directory} does not contain a {directory.name} directory")
        for text_doc in texts_dir.iterdir():
            if not (chains_dir / text_doc.name).exists():
                logger.warning(f"Cannot find chains annotation for file {text_doc.stem}")
            yield {'filepath': text_doc}


class RuevalReader(AbstractReader):
    """Right now this reader will read only coreference chain content from the RuEval corpus -
    more functionality to be added as necessary"""

    def __init__(self, path_to_rueval: Path):
        super().__init__(path_to_rueval)
        self._path = Path(path_to_rueval)
        if not self._path.is_dir():
            raise Exception("Path is not a directory; please provide a path to the directory containing RuEval")

    @property
    def path_constructor(self) -> AbstractPathConstructor:
        return RuevalPathConstructor()

    def read_doc(self, filepath: Path):
        doc_id = filepath.stem
        raw_text = filepath.read_text(encoding="utf16")
        node = TIETextNode.wrap(TextNode(raw_text, doc_id))

        chains = defaultdict(list)
        chains_dir = self._filepath / "Chains"
        for chain in (chains_dir / filepath.name).read_text().splitlines():
            _, start, length, chain_id = map(int, chain.split())
            chains[chain_id].append(Mention(node, start, start + length))

        yield DefaultDocumentFactory.create_document(id_=doc_id) \
            .with_main_root(node.with_chains(map(CoreferenceChain, chains.values())), update=True)

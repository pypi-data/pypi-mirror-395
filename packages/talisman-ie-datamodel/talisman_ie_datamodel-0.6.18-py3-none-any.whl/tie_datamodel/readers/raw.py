import logging
from pathlib import Path
from typing import Dict, Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tp_interfaces.helpers.io import check_path_existence
from tp_interfaces.readers.abstract import AbstractPathConstructor, AbstractReader

logger = logging.getLogger(__name__)


class RecursivePathConstructor(AbstractPathConstructor):
    def __init__(self, pattern="*"):
        self._pattern = pattern

    def get_data_paths(self, path: Path) -> Iterator[Dict[str, Path]]:
        sorted_paths = iter(sorted(p for p in path.rglob(self._pattern) if p.is_file()))
        for path in sorted_paths:
            yield {'filepath': Path(path)}


def relative_path_name_provider(file_path: Path, original_path: Path):
    return str(file_path.relative_to(original_path))


class RawTextReader(AbstractReader):
    def __init__(self, path: Path, name_provider=relative_path_name_provider):
        super().__init__(path)
        self._name_provider = name_provider

    @property
    def path_constructor(self):
        return RecursivePathConstructor("*.txt")

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        doc_name = self._name_provider(filepath, self._filepath)
        check_path_existence(filepath)
        with filepath.open("r", encoding="utf-8") as f:
            yield DefaultDocumentFactory.create_document(id_=doc_name).with_nodes([TextNode(f.read(), doc_name)])

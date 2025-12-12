import json
import logging
from os import PathLike

from fsspec import AbstractFileSystem
from tdm import TalismanDocument, TalismanDocumentModel

from tp_interfaces.abstract.dataset import AbstractDatasetManager
from .split_tdm_data import SplitTdmData

README_FILE_NAME = "README.md"
DOCUMENTS_FILE_NAME = "documents.jsonl"
logger = logging.getLogger(__name__)


class TdmDatasetManager(AbstractDatasetManager[TalismanDocument]):
    def __init__(self, path: str | PathLike, file_system: AbstractFileSystem | None = None):
        super().__init__(file_system=file_system, path=path)
        self._description_path = self._path / README_FILE_NAME
        self._documents_path = self._path / DOCUMENTS_FILE_NAME

        if self._fs.exists(self._description_path):
            with self._fs.open(self._description_path, "r", encoding="utf-8") as readme_f:
                self._description = readme_f.read()
        else:
            self._description: str = ""

        if self._fs.exists(self._documents_path):
            with self._fs.open(self._documents_path, "r", encoding="utf-8") as documents_f:
                # TODO: deserialize documents only when we want to manipulate them
                documents = [
                    TalismanDocumentModel.model_validate(json.loads(document_line)).deserialize() for document_line in documents_f
                ]
            self._documents = {doc.id: doc for doc in documents}
        else:
            self._documents = {}

    def set_description(self, description: str) -> None:
        self._description = description

    def add(self, element: TalismanDocument) -> None:
        self._documents[element.id] = element

    def remove(self, element: TalismanDocument) -> None:
        self._documents.pop(element.id, None)

    def save(self, version: str | None = None, exist_ok: bool = False) -> None:
        if version is not None:
            logger.warning(f"Version parameter {version} is ignored")

        if self._fs.exists(self._documents_path) and not exist_ok:
            raise ValueError(f"Dataset already exists")
        self._fs.makedirs(self._path, exist_ok=True)

        with self._fs.open(self._description_path, "w", encoding="utf-8") as readme_f:
            readme_f.write(self._description)

        with self._fs.open(self._documents_path, "w", encoding="utf-8") as documents_f:
            for document in self._documents.values():
                document_str = json.dumps(
                    TalismanDocumentModel.serialize(document=document).model_dump(exclude_none=True), sort_keys=True, ensure_ascii=False
                )
                documents_f.write(f"{document_str}\n")

        self.save_extra_data()

    def get_dataset(self) -> SplitTdmData:
        return SplitTdmData({None: self._documents.values()}, extra_data=self._extra_data)

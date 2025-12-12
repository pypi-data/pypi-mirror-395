import logging
import os
from pathlib import Path
from typing import AsyncIterator, Iterable, Protocol

import aiofiles
from tdm import TalismanDocument

from tp_interfaces.helpers.io import check_path_absense
from tp_interfaces.serializers.abstract import AbstractPathSerializer, AbstractSerializer

logger = logging.getLogger(__name__)


class FileNameGenerator(Protocol):
    def __call__(self, document: TalismanDocument) -> str:
        ...


class CountNameGenerator(FileNameGenerator):
    def __init__(self, template: str, *, start: int = 0):
        self._template = template
        self._index = start

    def __call__(self, document: TalismanDocument) -> str:
        try:
            return self._template.format(self._index)
        finally:
            self._index += 1


class DirectoryPathSerializer(AbstractPathSerializer):
    def __init__(self, serializer: AbstractSerializer, filename_generator: FileNameGenerator):
        self._serializer = serializer
        self._filename_generator = filename_generator

    def serialize(self, docs: Iterable[TalismanDocument], path: Path):
        check_path_absense(path)

        path.mkdir(parents=True, exist_ok=True)
        for doc in docs:
            file = path / self._filename_generator(doc)
            try:
                with file.open('w', encoding='utf-8') as f:
                    self._serializer.serialize(doc, f)
            except Exception as e:
                logger.error(f"Exception while document {doc.id} serialization", exc_info=e)
                os.remove(file)

    async def aserialize(self, docs: AsyncIterator[TalismanDocument], path: Path):
        check_path_absense(path)
        path.mkdir(parents=True, exist_ok=True)

        async for doc in docs:
            file = path / self._filename_generator(doc)
            try:
                async with aiofiles.open(file, "w", encoding="utf-8") as f:
                    await self._serializer.aserialize(doc, f)
            except Exception as e:
                logger.error(f"Exception while document {doc.id} serialization", exc_info=e)
                os.remove(file)

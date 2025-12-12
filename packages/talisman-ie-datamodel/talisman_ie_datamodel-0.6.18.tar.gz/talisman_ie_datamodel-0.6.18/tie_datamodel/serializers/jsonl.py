import json
from abc import abstractmethod
from pathlib import Path
from typing import AsyncIterator, Iterable, TextIO

import aiofiles
from tdm import TalismanDocument, TalismanDocumentModel

from tp_interfaces.helpers.io import check_path_absense
from tp_interfaces.serializers.abstract import AbstractPathSerializer, AbstractSerializer, AsyncTextIO


class LineByLinePathSerializer(AbstractPathSerializer):
    def __init__(self, serializer: AbstractSerializer):
        self._serializer = serializer

    def serialize(self, docs: Iterable[TalismanDocument], path: Path, *, rewrite: bool = False):
        if not rewrite:
            check_path_absense(path)

        with path.open("w", encoding="utf-8") as f:
            for doc in docs:
                self._serializer.serialize(doc, f)
                f.write("\n")

    async def aserialize(self, docs: AsyncIterator[TalismanDocument], path: Path, *, rewrite: bool = False):
        if not rewrite:
            check_path_absense(path)

        path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            async for doc in docs:
                await self._serializer.aserialize(doc, f)
                await f.write("\n")


class AbstractJSONLinesSerializer(AbstractSerializer):

    def serialize(self, doc: TalismanDocument, stream: TextIO):
        self._check_stream(stream)
        line = json.dumps(self._doc_to_dict(doc), sort_keys=True, ensure_ascii=False)
        stream.write(line)

    async def aserialize(self, doc: TalismanDocument, stream: AsyncTextIO):
        await self._a_check_stream(stream)
        line = json.dumps(self._doc_to_dict(doc), sort_keys=True, ensure_ascii=False)
        await stream.write(line)

    @abstractmethod
    def _doc_to_dict(self, doc: TalismanDocument) -> dict:
        pass


class TDMSerializer(AbstractJSONLinesSerializer):

    def _doc_to_dict(self, doc: TalismanDocument) -> dict:
        model: TalismanDocumentModel = TalismanDocumentModel.serialize(doc)
        return model.model_dump(exclude_none=True)

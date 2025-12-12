from tdm import TalismanDocument, TalismanDocumentModel

from .abstract import AbstractJSONLinesReader


class TDMReader(AbstractJSONLinesReader):
    def _convert_to_doc(self, json_dict: dict) -> TalismanDocument:
        return TalismanDocumentModel.model_validate(json_dict).deserialize()

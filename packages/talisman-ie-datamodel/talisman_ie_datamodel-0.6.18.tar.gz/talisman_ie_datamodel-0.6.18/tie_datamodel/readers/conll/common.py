from pathlib import Path
from typing import Iterator, List

from .abstract import AbstractCoNLLFileParser, BaseCoNLLReader


class CoNLLFileParser(AbstractCoNLLFileParser):

    def __init__(self, delimiter):
        self._delimiter = delimiter

    def read_docs(self, f) -> Iterator[List[List[str]]]:
        doc_raw_tokens = []
        for line in f:
            spl = line.split()
            if spl and spl[0].startswith(self._delimiter):
                if doc_raw_tokens:
                    yield doc_raw_tokens
                doc_raw_tokens = []
                continue
            doc_raw_tokens.append(spl)
        if doc_raw_tokens:
            yield doc_raw_tokens

    @staticmethod
    def conll_parser():
        return CoNLLFileParser('-DOCSTART-')

    @staticmethod
    def bionlp_parser():
        return CoNLLFileParser('###MEDLINE:')


class CoNLLReader(BaseCoNLLReader):
    def __init__(self, filepath: Path):
        super().__init__(filepath, CoNLLFileParser.conll_parser())


class BioNLPReader(BaseCoNLLReader):
    def __init__(self, filepath: Path):
        super().__init__(filepath, CoNLLFileParser.bionlp_parser())

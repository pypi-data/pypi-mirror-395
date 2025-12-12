__all__ = [
    'AbstractJSONLinesReader', 'DoccanoReader', 'TDMReader',
    'RawTextReader',
    'readers',
    'TACREDDocumentReader',
    'BratReader',
    'RuevalReader',
    'DocREDReader',
    'RuCoCoDocumentReader',
    'DirectoryReader',
]

from .brat import BratReader
from .directory import DirectoryReader
from .docred import DocREDReader
from .jsonl import AbstractJSONLinesReader, DoccanoReader, TDMReader
from .raw import RawTextReader
from .readers import readers
from .rucoco import RuCoCoDocumentReader
from .rueval import RuevalReader
from .tacred import TACREDDocumentReader

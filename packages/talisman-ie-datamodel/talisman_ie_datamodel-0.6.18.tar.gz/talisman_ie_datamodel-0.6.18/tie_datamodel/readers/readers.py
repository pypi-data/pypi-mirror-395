from tp_interfaces.readers.abstract import MultiFilePathConstructor, replace_path_constructor
from .brat import BratReader
from .conll.common import BioNLPReader, CoNLLReader
from .conll.ontonotes import OntonotesReader
from .docred import DocREDReader
from .jsonl import DoccanoReader, TDMReader
from .jsonl.wlcoref import WlcorefJSONLinesReader
from .labelstudio import LabelStudioDocumentReader
from .raw import RawTextReader
from .rucoco import RuCoCoDocumentReader
from .rueval import RuevalReader
from .tacred import TACREDDocumentReader

readers = {
    'docred': DocREDReader,
    'doccano': DoccanoReader,
    'plain': RawTextReader,
    'conll': CoNLLReader,
    'bionlp': BioNLPReader,
    'ontonotes': OntonotesReader,
    'tacred': TACREDDocumentReader,
    'default': TDMReader,
    'tdm-directory': replace_path_constructor(TDMReader, MultiFilePathConstructor()),
    'brat': BratReader,
    'wlcoref': WlcorefJSONLinesReader,
    'rueval': RuevalReader,
    'rucoco': RuCoCoDocumentReader,
    'label-studio': LabelStudioDocumentReader
}

configurable_readers = {
    'default': TDMReader.from_config,
    'wlcoref': WlcorefJSONLinesReader.from_config,
    'docred': DocREDReader.from_config
}

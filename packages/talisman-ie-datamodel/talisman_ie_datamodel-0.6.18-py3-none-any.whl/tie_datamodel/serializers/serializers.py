from .directory import CountNameGenerator, DirectoryPathSerializer
from .jsonl import LineByLinePathSerializer, TDMSerializer
from .label_studio import JSONArrayPathSerializer, LabelStudioSerializer
from .wiki import WikiFormatNERCSerializer

serializers = {
    'default': lambda: LineByLinePathSerializer(TDMSerializer()),
    'wiki': lambda: DirectoryPathSerializer(WikiFormatNERCSerializer(), filename_generator=CountNameGenerator("doc-{}.txt")),
    'label_studio': lambda: JSONArrayPathSerializer(LabelStudioSerializer())
}

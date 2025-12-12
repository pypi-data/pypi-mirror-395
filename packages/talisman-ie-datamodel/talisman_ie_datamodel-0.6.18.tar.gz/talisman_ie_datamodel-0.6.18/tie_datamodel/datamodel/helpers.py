from typing import Iterable, Mapping

from tdm import TalismanDocument
from tdm.datamodel.nodes import TextNode
from tdm.utils import dfs

from tie_datamodel.datamodel.node.text import Sentence, TIETextNode
from tie_datamodel.datamodel.span import Span

_SEPARATOR = "\n"


def document_nodes_data_merge(document: TalismanDocument) -> tuple[tuple[TIETextNode, ...], str, tuple[Span, ...], tuple[Sentence, ...]]:
    """
    Join text of all document nodes, shift borders of tokens and sentences according to their location in the merged text.
    return:
        - document nodes
        - merged text
        - tokens spans with shifted borders
        - sentences with shifted borders
    """
    text_nodes: tuple[TIETextNode, ...] = tuple(dfs(document, document.main_root, TIETextNode))
    texts = []
    concat_tokens: list[Span] = []
    concat_sentences: list[Sentence] = []
    pointer = 0
    for node in text_nodes:
        node: TIETextNode
        texts.append(node.content)
        for sentence in node.sentences:
            sentence = sentence.shift(pointer)
            concat_sentences.append(sentence)
            concat_tokens.extend(sentence)
        pointer += len(texts[-1]) + len(_SEPARATOR)
    return text_nodes, _SEPARATOR.join(texts), tuple(concat_tokens), tuple(concat_sentences)


def get_node_id2shift(content_nodes: Iterable[TextNode]) -> Mapping[str, int]:
    """
    Get mapping node_id -> text_shift for node text pointer in the merged text.
    """
    shift = 0
    d = {}
    for node in content_nodes:
        d[node.id] = shift
        shift += len(node.content) + 1
    return dict(sorted(d.items(), key=lambda item: item[1]))

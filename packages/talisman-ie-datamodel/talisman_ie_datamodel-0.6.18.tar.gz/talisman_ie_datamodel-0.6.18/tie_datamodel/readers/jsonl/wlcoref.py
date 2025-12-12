from typing import Optional, Tuple

from pydantic import ConfigDict
from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, Sentence, SentenceWithSyntax, TIETextNode
from tie_datamodel.datamodel.span import Span
from tie_datamodel.readers import AbstractJSONLinesReader
from tp_interfaces.abstract import ImmutableBaseModel


class WlcorefFormat(ImmutableBaseModel):
    document_id: str
    cased_words: Tuple[str, ...]
    sent_id: Tuple[int, ...]
    head: Tuple[Optional[int], ...]
    deprel: Tuple[str, ...]
    span_clusters: Tuple[Tuple[Tuple[int, int], ...], ...]
    model_config = ConfigDict(extra="ignore")


class WlcorefJSONLinesReader(AbstractJSONLinesReader):
    def _convert_to_doc(self, json_dict: dict) -> TalismanDocument:
        coref_line: WlcorefFormat = WlcorefFormat.model_validate(json_dict)

        all_spans: list[Span] = []
        sentences: list[SentenceWithSyntax] = []
        spans: list[Span] = []
        tree: list[Optional[tuple[str, int]]] = []
        raw_text: str = ''
        head_offset = 0
        for word, sent_id, head, rel in zip(coref_line.cased_words, coref_line.sent_id, coref_line.head, coref_line.deprel):
            if sent_id > len(sentences):
                sentences.append(SentenceWithSyntax.from_sentence(Sentence(Span(spans[0].start, spans[-1].end), spans), tuple(tree)))
                all_spans.extend(spans)
                head_offset += len(spans)
                spans, tree = [], []
            spans.append(Span(len(raw_text), len(raw_text) + len(word)))
            tree.append(None if head is None else (rel, head - head_offset))
            raw_text += word + ' '

        if spans:
            sentences.append(SentenceWithSyntax.from_sentence(Sentence(Span(spans[0].start, spans[-1].end), spans), tuple(tree)))
            all_spans.extend(spans)

        node = TIETextNode.wrap(TextNode(raw_text, coref_line.document_id)).with_sentences(sentences)

        chains: list[CoreferenceChain] = []
        for cluster in coref_line.span_clusters:
            chains.append(
                CoreferenceChain([
                    Mention(node, all_spans[start].start, all_spans[end - 1].end) for start, end in cluster
                ])
            )

        node = node.with_chains(chains)

        return DefaultDocumentFactory.create_document(id_=coref_line.document_id).with_main_root(node, update=True)

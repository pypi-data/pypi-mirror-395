from pathlib import Path
from typing import Callable, Iterator, List

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.facts import AtomValueFact, MentionFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue

from tie_datamodel.datamodel.node.text import TIETextNode
from tie_datamodel.datamodel.node.text.sentence import Sentence
from tie_datamodel.datamodel.span import Span
from tp_interfaces.readers.abstract import AbstractReader


class AbstractCoNLLFileParser(object):
    def read_docs(self, f) -> Iterator[List[List[str]]]:
        pass


class BaseCoNLLReader(AbstractReader):
    def __init__(self, filepath: Path, file_parser: AbstractCoNLLFileParser):
        super().__init__(filepath)
        self._file_parser = file_parser

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        with filepath.open(encoding="utf-8", mode='r') as f:
            for doc_idx, doc_raw_tokens in enumerate(self._file_parser.read_docs(f)):
                yield _create_doc(doc_raw_tokens, f"{self._filepath.name}-{doc_idx}")


def _create_doc(doc_raw_tokens: List[List[str]], node_id: str) -> TalismanDocument:
    tokens, sentences, fact_factories = [], [], []
    token_start = 0
    sent_tokens, sent_entities_labels, spans = [], [], []
    raw_text = ''

    for raw_token in doc_raw_tokens:
        if not raw_token:
            if sent_tokens:
                sentences.append(Sentence(Span(spans[0].start, spans[-1].end), spans))
                fact_factories.extend(_decode(sentences[-1], sent_entities_labels))
                sent_tokens, sent_entities_labels, spans = [], [], []
            continue

        token = raw_token[0]
        ent_label = raw_token[-1]
        spans.append(Span(token_start, token_start + len(token)))
        sent_tokens.append(token)
        sent_entities_labels.append(ent_label)
        raw_text += ' ' + token
        token_start += len(token) + 1

    if sent_tokens:
        tokens.extend(sent_tokens)
        sentences.append(Sentence(Span(spans[0].start, spans[-1].end), spans))
        fact_factories.extend(_decode(sentences[-1], sent_entities_labels))

    node = TIETextNode.wrap(TextNode(raw_text[1:], node_id)).with_sentences(sentences)

    return DefaultDocumentFactory.create_document(id_=node_id) \
        .with_main_root(node, update=True) \
        .with_facts((f(node) for f in fact_factories), update=True)


def _decode(sentence: Sentence, sent_entities_labels: List[str]) -> Iterator[Callable[[TextNode], AbstractFact]]:
    prev_mark = 'O'
    prev_ent = ''
    ent_start = sentence.start
    ent = ['O']  # not to reference before assignment
    for token, entity in zip(sentence, sent_entities_labels):
        ent = entity.split('-')
        if ent[0] == 'O' and prev_mark != 'O':
            yield _fact_factory(ent_start, token.start - 1, prev_ent)
        elif prev_mark == 'O' and ent[0] != 'O':
            ent_start = token.start
        elif (prev_mark != 'O' and ent[0] == 'B') or (prev_mark != 'O' and ent[0] == 'I' and prev_ent != ent[1]):
            yield _fact_factory(ent_start, token.start - 1, prev_ent)
            ent_start = token.start
        prev_mark = ent[0]
        prev_ent = ent[-1]
    if ent[0] != 'O':
        yield _fact_factory(ent_start, sentence.end, prev_ent)


def _fact_factory(start: int, end: int, label: str) -> Callable[[TextNode], AbstractFact]:
    def create_fact(node: TextNode) -> AbstractFact:
        return MentionFact(
            FactStatus.APPROVED,
            TextNodeMention(node, start, end),
            AtomValueFact(FactStatus.APPROVED, label, StringValue(node.content[start:end]))
        )

    return create_fact

import json
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator, List, Tuple

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.facts import ConceptFact, RelationFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue
from tdm.utils import mentioned_fact_factory

from tie_datamodel.datamodel.node.text import TIETextNode
from tie_datamodel.datamodel.node.text.sentence import Sentence
from tie_datamodel.datamodel.span import Span
from tp_interfaces.domain.model.types import AtomValueType, ConceptType, IdentifyingPropertyType
from tp_interfaces.readers.abstract import AbstractReader


class TACREDDocumentReader(AbstractReader):
    NO_RELATION_TYPE = 'no_relation'
    _special_tokens_mapping = {
        '-LRB-': '(',
        '-RRB-': ')',
        '-LSB-': '[',
        '-RSB-': ']',
        '-LCB-': '{',
        '-RCB-': '}'
    }

    def __init__(self, path_to_json: Path):
        super().__init__(path_to_json)

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        with filepath.open("r", encoding="utf-8") as f:
            raw_documents = json.load(f)

        tokens2raw_docs = defaultdict(list)
        for raw_doc in raw_documents:
            tokens = tuple(raw_doc['token'])
            tokens2raw_docs[tokens].append(raw_doc)

        return map(self._convert_to_doc, tokens2raw_docs.values())

    def _convert_to_doc(self, raw_docs: List[dict]) -> TalismanDocument:
        """
        Each document is one sentence with 2 entities and relation between them.
        All documents in raw_docs has same tokens and sentences but different entities and relations
        """
        example_ids = sorted(d['id'] for d in raw_docs)
        doc_id = ', '.join(example_ids)
        node_id = example_ids[0]  # not to duplicate long strs

        tokens = {tuple(d['token']) for d in raw_docs}
        if len(tokens) != 1:
            raise ValueError

        tokens_strs, = tokens
        raw_text, sentence = self._convert_tokens(tokens_strs)
        node = TIETextNode.wrap(TextNode(raw_text, node_id)).with_sentences([sentence])

        facts = []
        cache: dict[TextNodeMention, ConceptFact] = {}
        for d in raw_docs:
            # subj and obj end are indices of last included token of entity, fix them on 1 to become non-included
            source, other = self._create_facts(node, d['subj_start'], d['subj_end'], d['subj_type'], cache)
            facts.extend(other)

            target, other = self._create_facts(node, d['obj_start'], d['obj_end'], d['obj_type'], cache)
            facts.extend(other)
            relation_type = d['relation']
            if relation_type == self.NO_RELATION_TYPE:
                continue
            facts.append(
                RelationFact(FactStatus.APPROVED, relation_type, source, target)
            )

        return DefaultDocumentFactory.create_document(id_=doc_id).with_main_root(node, update=True).with_facts(facts, update=True)

    def _convert_tokens(self, tokens_strs: List[str]) -> Tuple[str, Sentence]:
        tokens_strs = [self._special_tokens_mapping.get(tok, tok) for tok in tokens_strs]
        raw_text = ' '.join(tokens_strs)

        token_spans = []
        cur_offset = 0
        for token in tokens_strs:
            span_start = cur_offset
            span_end = span_start + len(token)
            token_spans.append(Span(span_start, span_end))
            cur_offset = span_end + 1  # tokens are separated with space

        return raw_text, Sentence(Span(0, len(raw_text)), token_spans)

    @staticmethod
    def _create_facts(
            node: TIETextNode, start_token: int, end_token: int, label: str, cache: dict[TextNodeMention, ConceptFact]
    ) -> tuple[AbstractFact, Iterable[AbstractFact]]:

        mention = TextNodeMention(node, node.sentences[0][start_token].start, node.sentences[0][end_token].end)
        if mention in cache:
            return cache[mention], ()

        prop_type = IdentifyingPropertyType(
            "Название",
            ConceptType(label, id=f"{label}_cpt"),
            AtomValueType(label, StringValue, id=label),
            id=str(uuid.uuid5(uuid.NAMESPACE_DNS, label + node.id))
        )
        value = StringValue(node.content[mention.start:mention.end])
        cpt, _, prop, ment = mentioned_fact_factory(prop_type)(mention, FactStatus.APPROVED, value)
        cache[ment.mention] = cpt
        return cpt, [ment, prop]

import json
from copy import deepcopy
from itertools import chain
from os import PathLike
from pathlib import Path
from typing import Iterable, Iterator, Optional

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.facts import AtomValueFact, ConceptFact, MentionFact, PropertyFact, RelationFact
from tdm.datamodel.facts.concept import KBConceptValue as ConceptValue
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, Sentence, TIETextNode
from tie_datamodel.datamodel.span import Span
from tp_interfaces.helpers.io import check_path_existence
from tp_interfaces.readers.abstract import AbstractConfigurableReader

"""
DocRED is a dataset constructed from Wikipedia and Wikidata with the 2 key features:
(1) DocRED annotates both named entities and relations, and is the largest human-annotated dataset for document-level RE from plain text;
(2) DocRED requires reading multiple sentences in a document to extract entities and infer their relations by synthesizing all information
of the document.

For more details please refer to the official sources:
* [DocRED on arXiv](https://arxiv.org/abs/1906.06127v3)
* [DocRED on GitHub](https://github.com/thunlp/DocRED)
* [DocRED on paperwithcode.com](https://paperswithcode.com/dataset/docred)

or check our etc/datasets/relext/docred/README.md


There are 6 entity types and 96 kinds of relations. It is important to note that in the original dataset relation Wididata ID's
(not the relation names!) are used as the relation types. It's inconvenient for us, so we use official rel_info.json file for matching
Wikidata ID's to relation names and treat the latter as the relation types. It should also be noted that we consider any single entity as a
concept fact and its mentions as a corresponding mention facts.


DocRED example is a dictionary that has the following structure:

* title: str                                Title of the example document
* sents: List[List[str]]                    List of sentences (that are lists of words)
* vertexSet: List[List[Dict]]               List of entities, each of which consists of several mentions

    Each mention is a dictionary with the following fields:

    * name: str                             Mention words from the text
    * pos: Tuple[int, int]                  Mention words' positions in the sentence (from pos[0] to pos[1] not inclusive)
    * sent_id: int                          Sentence ID in which mention is located
    * type: str                             Entity type

* labels: List[dict]                        List of relations (test file does not have labels)

    Each relation is a dictionary with the following fields:

    * r: str                                Type of relation
    * h: int                                Head (source) entity index in vertexSet
    * t: int                                Tail (target) entity index in vertexSet
    * evidence: List[int]                   ???
"""

DEFAULT_PATH_TO_REL_INFO = Path('etc/datasets/relext/docred/DocRED/rel_info.json')


class DocREDReader(AbstractConfigurableReader):

    def __init__(
            self,
            path_to_file: PathLike,
            delete_duplicate_facts: bool = True,
            path_to_rel_info: PathLike = DEFAULT_PATH_TO_REL_INFO):
        """
        :param path_to_file: path to dataset file
        :param delete_duplicate_facts: should to delete duplicate ner facts
        :param path_to_rel_info: path to rel_info.json file for matching relation Wikidata ID's to relation names
        """
        super().__init__(Path(path_to_file))
        path_to_rel_info = Path(path_to_rel_info)
        self._delete_duplicate_facts = delete_duplicate_facts

        self._rel_info = {}
        if path_to_rel_info and path_to_rel_info.exists():
            with path_to_rel_info.open('r') as file:
                self._rel_info = json.load(file)

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        check_path_existence(filepath)
        with filepath.open('r', encoding='utf-8') as file:
            examples = json.load(file)

        return map(self._convert_to_doc, examples)

    def _convert_to_doc(self, example: dict) -> TalismanDocument:
        node = self._build_node(example)

        facts, chains = self._build_entities(node, example)

        doc = DefaultDocumentFactory.create_document(id_=example['title']) \
            .with_main_root(node, update=True) \
            .with_facts(facts, update=True).with_nodes([node.with_chains(chains)])

        return doc.with_facts(self._build_links(doc, example))

    @staticmethod
    def _build_node(example: dict) -> TIETextNode:
        sentences: list[Sentence] = []
        start_idx = 0
        for sent in example['sents']:
            tokens: list[Span] = []
            for word in sent:
                tokens.append(Span(start_idx, start_idx + len(word)))
                start_idx += len(word) + 1
            sentences.append(Sentence(Span(tokens[0].start, tokens[-1].end), tokens))
        raw_text = ' '.join(chain.from_iterable(example['sents']))

        return TIETextNode.wrap(TextNode(raw_text, example['title'])).with_sentences(sentences)

    @staticmethod
    def _build_entities(node: TIETextNode, example: dict) -> tuple[list[AbstractFact], list[CoreferenceChain]]:

        def build_concept_fact(id_: str, entity: dict) -> ConceptFact:
            return ConceptFact(FactStatus.APPROVED, entity['type'], ConceptValue(entity['name']), id=id_)

        def build_atom_value_fact(entity: dict) -> AtomValueFact:
            return AtomValueFact(FactStatus.APPROVED, 'mention', StringValue(entity['name']))

        def build_mention_fact(entity: dict, value: AtomValueFact) -> MentionFact:
            sentence = node.sentences[entity['sent_id']]
            return MentionFact(
                FactStatus.APPROVED, TextNodeMention(node, sentence[entity['pos'][0]].start, sentence[entity['pos'][1] - 1].end), value
            )

        def build_property_facts(concept: ConceptFact, value: AtomValueFact) -> PropertyFact:
            return PropertyFact(FactStatus.APPROVED, '', concept, value)

        def build_chain(mentions: Iterable[MentionFact]) -> CoreferenceChain:
            return CoreferenceChain(Mention(**f.mention.__dict__) for f in mentions)

        def build_entities_facts(id_: str, entity_cluster: list[dict]) -> tuple[list[AbstractFact], Optional[CoreferenceChain]]:
            concept = build_concept_fact(id_, entity_cluster[0])
            value = build_atom_value_fact(entity_cluster[0])
            facts = [build_mention_fact(entity, value) for entity in entity_cluster]
            chain = build_chain(facts) if len(facts) > 1 else None
            result = [concept, value, build_property_facts(concept, value), *facts]

            return result, chain

        facts = []
        chains = []
        for ind, entity_cluster in enumerate(example['vertexSet']):
            cluster_facts, cluster_chain = build_entities_facts(f'{ind}', entity_cluster)
            facts.extend(cluster_facts)
            if cluster_chain is not None:
                chains.append(cluster_chain)

        return facts, chains

    def _build_links(self, doc: TalismanDocument, example: dict) -> Iterator[RelationFact]:
        """
        NOTE: Relations can be between different sets of source and target entity types. To meet requirements of domain we construct
        unique relation type ids for them.
        """
        for rel in example.get('labels', ()):
            try:
                source = next(doc.get_facts(ConceptFact, filter_=[AbstractFact.id_filter(str(rel['h']))]))
                target = next(doc.get_facts(ConceptFact, filter_=[AbstractFact.id_filter(str(rel['t']))]))
            except StopIteration:
                break
            yield RelationFact(
                status=FactStatus.APPROVED,
                type_id=self._rel_info.get(rel['r'], rel['r']),
                source=source,
                target=target
            )

    @classmethod
    def from_config(cls, config: dict) -> 'DocREDReader':
        config = deepcopy(config)
        path_to_file = Path(config.pop('path_to_file'))
        path_to_rel_info = Path(config.pop('path_to_rel_info')) if 'path_to_rel_info' in config else None
        return cls(path_to_file=path_to_file, path_to_rel_info=path_to_rel_info, **config)

import logging
from pathlib import Path
from typing import Dict, Iterable, Iterator, TextIO

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import FactStatus
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue
from tdm.utils import mentioned_fact_factory

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, TIETextNode
from tp_interfaces.domain.model.types import AtomValueType
from tp_interfaces.helpers.io import check_path_existence
from tp_interfaces.readers.abstract import AbstractPathConstructor, AbstractReader

logger = logging.getLogger(__name__)


class BratPathConstructor(AbstractPathConstructor):
    def get_data_paths(self, filepath: Path) -> Iterator[Dict[str, Path]]:
        check_path_existence(filepath)
        for path_txt in filepath.glob("*.txt"):
            path_ann = Path(filepath, path_txt.stem + '.ann')
            if path_ann.is_file():
                yield {'path_txt': path_txt, 'path_ann': path_ann}
            else:
                logger.warning(f"skip file '{path_txt.stem}'. '{path_ann.stem}' not found.")


class BratReader(AbstractReader):
    def __init__(self, filepath: Path):
        super(BratReader, self).__init__(filepath)

    @property
    def path_constructor(self):
        return BratPathConstructor()

    @staticmethod
    def read_doc(path_txt: Path, path_ann: Path) -> Iterator[TalismanDocument]:
        node_id = path_txt.stem
        with path_txt.open("r", encoding="utf-8") as f:
            raw_text = f.read()

        node = TextNode(raw_text, node_id)

        with path_ann.open("r", encoding="utf-8") as f:
            entities, relations, mention_chains = parse_ann(f)

        chains = []
        for mention_chain in mention_chains:
            chains.append(
                CoreferenceChain(
                    (Mention(node, *entities[mention]['span']) for mention in mention_chain)
                )
            )

        if chains:
            node = TIETextNode.wrap(node).with_chains(chains)

        document = DefaultDocumentFactory.create_document(id_=node_id).with_main_root(node, update=True)

        entity_facts = dict()
        facts = []

        for id_t, item in entities.items():
            start, end = item['span']
            _, fact = mentioned_fact_factory(AtomValueType(item['type'], StringValue, id=item['type']))(
                TextNodeMention(node, start, end), FactStatus.APPROVED, StringValue(node.content[start:end])
            )

            facts.append(fact)
            entity_facts[id_t] = fact

        document = document.with_facts(facts, update=True)

        if relations:
            logger.warning(f"BratReader doesn't support relations now")

        # relation_facts = []
        # for id_t, item in relations.items():
        #     if item['subj'] in entity_facts and item['obj'] in entity_facts:
        #         relation_facts.append(RelationFact(
        #             id_=id_t, status=FactStatus.APPROVED, type_id=item['type'],
        #             value=RelationLinkValue(None, entity_facts[item['subj']], entity_facts[item['obj']])
        #         ))
        #     else:
        #         logger.warning(f"skip relation {id_t} in {path_ann.stem}. Arg not found.")

        yield document


def parse_ann(iter_str: TextIO) -> (Dict[str, Dict], Dict[str, Dict], Iterable[Iterable[Dict]]):
    entities = dict()
    relations = dict()
    entity_chains = []
    for line in iter_str:
        if line.startswith('T'):
            tag_id, tag_spans, text = line.split('\t')

            tag = tag_spans.split(" ")[0].strip()
            span = tag_spans[len(tag):].split(";")
            if len(span) > 1:
                logger.warning("Talisman Document doesn't support multispan facts")
                continue
            entities[tag_id] = {'type': tag, 'span': tuple(map(int, span[0].split()))}
        elif line.startswith('R'):
            tag_id, tag, subj, obj = line.split()[:4]
            subj = subj.replace("Arg1:", "")
            obj = obj.replace("Arg2:", "")
            relations[tag_id] = {'type': tag, 'subj': subj, 'obj': obj}
        elif line.startswith('*'):
            _, data = line.split('\t', 1)
            if data.startswith('Coref'):
                entity_chains.append(data[len('Coref'):].split())

    return entities, relations, entity_chains

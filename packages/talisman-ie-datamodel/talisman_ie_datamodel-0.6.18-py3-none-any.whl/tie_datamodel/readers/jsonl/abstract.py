import json
import logging
from abc import abstractmethod
from multiprocessing.pool import ApplyResult, Pool
from os import PathLike
from pathlib import Path
from random import Random
from typing import Dict, Iterable, Iterator

from tdm import TalismanDocument
from tdm.datamodel.common._view import generate_dataclass_view
from tdm.datamodel.mentions import NodeMention, TextNodeMention

from tie_datamodel.env import get_max_spawned_processes
from tp_interfaces.readers.abstract import AbstractConfigurableReader

try:
    from talisman_tools.helper.concurrency import check_on_jobs
except ImportError:
    setup_multiprocessing = lambda: None
    check_on_jobs = None

logger = logging.getLogger(__name__)


class AbstractJSONLinesReader(AbstractConfigurableReader):
    def __init__(self, filepath: PathLike, *, ratio: float = 1.0, seed: int = 42, shuffle: bool = False):
        super(AbstractJSONLinesReader, self).__init__(filepath)
        self._ratio = ratio
        self._seed = seed
        self._shuffle = shuffle

    @classmethod
    def from_config(cls, config: dict) -> 'AbstractJSONLinesReader':
        return cls(**config)

    def read_doc(self, filepath: Path) -> Iterator[TalismanDocument]:
        with filepath.open('r', encoding='utf-8') as f:
            lines = f.readlines()

        if self._shuffle:
            Random(self._seed).shuffle(lines)

        subset_len = int(len(lines) * self._ratio)
        lines = lines[:subset_len]

        yield from self._parse_contents(lines, n_jobs=get_max_spawned_processes())

    def _parse_contents(self, lines: Iterable[str], *, n_jobs: int = 1) -> Iterable[TalismanDocument]:
        if n_jobs <= 1:
            yield from map(self._process_line, lines)
            return

        # for fixing deserialization of document instance when process from pool exits
        generate_dataclass_view(TextNodeMention)
        generate_dataclass_view(NodeMention)

        decoding_jobs: Dict[int, ApplyResult[TalismanDocument]] = {}
        decoded_docs: Dict[int, TalismanDocument] = {}
        with Pool(n_jobs) as pool:
            for doc_id, line in enumerate(lines):
                decoding_jobs[doc_id] = pool.apply_async(self._process_line, args=(line,))

            last_processed_doc_id = 0
            while len(decoding_jobs):
                decoded_docs.update(check_on_jobs(decoding_jobs, ignore_max_treated_jobs=True))
                while last_processed_doc_id in decoded_docs:
                    yield decoded_docs.pop(last_processed_doc_id)
                    last_processed_doc_id += 1

    def _process_line(self, line: str) -> TalismanDocument:
        return self._convert_to_doc(json.loads(line))

    @abstractmethod
    def _convert_to_doc(self, json_dict: dict) -> TalismanDocument:
        pass

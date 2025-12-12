from pathlib import Path
from typing import Callable

from tp_interfaces.readers.abstract import AbstractReader, MultiFilePathConstructor


class DirectoryReader(AbstractReader):
    def __init__(self, base_reader: Callable[[Path], AbstractReader], path_to_dir: Path):
        super().__init__(path_to_dir)
        self._base_reader = base_reader

    @property
    def path_constructor(self):
        return MultiFilePathConstructor()

    def read_doc(self, filepath: Path):
        yield from self._base_reader(filepath).read()

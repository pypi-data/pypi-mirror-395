from typing import Iterable

from tdm import TalismanDocument

from tp_interfaces.abstract.dataset import AbstractSplitData
from tp_interfaces.serializable import SerializableFS


class SplitTdmData(AbstractSplitData[TalismanDocument]):
    """
    Split dataset implementation.

    None key is for dataset without splits (all data).
    """
    def __init__(self, data: dict[str | None, Iterable[TalismanDocument]], extra_data: dict[str, SerializableFS] | None = None):
        self._role2docs = data
        self._extra_data = {} if extra_data is None else extra_data
        if len(self._extra_data.keys() & self._role2docs.keys()) > 0:
            raise ValueError("Intersection of data and extra data keys is not empty")

    @property
    def roles(self) -> set[str | None]:
        return set(self._role2docs)

    @property
    def extra_roles(self) -> set[str]:
        return set(self._extra_data)

    def get_data(self, role: str | None = None) -> Iterable[TalismanDocument]:
        return self._role2docs[role]

    def get_extra_data(self, role: str) -> SerializableFS:
        return self._extra_data[role]

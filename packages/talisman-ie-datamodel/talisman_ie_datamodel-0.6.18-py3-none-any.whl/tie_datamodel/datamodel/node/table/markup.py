from typing import Mapping, Optional

from immutabledict import immutabledict
from tdm.abstract.datamodel import AbstractMarkup
from tdm.helper import freeze_dict
from typing_extensions import Self

from .abstract import AbstractTIETableNode


class TIETableNodeMarkup(AbstractMarkup, AbstractTIETableNode):
    __slots__ = ('_table_name', '_columns_meta')

    def __init__(self, table_name: Optional[str] = None, columns_meta: Mapping[str, str] = None):
        self._table_name = self._validate_table_name(table_name)
        self._columns_meta = self._validate_columns_meta(columns_meta) if columns_meta is not None else {}

    @staticmethod
    def _validate_table_name(table_name: str) -> Optional[str]:
        if table_name is not None:
            if not isinstance(table_name, str):
                raise ValueError
        return table_name

    @staticmethod
    def _validate_columns_meta(columns_meta: Mapping[str, str]) -> Mapping[str, str]:
        if not isinstance(columns_meta, (dict, immutabledict)):
            raise ValueError
        for key, value in columns_meta.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError
        return dict(columns_meta)

    @property
    def markup(self) -> immutabledict:
        return freeze_dict({
            'table_name': self._table_name,
            'columns_meta': self._columns_meta,
        })

    @classmethod
    def from_markup(cls, markup: AbstractMarkup) -> Self:
        kwargs: immutabledict = markup.markup
        table_name = kwargs.get('table_name')
        columns_meta = kwargs.get('columns_meta')
        return TIETableNodeMarkup(table_name, columns_meta)

    @property
    def table_name(self) -> Optional[str]:
        return self._table_name

    @property
    def columns_meta(self) -> Mapping[str, str]:
        return dict(self._columns_meta)

    def with_table_name(self, table_name: str) -> Self:
        return TIETableNodeMarkup(table_name, self._columns_meta)

    def with_columns_meta(self, columns_meta: Mapping[str, str]) -> Self:
        return TIETableNodeMarkup(self._table_name, columns_meta)

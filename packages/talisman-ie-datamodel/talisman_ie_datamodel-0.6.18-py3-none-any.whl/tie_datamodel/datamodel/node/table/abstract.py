from abc import ABCMeta, abstractmethod
from typing import Iterable, Mapping

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractNode
from tdm.datamodel.nodes import TableNode
from tdm.wrapper.node import modifier
from typing_extensions import Self


class AbstractTIETableNode(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def table_name(self) -> str | None:
        """
        get name of table
        """
        pass

    @property
    @abstractmethod
    def columns_meta(self) -> Mapping[str, str]:
        """
        get meta-information for all columns
        """
        pass

    # methods for table modifier

    @modifier
    @abstractmethod
    def with_table_name(self, table_name: str) -> Self:
        """
        set specified name for table
        :param table_name: table name
        :return: new table content with specified table name
        """
        pass

    @modifier
    @abstractmethod
    def with_columns_meta(self, meta: Mapping[str, str]) -> Self:
        """
        set meta-information for specified columns
        :param meta: dict 'row_index'->'meta' with meta-information to be added to columns.
        :return: new table content with specified columns meta
        """
        pass


class AbstractTableView(metaclass=ABCMeta):
    __slots__ = ()

    @property
    @abstractmethod
    def table_node(self) -> TableNode:
        """
        get table node
        """
        pass

    @property
    @abstractmethod
    def document(self) -> TalismanDocument:
        """
        get Talisman document
        """
        pass

    @property
    @abstractmethod
    def table_structure(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        """
        get table structure in form of matrix
        """
        pass

    @property
    @abstractmethod
    def columns_number(self) -> int:
        """
        get number of columns
        """
        pass

    @property
    @abstractmethod
    def rows_number(self) -> int:
        """
        get number of rows
        """
        pass

    @property
    @abstractmethod
    def header_indices(self) -> tuple[int, ...]:
        """
        get indices of header rows
        :return: table header rows ordered top-to-bottom
        """
        pass

    @property
    @abstractmethod
    def header(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        """
        get table header rows
        :return: tuple of rows, each row is tuple of cells content
        """
        pass

    @property
    @abstractmethod
    def transposition(self) -> bool:
        """
        get flag for table transposition
        """
        pass

    @abstractmethod
    def column(self, column: int, *, include_header: bool = False) -> tuple[AbstractNode | None, ...]:
        """
        get column cells for specified index. This method could include or exclude header cells from result
        :param column: target cell column index in range [0; columns_number)
        :param include_header: flag to include or exclude header cells from result
        :return: table cells content ordered top-to-bottom
        """
        pass

    @abstractmethod
    def row(self, row: int) -> tuple[AbstractNode | None, ...]:
        """
        get row cells for specified row index
        :param row: target cell row index in range [0; rows_number)
        :return: table cells content ordered left-to-right
        """
        pass

    @abstractmethod
    def cell(self, row: int, column: int) -> AbstractNode | None:
        """
        get cell content by row and column number
        :param row: target cell row index in range [0; rows_number)
        :param column: target cell column index in range [0; columns_number)
        :return: content contained in specified cell
        """
        pass

    @abstractmethod
    def with_header(self, rows: Iterable[int]) -> Self:
        """
        set specified rows as header
        :param rows: iterable of header rows indices
        :return: new table content with specified rows marked as header
        """
        pass

    @abstractmethod
    def transpose(self, transposition: bool) -> Self:
        """
        transpose horizontal table structure to vertical (tabular data in vertical columns)
        :param transposition: flag of table transposition
        :return: new table content in vertical form
        """
        pass

from abc import ABCMeta
from typing import Callable, Iterable, Iterator

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractNode
from tdm.datamodel.nodes import TableNode, TextNode
from typing_extensions import Self

from tie_datamodel.datamodel.node.table.abstract import AbstractTableView


class TableView(AbstractTableView, metaclass=ABCMeta):
    __slots__ = ("_table_node", "_document", "_table_structure", "_header_indices", "_columns_number", "_rows_number", "_transposition")

    def __init__(
            self,
            table_node: TableNode,
            document: TalismanDocument,
            header_indices: Iterable[int] | None = None,
            transposition: bool = False
    ):
        self._table_node = table_node
        self._document = document
        self._transposition = transposition

        # Get table structure and headers (if necessary)
        table_structure, metadata_headers = self._get_table_structure(table_node, document, transposition, header_indices is None)

        # Transpose table (if necessary)
        self._table_structure = self._transpose(table_structure) if transposition else table_structure

        # Setting up heading indexes
        self._header_indices = tuple(header_indices) if header_indices is not None else metadata_headers

        # Calculating table sizes
        self._rows_number = len(self._table_structure)
        self._columns_number = len(self._table_structure[0]) if self._rows_number > 0 else 0

    @staticmethod
    def _get_table_structure(
            table_node: TableNode, document: TalismanDocument, transposition: bool, need_headers: bool = True
    ) -> tuple[tuple[tuple[AbstractNode | None, ...], ...], tuple[int, ...]]:
        # TODO: implement processing of different node types (now cell is atomic and represents TextNode)
        table_structure, headers_list = [], []
        for i, row in enumerate(document.child_nodes(table_node)):
            cells = []
            for j, cell in enumerate(document.child_nodes(row)):
                # Extracting cell content
                nodes = document.child_nodes(cell)
                cell_content = None
                if nodes:
                    first_node = nodes[0]
                    if isinstance(first_node, TextNode) and first_node.content:
                        cell_content = first_node
                cells.append(cell_content)

                # Processing headers (if necessary)
                if need_headers and cell.metadata.header:
                    header_idx = j if transposition else i
                    if header_idx not in headers_list:
                        headers_list.append(header_idx)

            table_structure.append(tuple(cells))

        return tuple(table_structure), tuple(headers_list)

    @staticmethod
    def _transpose(table_structure: tuple[tuple[AbstractNode | None, ...], ...]) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return tuple(zip(*table_structure))

    def _validate_indices(self, row: int | None = None, column: int | None = None):
        if row is not None and (row < 0 or row >= self.rows_number):
            raise ValueError(f"Row index should be in range [0, {self.rows_number})!")
        if column is not None and (column < 0 or column >= self.columns_number):
            raise ValueError(f"Column index should be in range [0, {self.columns_number})!")

    @property
    def table_node(self) -> TableNode:
        return self._table_node

    @property
    def document(self) -> TalismanDocument:
        return self._document

    @property
    def table_structure(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return self._table_structure

    @property
    def columns_number(self) -> int:
        return self._columns_number

    @property
    def rows_number(self) -> int:
        return self._rows_number

    @property
    def header_indices(self) -> tuple[int, ...]:
        return self._header_indices

    @property
    def transposition(self) -> bool:
        return self._transposition

    @property
    def header(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return tuple(self.row(idx) for idx in self._header_indices)

    def _column_iterator(self, column: int, *, include_header: bool = False, row_start: int = 0, row_end: int | None = None,
                         cell_filter: Callable[[int, int], bool] = lambda row, column: True) -> Iterator[AbstractNode | None]:
        """
        Iterates table over specified column from row_start to row_end (defaults to table size).
        Cells for which cell_filter returns False are ignored.
        """
        if row_end is None:
            row_end = self.rows_number - 1
        step = 1 if row_start < row_end else -1
        for row in range(row_start, row_end + step, step):
            if cell_filter(row, column):
                if include_header:
                    yield self.cell(row, column)
                else:
                    if row not in self.header_indices:
                        yield self.cell(row, column)

    def _row_iterator(self, row: int, *, column_start: int = 0, column_end: int | None = None,
                      cell_filter: Callable[[int, int], bool] = lambda row, column: True) -> Iterator[AbstractNode | None]:
        """
        Iterates table over specified row from column_start to column_end (defaults to table size).
        Cells on which cell_filter returns False are ignored.
        """
        if column_end is None:
            column_end = self.columns_number - 1
        step = 1 if column_start < column_end else -1
        for column in range(column_start, column_end + step, step):
            if cell_filter(row, column):
                yield self.cell(row, column)

    def column(self, column: int, *, include_header: bool = False) -> tuple[AbstractNode | None, ...]:
        return tuple(self._column_iterator(column, include_header=include_header))

    def row(self, row: int) -> tuple[AbstractNode | None, ...]:
        return tuple(self._row_iterator(row))

    def cell(self, row: int, column: int) -> AbstractNode | None:
        self._validate_indices(row, column)
        return self._table_structure[row][column]

    def with_header(self, rows: Iterable[int]) -> Self:
        return TableView(self._table_node, self._document, tuple(rows), self._transposition)

    def transpose(self, transposition: bool) -> Self:
        return TableView(self._table_node, self._document, None, transposition)

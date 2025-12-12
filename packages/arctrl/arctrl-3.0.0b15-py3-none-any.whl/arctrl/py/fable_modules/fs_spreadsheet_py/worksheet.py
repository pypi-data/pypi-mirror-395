from __future__ import annotations
from typing import Any
from ..fable_library.array_ import (iterate as iterate_1, iterate_indexed)
from ..fable_library.option import some
from ..fable_library.seq import iterate
from ..fable_library.types import Array
from ..fable_library.util import ignore
from ..fable_openpyxl.openpyxl import (Worksheet, Table, Workbook, Cell)
from ..fs_spreadsheet.Cells.fs_cell import FsCell
from ..fs_spreadsheet.fs_worksheet import FsWorksheet
from ..fs_spreadsheet.Tables.fs_table import FsTable
from .cell import (from_fs_cell, to_fs_cell)
from .table import (from_fs_table, to_fs_table)

def from_fs_worksheet(parent: Workbook, fs_ws: FsWorksheet) -> Worksheet:
    py_ws: Worksheet = parent.create_sheet(fs_ws.Name)
    def action(table: FsTable, parent: Any=parent, fs_ws: Any=fs_ws) -> None:
        py_table: Table = from_fs_table(table)
        value: None = py_ws.add_table(py_table)
        ignore(None)

    iterate(action, fs_ws.Tables)
    def action_1(cell: FsCell, parent: Any=parent, fs_ws: Any=fs_ws) -> None:
        py_cell: Any | None = from_fs_cell(cell)
        ignore(py_ws.cell(cell.Address.RowNumber, cell.Address.ColumnNumber, some(py_cell)))

    iterate(action_1, fs_ws.CellCollection.GetCells())
    return py_ws


def to_fs_worksheet(py_ws: Worksheet) -> FsWorksheet:
    fs_ws: FsWorksheet = FsWorksheet(py_ws.title)
    def action(table: Table, py_ws: Any=py_ws) -> None:
        t: FsTable = to_fs_table(table)
        ignore(fs_ws.AddTable(t))

    iterate_1(action, list(py_ws.tables.values()))
    def action_2(row_index: int, row: Array[Cell], py_ws: Any=py_ws) -> None:
        def action_1(col_index: int, cell: Cell, row_index: Any=row_index, row: Any=row) -> None:
            if (type(cell.value).__name__) != "NoneType":
                c: FsCell = to_fs_cell(py_ws.title, row_index + 1, col_index + 1, cell)
                ignore(fs_ws.AddCell(c))


        iterate_indexed(action_1, row)

    iterate_indexed(action_2, [list(inner_tuple) for inner_tuple in py_ws.rows])
    return fs_ws


__all__ = ["from_fs_worksheet", "to_fs_worksheet"]


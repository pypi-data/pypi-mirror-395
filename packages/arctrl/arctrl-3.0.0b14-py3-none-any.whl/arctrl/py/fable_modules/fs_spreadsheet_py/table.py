from __future__ import annotations
from abc import abstractmethod
from openpyxl.worksheet.table import (TableStyleInfo, Table)
from typing import Protocol
from ..fable_openpyxl.openpyxl import Table as Table_1
from ..fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress
from ..fs_spreadsheet.Tables.fs_table import FsTable

class tablestyle(Protocol):
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def show_column_stripes(self) -> bool:
        ...

    @abstractmethod
    def show_first_column(self) -> bool:
        ...

    @abstractmethod
    def show_last_column(self) -> bool:
        ...

    @abstractmethod
    def show_row_stripes(self) -> bool:
        ...


class TableStyleStatic(Protocol):
    @abstractmethod
    def create(self, name: str, showFirstColumn: bool, showLastColumn: bool, showRowStripes: bool, showColumnStripes: bool) -> tablestyle:
        ...


def default_table_style(__unit: None=None) -> tablestyle:
    return TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=True)


def from_fs_table(fs_table: FsTable) -> Table:
    table: Table = Table(displayName=fs_table.Name, ref=fs_table.RangeAddress.Range)
    table.tableStyleInfo = default_table_style()
    return table


def to_fs_table(table: Table) -> FsTable:
    name: str = table.name if ((table.displayName) is None) else (table.displayName)
    ref: str = table.ref
    return FsTable(name, FsRangeAddress.from_string(ref))


__all__ = ["default_table_style", "from_fs_table", "to_fs_table"]


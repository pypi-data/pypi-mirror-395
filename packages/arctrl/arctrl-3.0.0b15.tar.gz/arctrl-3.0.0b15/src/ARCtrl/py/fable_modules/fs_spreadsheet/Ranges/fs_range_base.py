from __future__ import annotations
from typing import Any
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_fail, printf)
from ...fable_library.util import (equals, ignore, IEnumerable_1)
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import FsAddress
from .fs_range_address import FsRangeAddress

def _expr165() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeBase", None, FsRangeBase)


class FsRangeBase:
    def __init__(self, range_address: FsRangeAddress) -> None:
        self._sortRows: Any = None
        self._sortColumns: Any = None
        self._rangeAddress: FsRangeAddress = range_address
        _id: int
        FsRangeBase.IdCounter = (FsRangeBase.IdCounter + 1) or 0
        _id = FsRangeBase.IdCounter

    def Extend(self, address: FsAddress) -> None:
        this: FsRangeBase = self
        this._rangeAddress.Extend(address)

    @property
    def RangeAddress(self, __unit: None=None) -> FsRangeAddress:
        this: FsRangeBase = self
        return this._rangeAddress

    @RangeAddress.setter
    def RangeAddress(self, range_adress: FsRangeAddress) -> None:
        this: FsRangeBase = self
        if not equals(range_adress, this._rangeAddress):
            old_address: FsRangeAddress = this._rangeAddress
            this._rangeAddress = range_adress


    def Cell(self, cell_address_in_range: FsAddress, cells: FsCellsCollection) -> FsCell:
        this: FsRangeBase = self
        abs_row: int = ((cell_address_in_range.RowNumber + this.RangeAddress.FirstAddress.RowNumber) - 1) or 0
        abs_column: int = ((cell_address_in_range.ColumnNumber + this.RangeAddress.FirstAddress.ColumnNumber) - 1) or 0
        if True if (abs_row <= 0) else (abs_row > 1048576):
            arg: int = cells.MaxRowNumber or 0
            to_fail(printf("Row number must be between 1 and %i"))(arg)

        if True if (abs_column <= 0) else (abs_column > 16384):
            arg_1: int = cells.MaxColumnNumber or 0
            to_fail(printf("Column number must be between 1 and %i"))(arg_1)

        cell: FsCell | None = cells.TryGetCell(abs_row, abs_column)
        if cell is None:
            absolute_address: FsAddress = FsAddress(abs_row, abs_column, cell_address_in_range.FixedRow, cell_address_in_range.FixedColumn)
            new_cell: FsCell = FsCell.create_empty_with_adress(absolute_address)
            this.Extend(absolute_address)
            value: None = cells.Add(new_cell, abs_row, abs_column)
            ignore(None)
            return new_cell

        else: 
            return cell


    def Cells(self, cells: FsCellsCollection) -> IEnumerable_1[FsCell]:
        this: FsRangeBase = self
        return cells.GetCellsInStringRange(this.RangeAddress.FirstAddress, this.RangeAddress.LastAddress)

    def ColumnCount(self, __unit: None=None) -> int:
        this: FsRangeBase = self
        return (this._rangeAddress.LastAddress.ColumnNumber - this._rangeAddress.FirstAddress.ColumnNumber) + 1

    def RowCount(self, __unit: None=None) -> int:
        this: FsRangeBase = self
        return (this._rangeAddress.LastAddress.RowNumber - this._rangeAddress.FirstAddress.RowNumber) + 1


FsRangeBase_reflection = _expr165

def FsRangeBase__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeBase:
    return FsRangeBase(range_address)


def FsRangeBase__cctor(__unit: None=None) -> None:
    FsRangeBase.IdCounter = 0


FsRangeBase__cctor()

__all__ = ["FsRangeBase_reflection"]


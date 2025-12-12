from __future__ import annotations
from typing import Any
from ...fable_library.list import FSharpList
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (to_list, map)
from ...fable_library.util import IEnumerable_1
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import FsAddress
from .fs_range_address import FsRangeAddress
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection)

def _expr184() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeColumn", None, FsRangeColumn, FsRangeBase_reflection())


class FsRangeColumn(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress) -> None:
        super().__init__(range_address)
        pass

    @staticmethod
    def from_index(index: int) -> FsRangeColumn:
        return FsRangeColumn(FsRangeAddress(FsAddress(0, index), FsAddress(0, index)))

    @property
    def Index(self, __unit: None=None) -> int:
        self_1: FsRangeColumn = self
        return self_1.RangeAddress.FirstAddress.ColumnNumber

    @Index.setter
    def Index(self, i: int) -> None:
        self_1: FsRangeColumn = self
        self_1.RangeAddress.FirstAddress.ColumnNumber = i or 0
        self_1.RangeAddress.LastAddress.ColumnNumber = i or 0

    def Cell(self, row_index: int, cells_collection: FsCellsCollection) -> FsCell:
        return super().Cell(FsAddress((row_index - super().RangeAddress.FirstAddress.RowNumber) + 1, 1), cells_collection)

    def FirstCell(self, cells: FsCellsCollection) -> FsCell:
        return super().Cell(FsAddress(1, 1), cells)

    def Cells(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return super().Cells(cells_collection)

    @staticmethod
    def from_range_address(range_address: FsRangeAddress) -> FsRangeColumn:
        return FsRangeColumn(range_address)

    def Copy(self, __unit: None=None) -> FsRangeColumn:
        self_1: FsRangeColumn = self
        return FsRangeColumn(self_1.RangeAddress.Copy())

    @staticmethod
    def copy(range_column: FsRangeColumn) -> FsRangeColumn:
        return range_column.Copy()


FsRangeColumn_reflection = _expr184

def FsRangeColumn__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeColumn:
    return FsRangeColumn(range_address)


def FsSpreadsheet_FsRangeAddress__FsRangeAddress_toRangeColumns_Static_6A2513BC(range_address: FsRangeAddress) -> IEnumerable_1[FsRangeColumn]:
    columns: FSharpList[int] = to_list(range_big_int(range_address.FirstAddress.ColumnNumber, 1, range_address.LastAddress.ColumnNumber))
    fst_row: int = range_address.FirstAddress.RowNumber or 0
    lst_row: int = range_address.LastAddress.RowNumber or 0
    def mapping(c: int, range_address: Any=range_address) -> FsRangeColumn:
        return FsRangeColumn(FsRangeAddress(FsAddress(fst_row, c), FsAddress(lst_row, c)))

    return map(mapping, columns)


__all__ = ["FsRangeColumn_reflection", "FsSpreadsheet_FsRangeAddress__FsRangeAddress_toRangeColumns_Static_6A2513BC"]


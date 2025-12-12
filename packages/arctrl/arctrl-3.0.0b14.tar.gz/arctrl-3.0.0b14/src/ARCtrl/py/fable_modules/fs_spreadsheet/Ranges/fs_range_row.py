from __future__ import annotations
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.util import IEnumerable_1
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import FsAddress
from .fs_range_address import FsRangeAddress
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection)

def _expr166() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeRow", None, FsRangeRow, FsRangeBase_reflection())


class FsRangeRow(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress) -> None:
        super().__init__(range_address)
        pass

    @staticmethod
    def from_index(index: int) -> FsRangeRow:
        return FsRangeRow(FsRangeAddress(FsAddress(index, 0), FsAddress(index, 0)))

    @property
    def Index(self, __unit: None=None) -> int:
        self_1: FsRangeRow = self
        return self_1.RangeAddress.FirstAddress.RowNumber

    @Index.setter
    def Index(self, i: int) -> None:
        self_1: FsRangeRow = self
        self_1.RangeAddress.FirstAddress.RowNumber = i or 0
        self_1.RangeAddress.LastAddress.RowNumber = i or 0

    def Cell(self, column_index: int, cells: FsCellsCollection) -> FsCell:
        return super().Cell(FsAddress(1, (column_index - super().RangeAddress.FirstAddress.ColumnNumber) + 1), cells)

    def Cells(self, cells: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return super().Cells(cells)


FsRangeRow_reflection = _expr166

def FsRangeRow__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeRow:
    return FsRangeRow(range_address)


__all__ = ["FsRangeRow_reflection"]


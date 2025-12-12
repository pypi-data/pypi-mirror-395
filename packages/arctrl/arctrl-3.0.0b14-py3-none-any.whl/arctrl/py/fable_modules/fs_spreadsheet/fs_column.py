from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (length, min_by, max_by, map, exists)
from ..fable_library.util import (IEnumerable_1, compare_primitives, ignore, get_enumerator, IEnumerator, to_iterator)
from .Cells.fs_cell import FsCell
from .Cells.fs_cells_collection import FsCellsCollection
from .fs_address import FsAddress
from .Ranges.fs_range_address import FsRangeAddress
from .Ranges.fs_range_base import (FsRangeBase, FsRangeBase_reflection)

def _expr201() -> TypeInfo:
    return class_type("FsSpreadsheet.FsColumn", None, FsColumn, FsRangeBase_reflection())


class FsColumn(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress, cells: FsCellsCollection) -> None:
        super().__init__(range_address)
        self.cells_004018: FsCellsCollection = cells

    @staticmethod
    def empty(__unit: None=None) -> FsColumn:
        return FsColumn(FsRangeAddress(FsAddress(0, 0), FsAddress(0, 0)), FsCellsCollection())

    @staticmethod
    def create_at(index: int, cells: FsCellsCollection) -> FsColumn:
        def get_index_by(f: Callable[[Callable[[FsCell], int], IEnumerable_1[FsCell]], FsCell]) -> int:
            if length(cells.GetCellsInColumn(index)) == 0:
                return 1

            else: 
                def _arrow194(c: FsCell, f: Any=f) -> int:
                    return c.Address.RowNumber

                return f(_arrow194)(cells.GetCellsInColumn(index)).Address.RowNumber


        def _arrow197(projection: Callable[[FsCell], int]) -> Callable[[IEnumerable_1[FsCell]], FsCell]:
            def _arrow196(source_1: IEnumerable_1[FsCell]) -> FsCell:
                class ObjectExpr195:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return min_by(projection, source_1, ObjectExpr195())

            return _arrow196

        min_row_index: int = get_index_by(_arrow197) or 0
        def _arrow200(projection_1: Callable[[FsCell], int]) -> Callable[[IEnumerable_1[FsCell]], FsCell]:
            def _arrow199(source_2: IEnumerable_1[FsCell]) -> FsCell:
                class ObjectExpr198:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return max_by(projection_1, source_2, ObjectExpr198())

            return _arrow199

        max_row_index: int = get_index_by(_arrow200) or 0
        return FsColumn(FsRangeAddress(FsAddress(min_row_index, index), FsAddress(max_row_index, index)), cells)

    @property
    def Cells(self, __unit: None=None) -> IEnumerable_1[FsCell]:
        this: FsColumn = self
        return super().Cells(this.cells_004018)

    @property
    def Index(self, __unit: None=None) -> int:
        this: FsColumn = self
        return this.RangeAddress.FirstAddress.ColumnNumber

    @Index.setter
    def Index(self, i: int) -> None:
        this: FsColumn = self
        this.RangeAddress.FirstAddress.ColumnNumber = i or 0
        this.RangeAddress.LastAddress.ColumnNumber = i or 0

    @property
    def MinRowIndex(self, __unit: None=None) -> int:
        this: FsColumn = self
        return this.RangeAddress.FirstAddress.RowNumber

    @property
    def MaxRowIndex(self, __unit: None=None) -> int:
        this: FsColumn = self
        return this.RangeAddress.LastAddress.RowNumber

    def Copy(self, __unit: None=None) -> FsColumn:
        this: FsColumn = self
        ra: FsRangeAddress = this.RangeAddress.Copy()
        def mapping(c: FsCell) -> FsCell:
            return c.Copy()

        cells: IEnumerable_1[FsCell] = map(mapping, this.Cells)
        fcc: FsCellsCollection = FsCellsCollection()
        fcc.AddMany(cells)
        return FsColumn(ra, fcc)

    @staticmethod
    def copy(column: FsColumn) -> FsColumn:
        return column.Copy()

    @staticmethod
    def get_index(column: FsColumn) -> int:
        return column.Index

    def HasCellAt(self, row_index: int) -> bool:
        this: FsColumn = self
        def predicate(c: FsCell) -> bool:
            return c.RowNumber == row_index

        return exists(predicate, this.Cells)

    @staticmethod
    def has_cell_at(row_index: int, column: FsColumn) -> bool:
        return column.HasCellAt(row_index)

    def Item(self, row_index: int) -> FsCell:
        this: FsColumn = self
        return super().Cell(FsAddress(row_index, 1), this.cells_004018)

    @staticmethod
    def item(row_index: int, column: FsColumn) -> FsCell:
        return column.Item(row_index)

    def TryItem(self, row_index: int) -> FsCell | None:
        this: FsColumn = self
        return this.Item(row_index) if this.HasCellAt(row_index) else None

    @staticmethod
    def try_item(row_index: int, column: FsColumn) -> FsCell | None:
        return column.TryItem(row_index)

    def ToDenseColumn(self, __unit: None=None) -> None:
        this: FsColumn = self
        for i in range(this.MinRowIndex, this.MaxRowIndex + 1, 1):
            ignore(this.Item(i))

    @staticmethod
    def to_dense_column(column: FsColumn) -> FsColumn:
        column.ToDenseColumn()
        return column

    @staticmethod
    def create_dense_column_of(column: FsColumn) -> FsColumn:
        new_column: FsColumn = column.Copy()
        new_column.ToDenseColumn()
        return new_column

    def GetEnumerator(self, __unit: None=None) -> IEnumerator[FsCell]:
        this: FsColumn = self
        return get_enumerator(this.Cells)

    def __iter__(self) -> IEnumerator[FsCell]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None=None) -> IEnumerator[Any]:
        this: FsColumn = self
        return get_enumerator(this)


FsColumn_reflection = _expr201

def FsColumn__ctor_7678C70A(range_address: FsRangeAddress, cells: FsCellsCollection) -> FsColumn:
    return FsColumn(range_address, cells)


__all__ = ["FsColumn_reflection"]


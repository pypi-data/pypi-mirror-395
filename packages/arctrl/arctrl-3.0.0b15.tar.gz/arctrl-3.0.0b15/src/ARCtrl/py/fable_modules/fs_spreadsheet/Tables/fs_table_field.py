from __future__ import annotations
from typing import Any
from ...fable_library.option import (some, default_arg)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import skip
from ...fable_library.string_ import (to_fail, printf)
from ...fable_library.util import (equals, IEnumerable_1)
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import FsAddress
from ..Ranges.fs_range_address import FsRangeAddress
from ..Ranges.fs_range_column import FsRangeColumn

def _expr203() -> TypeInfo:
    return class_type("FsSpreadsheet.FsTableField", None, FsTableField)


class FsTableField:
    def __init__(self, name: str, index: int | None=None, column: FsRangeColumn | None=None, totals_row_label: Any | None=None, totals_row_function: Any | None=None) -> None:
        self._totalsRowsFunction: Any = default_arg(totals_row_function, None)
        self._totalsRowLabel: Any = default_arg(totals_row_label, None)
        self._column: FsRangeColumn = default_arg(column, None)
        self._index: int = default_arg(index, 0) or 0
        self._name: str = name
        self._Column: FsRangeColumn = self._column

    @property
    def Column(self, __unit: None=None) -> FsRangeColumn:
        __: FsTableField = self
        return __._Column

    @Column.setter
    def Column(self, v: FsRangeColumn) -> None:
        __: FsTableField = self
        __._Column = v

    @property
    def Index(self, __unit: None=None) -> int:
        this: FsTableField = self
        return this._index

    @Index.setter
    def Index(self, index: int) -> None:
        this: FsTableField = self
        if index == this._index:
            pass

        else: 
            this._index = index or 0
            if equals(this._column, None):
                pass

            else: 
                ind_diff: int = (index - this._index) or 0
                new_col: FsRangeColumn = FsRangeColumn(FsRangeAddress(FsAddress(this.Column.RangeAddress.FirstAddress.RowNumber, this._index + ind_diff), FsAddress(this.Column.RangeAddress.LastAddress.RowNumber, this._index + ind_diff)))
                this.Column = new_col



    @property
    def Name(self, __unit: None=None) -> str:
        this: FsTableField = self
        return this._name

    def SetName(self, name: str, cells_collection: FsCellsCollection, show_header_row: bool) -> None:
        this: FsTableField = self
        this._name = name
        if show_header_row:
            this.Column.FirstCell(cells_collection).SetValueAs(name)


    @staticmethod
    def set_name(name: str, cells_collection: FsCellsCollection, show_header_row: bool, table_field: FsTableField) -> FsTableField:
        table_field.SetName(name, cells_collection, show_header_row)
        return table_field

    def Copy(self, __unit: None=None) -> FsTableField:
        this: FsTableField = self
        col: FsRangeColumn = this.Column.Copy()
        ind: int = this.Index or 0
        return FsTableField(this.Name, ind, col, some(None), some(None))

    @staticmethod
    def copy(table_field: FsTableField) -> FsTableField:
        return table_field.Copy()

    def HeaderCell(self, cells_collection: FsCellsCollection, show_header_row: bool) -> FsCell:
        this: FsTableField = self
        if not show_header_row:
            arg: str = this._name
            return to_fail(printf("tried to get header cell of table field \"%s\" even though showHeaderRow is set to zero"))(arg)

        else: 
            return this.Column.FirstCell(cells_collection)


    @staticmethod
    def get_header_cell(cells_collection: FsCellsCollection, show_header_row: bool, table_field: FsTableField) -> FsCell:
        return table_field.HeaderCell(cells_collection, show_header_row)

    def DataCells(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        this: FsTableField = self
        return skip(1, this.Column.Cells(cells_collection))

    @staticmethod
    def get_data_cells(cells_collection: FsCellsCollection, table_field: FsTableField) -> IEnumerable_1[FsCell]:
        return table_field.DataCells(cells_collection)


FsTableField_reflection = _expr203

def FsTableField__ctor_E675DBB(name: str, index: int | None=None, column: FsRangeColumn | None=None, totals_row_label: Any | None=None, totals_row_function: Any | None=None) -> FsTableField:
    return FsTableField(name, index, column, totals_row_label, totals_row_function)


__all__ = ["FsTableField_reflection"]


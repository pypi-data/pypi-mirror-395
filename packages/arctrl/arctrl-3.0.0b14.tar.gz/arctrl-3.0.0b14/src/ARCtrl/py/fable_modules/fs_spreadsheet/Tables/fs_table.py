from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.map_util import (add_to_set, add_to_dict, get_item_from_dict, remove_from_dict)
from ...fable_library.option import (some, value as value_2, default_arg)
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (initialize, delay, collect, singleton, reduce, map, iterate_indexed, iterate, length, max, find, try_find, try_pick, choose, to_list, exists)
from ...fable_library.string_ import (to_text, printf, replace)
from ...fable_library.util import (equals, IEnumerable_1, int32_to_string, ignore, compare_primitives, get_enumerator)
from ..Cells.fs_cell import (FsCell, DataType)
from ..Cells.fs_cells_collection import (FsCellsCollection, Dictionary_tryGet)
from ..fs_address import FsAddress
from ..fs_column import FsColumn
from ..fs_row import FsRow
from ..Ranges.fs_range import FsRange
from ..Ranges.fs_range_address import FsRangeAddress
from ..Ranges.fs_range_base import (FsRangeBase, FsRangeBase_reflection)
from ..Ranges.fs_range_column import FsRangeColumn
from ..Ranges.fs_range_row import FsRangeRow
from .fs_table_field import FsTableField

def _expr218() -> TypeInfo:
    return class_type("FsSpreadsheet.FsTable", None, FsTable, FsRangeBase_reflection())


class FsTable(FsRangeBase):
    def __init__(self, name: str, range_address: FsRangeAddress, show_totals_row: bool | None=None, show_header_row: bool | None=None, field_names: IEnumerable_1[str] | None=None) -> None:
        super().__init__(range_address)
        self._name: str = replace(name.strip(), " ", "_")
        self._lastRangeAddress: FsRangeAddress = range_address
        self._showTotalsRow: bool = default_arg(show_totals_row, False)
        self._showHeaderRow: bool = default_arg(show_header_row, True)
        def _arrow217(__unit: None=None) -> Any:
            fns: IEnumerable_1[str] = field_names
            if length(fns) != super().ColumnCount():
                def _arrow216(__unit: None=None) -> str:
                    arg: int = length(fns) or 0
                    arg_1: int = super().ColumnCount() or 0
                    return to_text(printf("The number of field names (%i) must match the number of columns (%i) in the range."))(arg)(arg_1)

                raise Exception(_arrow216(), "fieldNames")

            dict_1: Any = dict([])
            def action(i: int, fn: str) -> None:
                col_i: int = (range_address.FirstAddress.ColumnNumber + i) or 0
                add_to_dict(dict_1, fn, FsTableField(fn, i, FsRangeColumn(FsRangeAddress(FsAddress(range_address.FirstAddress.RowNumber, col_i), FsAddress(range_address.LastAddress.RowNumber, col_i)))))

            iterate_indexed(action, fns)
            return dict_1

        self._fieldNames: Any = dict([]) if (field_names is None) else _arrow217()
        self._uniqueNames: Any = set([])

    @property
    def Name(self, __unit: None=None) -> str:
        this: FsTable = self
        return this._name

    def GetFieldNames(self, cells_collection: FsCellsCollection) -> Any:
        this: FsTable = self
        if equals(this._lastRangeAddress, this.RangeAddress) if ((not equals(this._lastRangeAddress, None)) if (not equals(this._fieldNames, None)) else False) else False:
            return this._fieldNames

        else: 
            this._lastRangeAddress = this.RangeAddress
            return this._fieldNames


    def GetFields(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsTableField]:
        this: FsTable = self
        def _arrow204(i: int) -> FsTableField:
            return this.GetFieldAt(i, cells_collection)

        return initialize(super().ColumnCount(), _arrow204)

    @property
    def ShowHeaderRow(self, __unit: None=None) -> bool:
        this: FsTable = self
        return this._showHeaderRow

    @ShowHeaderRow.setter
    def ShowHeaderRow(self, show_header_row: bool) -> None:
        this: FsTable = self
        this._showHeaderRow = show_header_row

    def HeadersRow(self, __unit: None=None) -> FsRangeRow:
        this: FsTable = self
        return None if (not this.ShowHeaderRow) else FsRange(super().RangeAddress).FirstRow()

    def TryGetHeaderRow(self, cells_collection: FsCellsCollection) -> FsRow | None:
        this: FsTable = self
        match_value: bool = this.ShowHeaderRow
        if match_value:
            row_index: int = this.RangeAddress.FirstAddress.RowNumber or 0
            return FsRow(FsRangeAddress(FsAddress(row_index, this.RangeAddress.FirstAddress.ColumnNumber), FsAddress(row_index, this.RangeAddress.LastAddress.ColumnNumber)), cells_collection)

        else: 
            return None


    def GetHeaderRow(self, cells_collection: FsCellsCollection) -> FsRow:
        this: FsTable = self
        match_value: FsRow | None = this.TryGetHeaderRow(cells_collection)
        if match_value is None:
            raise Exception(("Error. Unable to get header row for table \"" + this.Name) + "\" as `ShowHeaderRow` is set to `false`.")

        else: 
            return match_value


    def GetColumns(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsColumn]:
        this: FsTable = self
        def _arrow206(__unit: None=None) -> IEnumerable_1[FsColumn]:
            def _arrow205(i: int) -> IEnumerable_1[FsColumn]:
                return singleton(FsColumn(FsRangeAddress(FsAddress(this.RangeAddress.FirstAddress.RowNumber, i), FsAddress(this.RangeAddress.LastAddress.RowNumber, i)), cells_collection))

            return collect(_arrow205, range_big_int(this.RangeAddress.FirstAddress.ColumnNumber, 1, this.RangeAddress.LastAddress.ColumnNumber))

        return delay(_arrow206)

    def GetRows(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsRow]:
        this: FsTable = self
        def _arrow208(__unit: None=None) -> IEnumerable_1[FsRow]:
            def _arrow207(i: int) -> IEnumerable_1[FsRow]:
                return singleton(FsRow(FsRangeAddress(FsAddress(i, this.RangeAddress.FirstAddress.ColumnNumber), FsAddress(i, this.RangeAddress.LastAddress.ColumnNumber)), cells_collection))

            return collect(_arrow207, range_big_int(this.RangeAddress.FirstAddress.RowNumber, 1, this.RangeAddress.LastAddress.RowNumber))

        return delay(_arrow208)

    def GetBodyRows(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsRow]:
        this: FsTable = self
        first_row_index: int = ((this.RangeAddress.FirstAddress.RowNumber + 1) if this.ShowHeaderRow else this.RangeAddress.FirstAddress.RowNumber) or 0
        def _arrow210(__unit: None=None) -> IEnumerable_1[FsRow]:
            def _arrow209(i: int) -> IEnumerable_1[FsRow]:
                return singleton(FsRow(FsRangeAddress(FsAddress(i, this.RangeAddress.FirstAddress.ColumnNumber), FsAddress(i, this.RangeAddress.LastAddress.ColumnNumber)), cells_collection))

            return collect(_arrow209, range_big_int(first_row_index, 1, this.RangeAddress.LastAddress.RowNumber))

        return delay(_arrow210)

    def GetRowAt(self, index: int, cells_collection: FsCellsCollection) -> FsRow:
        this: FsTable = self
        if True if (index <= 0) else (index > super().RowCount()):
            def _arrow211(__unit: None=None) -> str:
                arg: int = super().RowCount() or 0
                return to_text(printf("Row index must be between 1 and %i"))(arg)

            raise Exception(int32_to_string(index), _arrow211())

        row_i: int = ((this.RangeAddress.FirstAddress.RowNumber + index) - 1) or 0
        return FsRow(FsRangeAddress(FsAddress(row_i, this.RangeAddress.FirstAddress.ColumnNumber), FsAddress(row_i, this.RangeAddress.LastAddress.ColumnNumber)), cells_collection)

    def GetBodyRowAt(self, index: int, cells_collection: FsCellsCollection) -> FsRow:
        this: FsTable = self
        return this.GetRowAt(index + 1, cells_collection) if this.ShowHeaderRow else this.GetRowAt(index, cells_collection)

    def RescanRange(self, __unit: None=None) -> None:
        this: FsTable = self
        def reduction(r1: FsRangeAddress, r2: FsRangeAddress) -> FsRangeAddress:
            return r1.Union(r2)

        def mapping(v: FsTableField) -> FsRangeAddress:
            return v.Column.RangeAddress

        range_address: FsRangeAddress = reduce(reduction, map(mapping, this._fieldNames.values()))
        this.RangeAddress = range_address

    @staticmethod
    def rescan_range(table: FsTable) -> FsTable:
        table.RescanRange()
        return table

    def GetUniqueName(self, original_name: str, initial_offset: int, enforce_offset: bool) -> str:
        this: FsTable = self
        name: str = original_name + (int32_to_string(initial_offset) if enforce_offset else "")
        if name in this._uniqueNames:
            i: int = initial_offset or 0
            name = original_name + int32_to_string(i)
            while name in this._uniqueNames:
                i = (i + 1) or 0
                name = original_name + int32_to_string(i)

        ignore(add_to_set(name, this._uniqueNames))
        return name

    @staticmethod
    def get_unique_names(original_name: str, initial_offset: int, enforce_offset: bool, table: FsTable) -> str:
        return table.GetUniqueName(original_name, initial_offset, enforce_offset)

    def InitFields(self, field_names: IEnumerable_1[str]) -> None:
        this: FsTable = self
        def action(i: int, fn: str) -> None:
            table_field: FsTableField = FsTableField(fn, i, FsRangeColumn.from_index(i))
            add_to_dict(this._fieldNames, fn, table_field)

        iterate_indexed(action, field_names)

    @staticmethod
    def init_fields(field_names: IEnumerable_1[str], table: FsTable) -> FsTable:
        table.InitFields(field_names)
        return table

    def AddFields(self, table_fields: IEnumerable_1[FsTableField]) -> None:
        this: FsTable = self
        def action(tf: FsTableField) -> None:
            add_to_dict(this._fieldNames, tf.Name, tf)

        iterate(action, table_fields)

    @staticmethod
    def add_fields(table_fields: IEnumerable_1[FsTableField], table: FsTable) -> FsTable:
        table.AddFields(table_fields)
        return table

    def Field(self, name: str, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(name, this._fieldNames)
        if match_value is None:
            def _arrow213(__unit: None=None) -> int:
                def mapping(v: FsTableField) -> int:
                    return v.Index

                s: IEnumerable_1[int] = map(mapping, this._fieldNames.values())
                class ObjectExpr212:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return 0 if (length(s) == 0) else max(s, ObjectExpr212())

            def _arrow214(__unit: None=None) -> FsRangeAddress:
                offset: int = len(this._fieldNames) or 0
                return FsRangeAddress(FsAddress(this.RangeAddress.FirstAddress.RowNumber, this.RangeAddress.FirstAddress.ColumnNumber + offset), FsAddress(this.RangeAddress.LastAddress.RowNumber, this.RangeAddress.FirstAddress.ColumnNumber + offset))

            new_field: FsTableField = FsTableField(name, _arrow213() + 1, FsRangeColumn(_arrow214()), some(None), some(None))
            if this.ShowHeaderRow:
                value: None = new_field.HeaderCell(cells_collection, True).SetValueAs(name)
                ignore(None)

            add_to_dict(this._fieldNames, name, new_field)
            this.RescanRange()
            return new_field

        else: 
            return match_value


    def GetField(self, name: str, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        name_1: str = replace(name, "\r\n", "\n")
        try: 
            return get_item_from_dict(this.GetFieldNames(cells_collection), name_1)

        except Exception as match_value:
            raise Exception(("The header row doesn\'t contain field name \'" + name_1) + "\'.")


    @staticmethod
    def get_field(name: str, cells_collection: FsCellsCollection, table: FsTable) -> FsTableField:
        return table.GetField(name, cells_collection)

    def GetFieldAt(self, index: int, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        try: 
            def predicate(ftf: FsTableField) -> bool:
                return ftf.Index == index

            return find(predicate, this.GetFieldNames(cells_collection).values())

        except Exception as match_value:
            raise Exception(("FsTableField with index " + str(index)) + " does not exist in the FsTable.")


    def GetFieldIndex(self, name: str, cells_collection: FsCellsCollection) -> int:
        this: FsTable = self
        return this.GetField(name, cells_collection).Index

    def RenameField(self, old_name: str, new_name: str) -> None:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(old_name, this._fieldNames)
        if match_value is None:
            raise Exception("The FsTabelField does not exist in this FsTable", "oldName")

        else: 
            field: FsTableField = match_value
            ignore(remove_from_dict(this._fieldNames, old_name))
            add_to_dict(this._fieldNames, new_name, field)


    @staticmethod
    def rename_field(old_name: str, new_name: str, table: FsTable) -> FsTable:
        table.RenameField(old_name, new_name)
        return table

    def TryGetHeaderCellOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> FsCell | None:
        this: FsTable = self
        fst_row_index: int = this.RangeAddress.FirstAddress.RowNumber or 0
        def predicate(c: FsCell) -> bool:
            return c.RowNumber == fst_row_index

        return try_find(predicate, cells_collection.GetCellsInColumn(col_index))

    @staticmethod
    def try_get_header_cell_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfColumnAt(cells_collection, col_index)

    def TryGetHeaderCellOfColumn(self, cells_collection: FsCellsCollection, column: FsRangeColumn) -> FsCell | None:
        this: FsTable = self
        return this.TryGetHeaderCellOfColumnAt(cells_collection, column.Index)

    @staticmethod
    def try_get_header_cell_of_column(cells_collection: FsCellsCollection, column: FsRangeColumn, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfColumn(cells_collection, column)

    def GetHeaderCellOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfColumnAt(cells_collection, col_index))

    @staticmethod
    def get_header_cell_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfColumnAt(cells_collection, col_index)

    def GetHeaderCellOfColumn(self, cells_collection: FsCellsCollection, column: FsRangeColumn) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfColumn(cells_collection, column))

    @staticmethod
    def get_header_cell_of_column(cells_collection: FsCellsCollection, column: FsRangeColumn, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfColumn(cells_collection, column)

    def GetHeaderCellOfTableField(self, cells_collection: FsCellsCollection, table_field: FsTableField) -> FsCell:
        this: FsTable = self
        return table_field.HeaderCell(cells_collection, this.ShowHeaderRow)

    @staticmethod
    def get_header_cell_of_table_field(cells_collection: FsCellsCollection, table_field: FsTableField, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfTableField(cells_collection, table_field)

    def TryGetHeaderCellOfTableFieldAt(self, cells_collection: FsCellsCollection, table_field_index: int) -> FsCell | None:
        this: FsTable = self
        def chooser(tf: FsTableField) -> FsCell | None:
            if tf.Index == table_field_index:
                return tf.HeaderCell(cells_collection, this.ShowHeaderRow)

            else: 
                return None


        return try_pick(chooser, this._fieldNames.values())

    @staticmethod
    def try_get_header_cell_of_table_field_index_at(cells_collection: FsCellsCollection, table_field_index: int, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfTableFieldAt(cells_collection, table_field_index)

    def GetHeaderCellOfTableFieldAt(self, cells_collection: FsCellsCollection, table_field_index: int) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfTableFieldAt(cells_collection, table_field_index))

    @staticmethod
    def get_header_cell_of_table_field_index_at(cells_collection: FsCellsCollection, table_field_index: int, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfTableFieldAt(cells_collection, table_field_index)

    def TryGetHeaderCellByFieldName(self, cells_collection: FsCellsCollection, field_name: str) -> FsCell | None:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(field_name, this._fieldNames)
        if match_value is None:
            return None

        else: 
            tf: FsTableField = match_value
            return tf.HeaderCell(cells_collection, this.ShowHeaderRow)


    @staticmethod
    def try_get_header_cell_by_field_name(cells_collection: FsCellsCollection, field_name: str, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellByFieldName(cells_collection, field_name)

    def GetDataCellsOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> IEnumerable_1[FsCell]:
        this: FsTable = self
        def chooser(ri: int) -> FsCell | None:
            return cells_collection.TryGetCell(ri, col_index)

        return choose(chooser, to_list(range_big_int(this.RangeAddress.FirstAddress.RowNumber + 1, 1, this.RangeAddress.LastAddress.RowNumber)))

    @staticmethod
    def get_data_cells_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> IEnumerable_1[FsCell]:
        return table.GetDataCellsOfColumnAt(cells_collection, col_index)

    def Copy(self, __unit: None=None) -> FsTable:
        this: FsTable = self
        ra: FsRangeAddress = this.RangeAddress.Copy()
        return FsTable(this.Name, ra, False, this.ShowHeaderRow)

    @staticmethod
    def copy(table: FsTable) -> FsTable:
        return table.Copy()

    @staticmethod
    def validate_for_write(table: FsTable, cells_collection: FsCellsCollection) -> None:
        if length(table.GetBodyRows(cells_collection)) == 0:
            def _arrow215(__unit: None=None) -> str:
                arg: str = table.Name
                return to_text(printf("The table \'%s\' must contain at least one body row."))(arg)

            raise Exception(_arrow215(), "table")


    def RescanFieldNames(self, cells_collection: FsCellsCollection) -> None:
        this: FsTable = self
        if this.ShowHeaderRow:
            old_field_names: Any = this._fieldNames
            this._fieldNames = dict([])
            cell_pos: int = 0
            with get_enumerator(this.GetHeaderRow(cells_collection)) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    cell: FsCell = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    name: str = cell.ValueAsString()
                    match_value: FsTableField | None = Dictionary_tryGet(name, old_field_names)
                    if match_value is None:
                        if (name is None) != (name == ""):
                            name = this.GetUniqueName("Column", cell_pos + 1, True)
                            value: None = cell.SetValueAs(name)
                            ignore(None)
                            cell.DataType = DataType(0)

                        if name in this._fieldNames:
                            raise Exception(("The header row contains more than one field name \'" + name) + "\'.")

                        add_to_dict(this._fieldNames, name, FsTableField(name, cell_pos))
                        cell_pos = (cell_pos + 1) or 0

                    else: 
                        table_field: FsTableField = match_value
                        table_field.Index = cell_pos or 0
                        add_to_dict(this._fieldNames, name, table_field)
                        cell_pos = (cell_pos + 1) or 0


        else: 
            col_count: int = super().ColumnCount() or 0
            for i in range(1, col_count + 1, 1):
                def predicate(v: FsTableField) -> bool:
                    return v.Index == (i - 1)

                if not exists(predicate, this._fieldNames.values()):
                    name_1: str = "Column" + int32_to_string(i)
                    add_to_dict(this._fieldNames, name_1, FsTableField(name_1, i - 1))




FsTable_reflection = _expr218

def FsTable__ctor_3B894C50(name: str, range_address: FsRangeAddress, show_totals_row: bool | None=None, show_header_row: bool | None=None, field_names: IEnumerable_1[str] | None=None) -> FsTable:
    return FsTable(name, range_address, show_totals_row, show_header_row, field_names)


__all__ = ["FsTable_reflection"]


from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.array_ import (remove_in_place, add_range_in_place)
from ..fable_library.list import (iterate as iterate_1, FSharpList)
from ..fable_library.map import (of_seq, try_find as try_find_1)
from ..fable_library.option import (default_arg, value as value_3)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (map, sort_by, head, last, iterate, try_find, find, exists, filter, max_by, empty)
from ..fable_library.seq2 import group_by
from ..fable_library.string_ import (to_fail, printf, to_console)
from ..fable_library.types import Array
from ..fable_library.util import (compare_primitives, IEnumerable_1, number_hash, ignore, get_enumerator, dispose, equals, safe_hash, clear)
from .Cells.fs_cell import FsCell
from .Cells.fs_cells_collection import FsCellsCollection
from .fs_address import FsAddress
from .fs_column import FsColumn
from .fs_row import FsRow
from .Ranges.fs_range_address import FsRangeAddress
from .Tables.fs_table import FsTable

__B = TypeVar("__B")

def _expr240() -> TypeInfo:
    return class_type("FsSpreadsheet.FsWorksheet", None, FsWorksheet)


class FsWorksheet:
    def __init__(self, name: str, fs_rows: Array[FsRow] | None=None, fs_tables: Array[FsTable] | None=None, fs_cells_collection: FsCellsCollection | None=None) -> None:
        self.name: str = name
        self._name: str = self.name
        self._rows: Array[FsRow] = default_arg(fs_rows, [])
        self._tables: Array[FsTable] = default_arg(fs_tables, [])
        self._cells: FsCellsCollection = default_arg(fs_cells_collection, FsCellsCollection())

    @staticmethod
    def init(name: str) -> FsWorksheet:
        return FsWorksheet(name, [], [], FsCellsCollection())

    @property
    def Name(self, __unit: None=None) -> str:
        self_1: FsWorksheet = self
        return self_1._name

    @Name.setter
    def Name(self, name: str) -> None:
        self_1: FsWorksheet = self
        self_1._name = name

    @property
    def CellCollection(self, __unit: None=None) -> FsCellsCollection:
        self_1: FsWorksheet = self
        return self_1._cells

    @property
    def Tables(self, __unit: None=None) -> Array[FsTable]:
        self_1: FsWorksheet = self
        return self_1._tables

    @property
    def Rows(self, __unit: None=None) -> Array[FsRow]:
        self_1: FsWorksheet = self
        return self_1._rows

    @property
    def Columns(self, __unit: None=None) -> IEnumerable_1[FsColumn]:
        self_1: FsWorksheet = self
        def mapping(tupled_arg: tuple[int, IEnumerable_1[FsCell]]) -> FsColumn:
            column_index: int = tupled_arg[0] or 0
            def _arrow226(__unit: None=None, tupled_arg: Any=tupled_arg) -> FsRangeAddress:
                tupled_arg_1: tuple[FsAddress, FsAddress]
                def projection_1(c_1: FsCell) -> int:
                    return c_1.RowNumber

                class ObjectExpr223:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                cells_1: IEnumerable_1[FsCell] = sort_by(projection_1, tupled_arg[1], ObjectExpr223())
                def _arrow224(__unit: None=None) -> int:
                    c_2: FsCell = head(cells_1)
                    return c_2.RowNumber

                def _arrow225(__unit: None=None) -> int:
                    c_3: FsCell = last(cells_1)
                    return c_3.RowNumber

                tupled_arg_1 = (FsAddress(_arrow224(), column_index), FsAddress(_arrow225(), column_index))
                return FsRangeAddress(tupled_arg_1[0], tupled_arg_1[1])

            return FsColumn(_arrow226(), self_1.CellCollection)

        def projection(c: FsCell) -> int:
            return c.ColumnNumber

        class ObjectExpr228:
            @property
            def Equals(self) -> Callable[[int, int], bool]:
                def _arrow227(x: int, y: int) -> bool:
                    return x == y

                return _arrow227

            @property
            def GetHashCode(self) -> Callable[[int], int]:
                return number_hash

        return map(mapping, group_by(projection, self_1._cells.GetCells(), ObjectExpr228()))

    @property
    def MaxRowIndex(self, __unit: None=None) -> int:
        this: FsWorksheet = self
        return this.CellCollection.MaxRowNumber

    @property
    def MaxColumnIndex(self, __unit: None=None) -> int:
        this: FsWorksheet = self
        return this.CellCollection.MaxColumnNumber

    def Copy(self, __unit: None=None) -> FsWorksheet:
        self_1: FsWorksheet = self
        fcc: FsCellsCollection = self_1.CellCollection.Copy()
        def _arrow229(__unit: None=None) -> Array[FsRow]:
            n: Array[FsRow] = []
            def action(r: FsRow) -> None:
                item: FsRow = r.Copy()
                (n.append(item))

            iterate(action, self_1.Rows)
            return n

        def _arrow230(__unit: None=None) -> Array[FsTable]:
            n_1: Array[FsTable] = []
            def action_1(t: FsTable) -> None:
                item_1: FsTable = t.Copy()
                (n_1.append(item_1))

            iterate(action_1, self_1.Tables)
            return n_1

        return FsWorksheet(self_1.Name, _arrow229(), _arrow230(), fcc)

    @staticmethod
    def copy(sheet: FsWorksheet) -> FsWorksheet:
        return sheet.Copy()

    def Row(self, row_index: int, SkipSearch: bool | None=None) -> FsRow:
        self_1: FsWorksheet = self
        if default_arg(SkipSearch, False):
            row: FsRow = FsRow.create_at(row_index, self_1.CellCollection)
            (self_1._rows.append(row))
            return row

        else: 
            def predicate(row_1: FsRow) -> bool:
                return row_1.Index == row_index

            match_value: FsRow | None = try_find(predicate, self_1._rows)
            if match_value is None:
                row_3: FsRow = FsRow.create_at(row_index, self_1.CellCollection)
                (self_1._rows.append(row_3))
                return row_3

            else: 
                return match_value



    def RowWithRange(self, range_address: FsRangeAddress, SkipSearch: bool | None=None) -> FsRow:
        self_1: FsWorksheet = self
        skip_search: bool = default_arg(SkipSearch, False)
        if range_address.FirstAddress.RowNumber != range_address.LastAddress.RowNumber:
            to_fail(printf("Row may not have a range address spanning over different row indices"))

        if skip_search:
            row: FsRow = FsRow(range_address, self_1.CellCollection)
            row.RangeAddress = range_address
            (self_1._rows.append(row))
            return row

        else: 
            row_1: FsRow = self_1.Row(range_address.FirstAddress.RowNumber)
            row_1.RangeAddress = range_address
            return row_1


    @staticmethod
    def append_row(row: FsRow, sheet: FsWorksheet) -> FsWorksheet:
        ignore(sheet.Row(row.Index))
        return sheet

    @staticmethod
    def get_rows(sheet: FsWorksheet) -> Array[FsRow]:
        return sheet.Rows

    @staticmethod
    def get_row_at(row_index: int, sheet: FsWorksheet) -> FsRow:
        def predicate(arg: FsRow) -> bool:
            return row_index == FsRow.get_index(arg)

        return find(predicate, FsWorksheet.get_rows(sheet))

    @staticmethod
    def try_get_row_at(row_index: int, sheet: FsWorksheet) -> FsRow | None:
        def predicate(arg: FsRow) -> bool:
            return row_index == FsRow.get_index(arg)

        return try_find(predicate, sheet.Rows)

    @staticmethod
    def try_get_row_after(row_index: int, sheet: FsWorksheet) -> FsRow | None:
        def predicate(r: FsRow) -> bool:
            return r.Index >= row_index

        return try_find(predicate, sheet.Rows)

    def InsertBefore(self, row: FsRow, ref_row: FsRow) -> FsWorksheet:
        self_1: FsWorksheet = self
        enumerator: Any = get_enumerator(self_1._rows)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                row_1: FsRow = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                if row_1.Index >= ref_row.Index:
                    row_1.Index = (row_1.Index + 1) or 0


        finally: 
            dispose(enumerator)

        ignore(self_1.Row(row.Index))
        return self_1

    @staticmethod
    def insert_before(row: FsRow, ref_row: FsRow, sheet: FsWorksheet) -> FsWorksheet:
        return sheet.InsertBefore(row, ref_row)

    def ContainsRowAt(self, row_index: int) -> bool:
        self_1: FsWorksheet = self
        def predicate(t: FsRow) -> bool:
            return t.Index == row_index

        return exists(predicate, self_1.Rows)

    @staticmethod
    def contains_row_at(row_index: int, sheet: FsWorksheet) -> bool:
        return sheet.ContainsRowAt(row_index)

    @staticmethod
    def count_rows(sheet: FsWorksheet) -> int:
        return len(sheet.Rows)

    def RemoveRowAt(self, row_index: int) -> None:
        self_1: FsWorksheet = self
        def predicate(r: FsRow) -> bool:
            return r.Index == row_index

        with get_enumerator(filter(predicate, self_1._rows)) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                class ObjectExpr231:
                    @property
                    def Equals(self) -> Callable[[FsRow, FsRow], bool]:
                        return equals

                    @property
                    def GetHashCode(self) -> Callable[[FsRow], int]:
                        return safe_hash

                ignore(remove_in_place(enumerator.System_Collections_Generic_IEnumerator_1_get_Current(), self_1._rows, ObjectExpr231()))

    @staticmethod
    def remove_row_at(row_index: int, sheet: FsWorksheet) -> FsWorksheet:
        sheet.RemoveRowAt(row_index)
        return sheet

    def TryRemoveAt(self, row_index: int) -> FsWorksheet:
        self_1: FsWorksheet = self
        if self_1.ContainsRowAt(row_index):
            self_1.RemoveRowAt(row_index)

        return self_1

    @staticmethod
    def try_remove_at(row_index: int, sheet: FsWorksheet) -> None:
        if FsWorksheet.contains_row_at(row_index, sheet):
            sheet.RemoveRowAt(row_index)


    def SortRows(self, __unit: None=None) -> None:
        self_1: FsWorksheet = self
        def projection(r: FsRow) -> int:
            return r.Index

        class ObjectExpr232:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        sorted: Array[FsRow] = list(sort_by(projection, self_1._rows, ObjectExpr232()))
        clear(self_1._rows)
        add_range_in_place(sorted, self_1._rows)

    def MapRowsInPlace(self, f: Callable[[FsRow], FsRow]) -> FsWorksheet:
        self_1: FsWorksheet = self
        for i in range(0, (len(self_1._rows) - 1) + 1, 1):
            r: FsRow = self_1._rows[i]
            self_1._rows[i] = f(r)
        return self_1

    @staticmethod
    def map_rows_in_place(f: Callable[[FsRow], FsRow], sheet: FsWorksheet) -> FsWorksheet:
        return sheet.MapRowsInPlace(f)

    def GetMaxRowIndex(self, __unit: None=None) -> FsRow:
        self_1: FsWorksheet = self
        if len(self_1.Rows) == 0:
            raise Exception("The FsWorksheet has no FsRows.")

        def projection(r: FsRow) -> int:
            return r.Index

        class ObjectExpr233:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        return max_by(projection, self_1.Rows, ObjectExpr233())

    @staticmethod
    def get_max_row_index(sheet: FsWorksheet) -> FsRow:
        return sheet.GetMaxRowIndex()

    def GetRowValuesAt(self, row_index: int) -> IEnumerable_1[Any]:
        self_1: FsWorksheet = self
        def mapping(c: FsCell) -> Any:
            return c.Value

        return map(mapping, self_1.Row(row_index).Cells) if self_1.ContainsRowAt(row_index) else empty()

    @staticmethod
    def get_row_values_at(row_index: int, sheet: FsWorksheet) -> IEnumerable_1[Any]:
        return sheet.GetRowValuesAt(row_index)

    def TryGetRowValuesAt(self, row_index: int) -> IEnumerable_1[Any] | None:
        self_1: FsWorksheet = self
        return self_1.GetRowValuesAt(row_index) if self_1.ContainsRowAt(row_index) else None

    @staticmethod
    def try_get_row_values_at(row_index: int, sheet: FsWorksheet) -> IEnumerable_1[Any] | None:
        return sheet.TryGetRowValuesAt(row_index)

    def RescanRows(self, __unit: None=None) -> None:
        self_1: FsWorksheet = self
        def mapping(r: FsRow) -> tuple[int, FsRow]:
            return (r.Index, r)

        class ObjectExpr234:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        rows: Any = of_seq(map(mapping, self_1._rows), ObjectExpr234())
        def action_1(tupled_arg: tuple[int, IEnumerable_1[FsCell]]) -> None:
            row_index: int = tupled_arg[0] or 0
            min: int = 1
            max: int = 1
            def action(c_1: FsCell, tupled_arg: Any=tupled_arg) -> None:
                nonlocal min, max
                cn: int = c_1.ColumnNumber or 0
                if cn < min:
                    min = cn or 0

                if cn > max:
                    max = cn or 0


            iterate(action, tupled_arg[1])
            new_range: FsRangeAddress = FsRangeAddress(FsAddress(row_index, min), FsAddress(row_index, max))
            match_value: FsRow | None = try_find_1(row_index, rows)
            if match_value is None:
                ignore(self_1.RowWithRange(new_range, True))

            else: 
                row: FsRow = match_value
                row.RangeAddress = new_range


        def projection(c: FsCell) -> int:
            return c.RowNumber

        class ObjectExpr236:
            @property
            def Equals(self) -> Callable[[int, int], bool]:
                def _arrow235(x_1: int, y_1: int) -> bool:
                    return x_1 == y_1

                return _arrow235

            @property
            def GetHashCode(self) -> Callable[[int], int]:
                return number_hash

        iterate(action_1, group_by(projection, self_1._cells.GetCells(), ObjectExpr236()))

    def Column(self, column_index: int) -> FsColumn:
        self_1: FsWorksheet = self
        return FsColumn.create_at(column_index, self_1.CellCollection)

    def ColumnWithRange(self, range_address: FsRangeAddress) -> None:
        self_1: FsWorksheet = self
        if range_address.FirstAddress.ColumnNumber != range_address.LastAddress.ColumnNumber:
            to_fail(printf("Column may not have a range address spanning over different column indices"))

        self_1.Column(range_address.FirstAddress.ColumnNumber).RangeAddress = range_address

    @staticmethod
    def get_columns(sheet: FsWorksheet) -> IEnumerable_1[FsColumn]:
        return sheet.Columns

    @staticmethod
    def get_column_at(column_index: int, sheet: FsWorksheet) -> FsColumn:
        def predicate(arg: FsColumn) -> bool:
            return column_index == FsColumn.get_index(arg)

        return find(predicate, FsWorksheet.get_columns(sheet))

    @staticmethod
    def try_get_column_at(column_index: int, sheet: FsWorksheet) -> FsColumn | None:
        def predicate(arg: FsColumn) -> bool:
            return column_index == FsColumn.get_index(arg)

        return try_find(predicate, sheet.Columns)

    def Table(self, table_name: str, range_address: FsRangeAddress, show_header_row: bool | None=None) -> FsTable:
        self_1: FsWorksheet = self
        show_header_row_1: bool = default_arg(show_header_row, True)
        def predicate(table: FsTable) -> bool:
            return table.Name == self_1.name

        match_value: FsTable | None = try_find(predicate, self_1._tables)
        if match_value is None:
            table_2: FsTable = FsTable(table_name, range_address, show_header_row_1)
            (self_1._tables.append(table_2))
            return table_2

        else: 
            return match_value


    @staticmethod
    def try_get_table_by_name(table_name: str, sheet: FsWorksheet) -> FsTable | None:
        def predicate(t: FsTable) -> bool:
            return t.Name == table_name

        return try_find(predicate, sheet.Tables)

    @staticmethod
    def get_table_by_name(table_name: str, sheet: FsWorksheet) -> FsTable:
        try: 
            def predicate(t: FsTable) -> bool:
                return t.Name == table_name

            return value_3(try_find(predicate, sheet.Tables))

        except Exception as match_value:
            raise Exception(((("FsTable with name " + table_name) + " is not presen in the FsWorksheet ") + sheet.Name) + ".")


    def AddTable(self, table: FsTable) -> FsWorksheet:
        self_1: FsWorksheet = self
        def predicate(t: FsTable) -> bool:
            return t.Name == table.Name

        if exists(predicate, self_1.Tables):
            to_console(((("FsTable " + table.Name) + " could not be appended as an FsTable with this name is already present in the FsWorksheet ") + self_1.Name) + ".")

        else: 
            (self_1._tables.append(table))

        return self_1

    @staticmethod
    def add_table(table: FsTable, sheet: FsWorksheet) -> FsWorksheet:
        return sheet.AddTable(table)

    def AddTables(self, tables: FSharpList[Any]) -> FsWorksheet:
        self_1: FsWorksheet = self
        def action(arg: __B | None=None) -> None:
            ignore(self_1.AddTable(arg))

        iterate_1(action, tables)
        return self_1

    @staticmethod
    def add_tables(tables: FSharpList[Any], sheet: FsWorksheet) -> FsWorksheet:
        return sheet.AddTables(tables)

    def TryGetCellAt(self, row_index: int, col_index: int) -> FsCell | None:
        self_1: FsWorksheet = self
        return self_1.CellCollection.TryGetCell(row_index, col_index)

    @staticmethod
    def try_get_cell_at(row_index: int, col_index: int, sheet: FsWorksheet) -> FsCell | None:
        return sheet.TryGetCellAt(row_index, col_index)

    def GetCellAt(self, row_index: int, col_index: int) -> FsCell:
        self_1: FsWorksheet = self
        return value_3(self_1.TryGetCellAt(row_index, col_index))

    @staticmethod
    def get_cell_at(row_index: int, col_index: int, sheet: FsWorksheet) -> FsCell:
        return sheet.GetCellAt(row_index, col_index)

    def AddCell(self, cell: FsCell) -> FsWorksheet:
        self_1: FsWorksheet = self
        value: None = self_1.CellCollection.Add(cell)
        ignore(None)
        return self_1

    def AddCells(self, cells: IEnumerable_1[FsCell]) -> FsWorksheet:
        self_1: FsWorksheet = self
        value: None = self_1.CellCollection.AddMany(cells)
        ignore(None)
        return self_1

    def InsertValueAt(self, value: Any, row_index: int, col_index: int) -> None:
        self_1: FsWorksheet = self
        cell: FsCell = FsCell(value)
        self_1.CellCollection.Add(cell, row_index, col_index)

    @staticmethod
    def insert_value_at(value: Any, row_index: int, col_index: int, sheet: FsWorksheet) -> None:
        sheet.InsertValueAt(value, row_index, col_index)

    def SetValueAt(self, value: Any, row_index: int, col_index: int) -> FsWorksheet:
        self_1: FsWorksheet = self
        match_value: FsCell | None = self_1.CellCollection.TryGetCell(row_index, col_index)
        if match_value is None:
            value_2: None = self_1.CellCollection.Add(value, row_index, col_index)
            ignore(None)
            return self_1

        else: 
            c: FsCell = match_value
            value_1: None = c.SetValueAs(value)
            ignore(None)
            return self_1


    @staticmethod
    def set_value_at(value: Any, row_index: int, col_index: int, sheet: FsWorksheet) -> FsWorksheet:
        return sheet.SetValueAt(value, row_index, col_index)

    def RemoveCellAt(self, row_index: int, col_index: int) -> FsWorksheet:
        self_1: FsWorksheet = self
        self_1.CellCollection.RemoveCellAt(row_index, col_index)
        return self_1

    @staticmethod
    def remove_cell_at(row_index: int, col_index: int, sheet: FsWorksheet) -> FsWorksheet:
        return sheet.RemoveCellAt(row_index, col_index)

    def TryRemoveValueAt(self, row_index: int, col_index: int) -> None:
        self_1: FsWorksheet = self
        self_1.CellCollection.TryRemoveValueAt(row_index, col_index)

    @staticmethod
    def try_remove_value_at(row_index: int, col_index: int, sheet: FsWorksheet) -> None:
        sheet.TryRemoveValueAt(row_index, col_index)

    def RemoveValueAt(self, row_index: int, col_index: int) -> None:
        self_1: FsWorksheet = self
        self_1.CellCollection.RemoveValueAt(row_index, col_index)

    @staticmethod
    def remove_value_at(row_index: int, col_index: int, sheet: FsWorksheet) -> None:
        sheet.RemoveValueAt(row_index, col_index)

    @staticmethod
    def add_cell(cell: FsCell, sheet: FsWorksheet) -> FsWorksheet:
        return sheet.AddCell(cell)

    @staticmethod
    def add_cells(cell: IEnumerable_1[FsCell], sheet: FsWorksheet) -> FsWorksheet:
        return sheet.AddCells(cell)

    @staticmethod
    def validate_for_write(ws: FsWorksheet) -> None:
        try: 
            def action(t: FsTable) -> None:
                cells_collection: FsCellsCollection = ws.CellCollection
                FsTable.validate_for_write(t, cells_collection)

            iterate(action, ws.Tables)

        except Exception as ex:
            arg: str = ws.Name
            arg_1: str = str(ex)
            to_fail(printf("FsWorksheet %s could not be validated for writing to xlsx file. %s"))(arg)(arg_1)



FsWorksheet_reflection = _expr240

def FsWorksheet__ctor_7FDA5F7A(name: str, fs_rows: Array[FsRow] | None=None, fs_tables: Array[FsTable] | None=None, fs_cells_collection: FsCellsCollection | None=None) -> FsWorksheet:
    return FsWorksheet(name, fs_rows, fs_tables, fs_cells_collection)


__all__ = ["FsWorksheet_reflection"]


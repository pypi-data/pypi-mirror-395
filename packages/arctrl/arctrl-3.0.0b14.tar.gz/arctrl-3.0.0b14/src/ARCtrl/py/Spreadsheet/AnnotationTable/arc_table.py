from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import (map as map_1, unzip)
from ...fable_modules.fable_library.list import (reverse, map, FSharpList, fold, singleton, cons, is_empty, head, tail, empty, of_array, to_array, exists, collect as collect_1, sort_by, of_seq, length, iterate_indexed)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.reflection import enum_type
from ...fable_modules.fable_library.seq import (try_find, to_array as to_array_1, delay, map as map_2, collect, singleton as singleton_1, fold as fold_1)
from ...fable_modules.fable_library.string_ import (starts_with_exact, to_fail, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, compare_primitives, max)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from ...fable_modules.fs_spreadsheet.fs_address import FsAddress
from ...fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress
from ...fable_modules.fs_spreadsheet.Tables.fs_table import FsTable
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.arc_table_aux import (ColumnValueRefs, ArcTableValues)
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.composite_header import CompositeHeader
from .composite_column import (from_string_cell_columns, ColumnValueRefs_fromStringCellColumns, fix_deprecated_ioheader, to_string_cell_columns)

__A = TypeVar("__A")

def Aux_List_groupWhen(f: Callable[[__A], bool], list_1: FSharpList[Any]) -> FSharpList[FSharpList[Any]]:
    def mapping(list_3: FSharpList[__A], f: Any=f, list_1: Any=list_1) -> FSharpList[__A]:
        return reverse(list_3)

    def folder(acc: FSharpList[FSharpList[__A]], e: __A, f: Any=f, list_1: Any=list_1) -> FSharpList[FSharpList[__A]]:
        match_value: bool = f(e)
        if match_value:
            return cons(singleton(e), acc)

        elif not is_empty(acc):
            return cons(cons(e, head(acc)), tail(acc))

        else: 
            return singleton(singleton(e))


    return reverse(map(mapping, fold(folder, empty(), list_1)))


def classify_header_order(header: CompositeHeader) -> enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]):
    if ((((((header.tag == 4) or (header.tag == 5)) or (header.tag == 6)) or (header.tag == 7)) or (header.tag == 8)) or (header.tag == 9)) or (header.tag == 10):
        return 2

    elif (((((header.tag == 0) or (header.tag == 1)) or (header.tag == 2)) or (header.tag == 3)) or (header.tag == 14)) or (header.tag == 13):
        return 3

    elif header.tag == 12:
        return 4

    else: 
        return 1



def classify_column_order(column: CompositeColumn) -> enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]):
    return classify_header_order(column.Header)


helper_column_strings: FSharpList[str] = of_array(["Term Source REF", "Term Accession Number", "Unit", "Data Format", "Data Selector Format"])

def group_columns_by_header(string_cell_columns: Array[Array[str]]) -> Array[Array[Array[str]]]:
    def mapping(list_4: FSharpList[Array[str]], string_cell_columns: Any=string_cell_columns) -> Array[Array[str]]:
        return to_array(list_4)

    def f(c: Array[str], string_cell_columns: Any=string_cell_columns) -> bool:
        v: str = c[0]
        def predicate(s: str, c: Any=c) -> bool:
            return starts_with_exact(v, s)

        return not exists(predicate, helper_column_strings)

    return map_1(mapping, to_array(Aux_List_groupWhen(f, of_array(string_cell_columns))), None)


def try_annotation_table(sheet: FsWorksheet) -> FsTable | None:
    def predicate(t: FsTable, sheet: Any=sheet) -> bool:
        return starts_with_exact(t.Name, "annotationTable")

    return try_find(predicate, sheet.Tables)


def compose_columns(string_cell_columns: Array[Array[str]]) -> Array[CompositeColumn]:
    def _arrow1537(columns: Array[Array[str]], string_cell_columns: Any=string_cell_columns) -> CompositeColumn:
        return from_string_cell_columns(columns)

    return map_1(_arrow1537, group_columns_by_header(string_cell_columns), None)


def compose_arc_table_values(string_cell_columns: Array[Array[str]]) -> tuple[Array[CompositeHeader], ArcTableValues]:
    value_map: Any = dict([])
    row_count: int = (len(string_cell_columns[0]) - 1) or 0
    def mapping(columns: Array[Array[str]], string_cell_columns: Any=string_cell_columns) -> tuple[CompositeHeader, ColumnValueRefs]:
        return ColumnValueRefs_fromStringCellColumns(value_map, columns)

    pattern_input: tuple[Array[CompositeHeader], Array[ColumnValueRefs]] = unzip(map_1(mapping, group_columns_by_header(string_cell_columns), None))
    return (pattern_input[0], ArcTableValues.from_ref_columns(pattern_input[1], value_map, row_count))


def try_from_fs_worksheet(sheet: FsWorksheet) -> ArcTable | None:
    try: 
        match_value: FsTable | None = try_annotation_table(sheet)
        if match_value is None:
            return None

        else: 
            t: FsTable = match_value
            def _arrow1541(__unit: None=None) -> IEnumerable_1[Array[str]]:
                def _arrow1540(c: int) -> Array[str]:
                    def _arrow1539(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow1538(r: int) -> IEnumerable_1[str]:
                            match_value_1: FsCell | None = sheet.CellCollection.TryGetCell(r, c)
                            if match_value_1 is None:
                                return singleton_1("")

                            else: 
                                cell: FsCell = match_value_1
                                return singleton_1(cell.ValueAsString())


                        return collect(_arrow1538, range_big_int(1, 1, t.RangeAddress.LastAddress.RowNumber))

                    return to_array_1(delay(_arrow1539))

                return map_2(_arrow1540, range_big_int(1, 1, t.RangeAddress.LastAddress.ColumnNumber))

            pattern_input: tuple[Array[CompositeHeader], ArcTableValues] = compose_arc_table_values(map_1(fix_deprecated_ioheader, to_array_1(delay(_arrow1541)), None))
            return ArcTable.from_arc_table_values(sheet.Name, list(pattern_input[0]), pattern_input[1])


    except Exception as err:
        arg: str = sheet.Name
        arg_1: str = str(err)
        return to_fail(printf("Could not parse table with name \"%s\":\n%s"))(arg)(arg_1)



def to_fs_worksheet(index: int | None, table: ArcTable) -> FsWorksheet:
    string_count: Any = dict([])
    ws: FsWorksheet = FsWorksheet(table.Name)
    if table.ColumnCount == 0:
        return ws

    else: 
        def _arrow1542(column_1: CompositeColumn, index: Any=index, table: Any=table) -> FSharpList[FSharpList[str]]:
            return to_string_cell_columns(column_1)

        def _arrow1543(column: CompositeColumn, index: Any=index, table: Any=table) -> enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]):
            return classify_column_order(column)

        class ObjectExpr1544:
            @property
            def Compare(self) -> Callable[[enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)]), enum_type("ARCtrl.Spreadsheet.ArcTable.ColumnOrder", int, [("InputClass", 1.0), ("ProtocolClass", 2.0), ("ParamsClass", 3.0), ("OutputClass", 4.0)])], int]:
                return compare_primitives

        columns: FSharpList[FSharpList[str]] = collect_1(_arrow1542, sort_by(_arrow1543, of_seq(table.Columns), ObjectExpr1544()))
        table_row_count: int
        def folder(acc: int, c: FSharpList[str], index: Any=index, table: Any=table) -> int:
            def _arrow1545(x_1: int, y_1: int, acc: Any=acc, c: Any=c) -> int:
                return compare_primitives(x_1, y_1)

            return max(_arrow1545, acc, length(c))

        max_row: int = fold_1(folder, 0, columns) or 0
        table_row_count = 2 if (max_row == 1) else max_row
        table_column_count: int = length(columns) or 0
        name: str = "annotationTable" if (index is None) else (((("" + "annotationTable") + "") + str(index)) + "")
        fs_table: FsTable = ws.Table(name, FsRangeAddress(FsAddress(1, 1), FsAddress(table_row_count, table_column_count)))
        def action_1(col_i: int, col: FSharpList[str], index: Any=index, table: Any=table) -> None:
            def action(row_i: int, string_cell: str, col_i: Any=col_i, col: Any=col) -> None:
                value: str
                if row_i == 0:
                    match_value: str | None = Dictionary_tryGet(string_cell, string_count)
                    if match_value is None:
                        add_to_dict(string_count, string_cell, "")
                        value = string_cell

                    else: 
                        spaces: str = match_value
                        string_count[string_cell] = spaces + " "
                        value = (string_cell + " ") + spaces


                else: 
                    value = string_cell

                address: FsAddress = FsAddress(row_i + 1, col_i + 1)
                fs_table.Cell(address, ws.CellCollection).SetValueAs(value)

            iterate_indexed(action, col)

        iterate_indexed(action_1, columns)
        return ws



__all__ = ["Aux_List_groupWhen", "classify_header_order", "classify_column_order", "helper_column_strings", "group_columns_by_header", "try_annotation_table", "compose_columns", "compose_arc_table_values", "try_from_fs_worksheet", "to_fs_worksheet"]


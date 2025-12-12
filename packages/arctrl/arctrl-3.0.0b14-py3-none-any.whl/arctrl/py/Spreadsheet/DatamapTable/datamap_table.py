from __future__ import annotations
from typing import Any
from ...fable_modules.fable_library.list import (of_array, FSharpList, exists, iterate, length, head, iterate_indexed)
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (try_find, item, to_array, delay, map, to_list)
from ...fable_modules.fable_library.string_ import (starts_with_exact, to_fail, printf)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, ignore)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.Cells.fs_cells_collection import Dictionary_tryGet
from ...fable_modules.fs_spreadsheet.fs_address import FsAddress
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress
from ...fable_modules.fs_spreadsheet.Tables.fs_table import FsTable
from ...Core.data_context import (DataContext__ctor_Z780A8A2A, DataContext)
from ...Core.datamap import Datamap
from ..AnnotationTable.arc_table import Aux_List_groupWhen
from .datamap_column import (set_from_fs_columns, to_fs_columns)

helper_column_strings: FSharpList[str] = of_array(["Term Source REF", "Term Accession Number", "Data Format", "Data Selector Format"])

def group_columns_by_header(columns: FSharpList[FsColumn]) -> FSharpList[FSharpList[FsColumn]]:
    def f(c: FsColumn, columns: Any=columns) -> bool:
        v: str = c.Item(1).ValueAsString()
        def predicate(s: str, c: Any=c) -> bool:
            return starts_with_exact(v, s)

        return not exists(predicate, helper_column_strings)

    return Aux_List_groupWhen(f, columns)


def try_datamap_table(sheet: FsWorksheet) -> FsTable | None:
    def predicate(t: FsTable, sheet: Any=sheet) -> bool:
        return starts_with_exact(t.Name, "datamapTable")

    return try_find(predicate, sheet.Tables)


def compose_columns(columns: IEnumerable_1[FsColumn]) -> Array[DataContext]:
    l: int = (item(0, columns).MaxRowIndex - 1) or 0
    def _arrow1586(__unit: None=None, columns: Any=columns) -> IEnumerable_1[DataContext]:
        def _arrow1585(i: int) -> DataContext:
            return DataContext__ctor_Z780A8A2A()

        return map(_arrow1585, range_big_int(0, 1, l - 1))

    dc: Array[DataContext] = list(to_array(delay(_arrow1586)))
    def action(arg: FSharpList[FsColumn], columns: Any=columns) -> None:
        ignore(set_from_fs_columns(dc, arg))

    iterate(action, group_columns_by_header(to_list(columns)))
    return dc


def try_from_fs_worksheet(sheet: FsWorksheet) -> Datamap | None:
    try: 
        match_value: FsTable | None = try_datamap_table(sheet)
        if match_value is None:
            return None

        else: 
            t: FsTable = match_value
            return Datamap(compose_columns(t.GetColumns(sheet.CellCollection)))


    except Exception as err:
        arg: str = sheet.Name
        arg_1: str = str(err)
        return to_fail(printf("Could not parse datamap table with name \"%s\":\n%s"))(arg)(arg_1)



def to_fs_worksheet(table: Datamap) -> FsWorksheet:
    string_count: Any = dict([])
    ws: FsWorksheet = FsWorksheet("isa_datamap")
    if len(table.DataContexts) == 0:
        return ws

    else: 
        columns: FSharpList[FSharpList[FsCell]] = to_fs_columns(table.DataContexts)
        max_row: int = length(head(columns)) or 0
        max_col: int = length(columns) or 0
        fs_table: FsTable = ws.Table("datamapTable", FsRangeAddress(FsAddress(1, 1), FsAddress(max_row, max_col)))
        def action_1(col_i: int, col: FSharpList[FsCell], table: Any=table) -> None:
            def action(row_i: int, cell: FsCell, col_i: Any=col_i, col: Any=col) -> None:
                value: str
                v: str = cell.ValueAsString()
                if row_i == 0:
                    match_value: str | None = Dictionary_tryGet(v, string_count)
                    if match_value is None:
                        add_to_dict(string_count, cell.ValueAsString(), "")
                        value = v

                    else: 
                        spaces: str = match_value
                        string_count[v] = spaces + " "
                        value = (v + " ") + spaces


                else: 
                    value = v

                address: FsAddress = FsAddress(row_i + 1, col_i + 1)
                fs_table.Cell(address, ws.CellCollection).SetValueAs(value)

            iterate_indexed(action, col)

        iterate_indexed(action_1, columns)
        ws.RescanRows()
        return ws



__all__ = ["helper_column_strings", "group_columns_by_header", "try_datamap_table", "compose_columns", "try_from_fs_worksheet", "to_fs_worksheet"]


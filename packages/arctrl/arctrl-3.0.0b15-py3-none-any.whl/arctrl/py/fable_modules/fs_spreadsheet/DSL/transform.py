from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (is_empty, head, cons, tail as tail_25, singleton, reverse, empty, of_array_with_tail, FSharpList, iterate, iterate_indexed, map, transpose, choose)
from ...fable_library.seq import max
from ...fable_library.set import (of_seq, FSharpSet__Contains, add)
from ...fable_library.string_ import (to_fail, printf, to_text)
from ...fable_library.types import to_string
from ...fable_library.util import (compare_primitives, ignore)
from ..Cells.fs_cell import (FsCell, DataType)
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import FsAddress
from ..fs_row import FsRow
from ..fs_workbook import FsWorkbook
from ..fs_worksheet import FsWorksheet
from ..Ranges.fs_range_address import FsRangeAddress
from ..Tables.fs_table import FsTable
from ..Tables.fs_table_field import FsTableField
from .types import (SheetElement, TableElement__get_IsColumn, ColumnElement, TableElement, RowElement, ColumnIndex__get_Index, RowIndex__get_Index, RowIndex, WorkbookElement, Workbook)

def split_rows_and_columns(els: FSharpList[SheetElement]) -> FSharpList[tuple[str, FSharpList[SheetElement]]]:
    def loop(in_rows_mut: bool, in_columns_mut: bool, current_mut: FSharpList[SheetElement], remaining_mut: FSharpList[SheetElement], agg_mut: FSharpList[tuple[str, FSharpList[SheetElement]]], els: Any=els) -> FSharpList[tuple[str, FSharpList[SheetElement]]]:
        while True:
            (in_rows, in_columns, current, remaining, agg) = (in_rows_mut, in_columns_mut, current_mut, remaining_mut, agg_mut)
            if not is_empty(remaining):
                if head(remaining).tag == 4:
                    if in_columns:
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = cons(SheetElement(4, head(remaining).fields[0]), current)
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue

                    elif in_rows:
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = singleton(SheetElement(4, head(remaining).fields[0]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = cons(("Rows", reverse(current)), agg)
                        continue

                    else: 
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = singleton(SheetElement(4, head(remaining).fields[0]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue


                elif head(remaining).tag == 3:
                    if in_columns:
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = cons(SheetElement(3, head(remaining).fields[0], head(remaining).fields[1]), current)
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue

                    elif in_rows:
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = singleton(SheetElement(3, head(remaining).fields[0], head(remaining).fields[1]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = cons(("Rows", reverse(current)), agg)
                        continue

                    else: 
                        in_rows_mut = False
                        in_columns_mut = True
                        current_mut = singleton(SheetElement(3, head(remaining).fields[0], head(remaining).fields[1]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue


                elif head(remaining).tag == 2:
                    if in_rows:
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = cons(SheetElement(2, head(remaining).fields[0]), current)
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue

                    elif in_columns:
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = singleton(SheetElement(2, head(remaining).fields[0]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = cons(("Columns", reverse(current)), agg)
                        continue

                    else: 
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = singleton(SheetElement(2, head(remaining).fields[0]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue


                elif head(remaining).tag == 1:
                    if in_rows:
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = cons(SheetElement(1, head(remaining).fields[0], head(remaining).fields[1]), current)
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue

                    elif in_columns:
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = singleton(SheetElement(1, head(remaining).fields[0], head(remaining).fields[1]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = cons(("Columns", reverse(current)), agg)
                        continue

                    else: 
                        in_rows_mut = True
                        in_columns_mut = False
                        current_mut = singleton(SheetElement(1, head(remaining).fields[0], head(remaining).fields[1]))
                        remaining_mut = tail_25(remaining)
                        agg_mut = agg
                        continue


                elif head(remaining).tag == 0:
                    if in_rows:
                        in_rows_mut = False
                        in_columns_mut = False
                        current_mut = empty()
                        remaining_mut = tail_25(remaining)
                        agg_mut = of_array_with_tail([("Table", singleton(SheetElement(0, head(remaining).fields[0], head(remaining).fields[1]))), ("Rows", reverse(current))], agg)
                        continue

                    elif in_columns:
                        in_rows_mut = False
                        in_columns_mut = False
                        current_mut = empty()
                        remaining_mut = tail_25(remaining)
                        agg_mut = of_array_with_tail([("Table", singleton(SheetElement(0, head(remaining).fields[0], head(remaining).fields[1]))), ("Columns", reverse(current))], agg)
                        continue

                    else: 
                        in_rows_mut = False
                        in_columns_mut = False
                        current_mut = empty()
                        remaining_mut = tail_25(remaining)
                        agg_mut = cons(("Table", singleton(SheetElement(0, head(remaining).fields[0], head(remaining).fields[1]))), agg)
                        continue


                else: 
                    raise Exception("Unknown element combination when grouping Sheet elements")


            elif in_rows:
                return cons(("Rows", reverse(current)), agg)

            elif in_columns:
                return cons(("Columns", reverse(current)), agg)

            else: 
                return agg

            break

    return reverse(loop(False, False, empty(), els, empty()))


def FsSpreadsheet_DSL_Workbook__Workbook_parseTable_Static(cell_collection: FsCellsCollection, table: FsTable, els: FSharpList[TableElement]) -> None:
    def action_1(col_2: FSharpList[tuple[DataType, Any]], cell_collection: Any=cell_collection, table: Any=table, els: Any=els) -> None:
        if not is_empty(col_2):
            field: FsTableField = table.Field(to_string(head(col_2)[1]), cell_collection)
            def action(i: int, tupled_arg: tuple[DataType, Any], col_2: Any=col_2) -> None:
                cell_4: FsCell = field.Column.Cell(i + 2, cell_collection)
                cell_4.DataType = tupled_arg[0]
                cell_4.Value = tupled_arg[1]

            iterate_indexed(action, tail_25(col_2))

        else: 
            raise Exception("Empty column")


    def mapping_1(col: TableElement, cell_collection: Any=cell_collection, table: Any=table, els: Any=els) -> FSharpList[tuple[DataType, Any]]:
        if col.tag == 1:
            def mapping(cell: ColumnElement, col: Any=col) -> tuple[DataType, Any]:
                if cell.tag == 1:
                    return cell.fields[0]

                else: 
                    raise Exception("Indexed cells not supported in column transformation")


            return map(mapping, col.fields[0])

        else: 
            raise Exception("Indexed columns not supported in table transformation")


    def mapping_3(row: TableElement, cell_collection: Any=cell_collection, table: Any=table, els: Any=els) -> FSharpList[tuple[DataType, Any]]:
        if row.tag == 0:
            def mapping_2(cell_2: RowElement, row: Any=row) -> tuple[DataType, Any]:
                if cell_2.tag == 1:
                    return cell_2.fields[0]

                else: 
                    raise Exception("Indexed cells not supported in row transformation")


            return map(mapping_2, row.fields[0])

        else: 
            raise Exception("Indexed rows not supported in table transformation")


    iterate(action_1, map(mapping_1, els) if TableElement__get_IsColumn(head(els)) else transpose(map(mapping_3, els)))


def FsSpreadsheet_DSL_Workbook__Workbook_parseRow_Static(cell_collection: FsCellsCollection, row: FsRow, els: FSharpList[RowElement]) -> None:
    def chooser(el: RowElement, cell_collection: Any=cell_collection, row: Any=row, els: Any=els) -> int | None:
        if el.tag == 0:
            return ColumnIndex__get_Index(el.fields[0])

        else: 
            return None


    class ObjectExpr267:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    cell_index_set: Any = of_seq(choose(chooser, els), ObjectExpr267())
    def action(el_1: RowElement, cell_collection: Any=cell_collection, row: Any=row, els: Any=els) -> None:
        if el_1.tag == 1:
            def _arrow268(__unit: None=None, el_1: Any=el_1) -> int:
                nonlocal cell_index_set
                i_1: int = 1
                while FSharpSet__Contains(cell_index_set, i_1):
                    i_1 = (i_1 + 1) or 0
                cell_index_set = add(i_1, cell_index_set)
                return i_1

            cell_1: FsCell = row.Item(_arrow268())
            cell_1.DataType = el_1.fields[0][0]
            cell_1.Value = el_1.fields[0][1]

        else: 
            cell: FsCell = row.Item(ColumnIndex__get_Index(el_1.fields[0]))
            cell.DataType = el_1.fields[1][0]
            cell.Value = el_1.fields[1][1]


    iterate(action, els)


def FsSpreadsheet_DSL_Workbook__Workbook_parseSheet_Static(sheet: FsWorksheet, els: FSharpList[SheetElement]) -> None:
    def chooser(el: SheetElement, sheet: Any=sheet, els: Any=els) -> int | None:
        if el.tag == 1:
            return RowIndex__get_Index(el.fields[0])

        else: 
            return None


    class ObjectExpr269:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    row_index_set: Any = add(0, of_seq(choose(chooser, els), ObjectExpr269()))
    def action_3(_arg: tuple[str, FSharpList[SheetElement]], sheet: Any=sheet, els: Any=els) -> None:
        (pattern_matching_result, l, name, table_elements, l_1, s) = (None, None, None, None, None, None)
        if _arg[0] == "Columns":
            pattern_matching_result = 0
            l = _arg[1]

        elif _arg[0] == "Table":
            if not is_empty(_arg[1]):
                if head(_arg[1]).tag == 0:
                    if is_empty(tail_25(_arg[1])):
                        pattern_matching_result = 1
                        name = head(_arg[1]).fields[0]
                        table_elements = head(_arg[1]).fields[1]

                    else: 
                        pattern_matching_result = 3
                        s = _arg[0]


                else: 
                    pattern_matching_result = 3
                    s = _arg[0]


            else: 
                pattern_matching_result = 3
                s = _arg[0]


        elif _arg[0] == "Rows":
            pattern_matching_result = 2
            l_1 = _arg[1]

        else: 
            pattern_matching_result = 3
            s = _arg[0]

        if pattern_matching_result == 0:
            columns: FSharpList[SheetElement] = l
            class ObjectExpr270:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            base_row_index: int = (1 + max(row_index_set, ObjectExpr270())) or 0
            def chooser_1(col: SheetElement, _arg: Any=_arg) -> int | None:
                if col.tag == 3:
                    return ColumnIndex__get_Index(col.fields[0])

                else: 
                    return None


            class ObjectExpr271:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            column_index_set: Any = of_seq(choose(chooser_1, columns), ObjectExpr271())
            def action_1(col_1: SheetElement, _arg: Any=_arg) -> None:
                pattern_input: tuple[int, FSharpList[ColumnElement]]
                if col_1.tag == 3:
                    pattern_input = (ColumnIndex__get_Index(col_1.fields[0]), col_1.fields[1])

                elif col_1.tag == 4:
                    def _arrow272(__unit: None=None, col_1: Any=col_1) -> int:
                        nonlocal column_index_set
                        i_3: int = 1
                        while FSharpSet__Contains(column_index_set, i_3):
                            i_3 = (i_3 + 1) or 0
                        column_index_set = add(i_3, column_index_set)
                        return i_3

                    pattern_input = (_arrow272(), col_1.fields[0])

                else: 
                    raise Exception("Expected column elements")

                elements_2: FSharpList[ColumnElement] = pattern_input[1]
                col_i: int = pattern_input[0] or 0
                def chooser_2(el_1: ColumnElement, col_1: Any=col_1) -> int | None:
                    if el_1.tag == 0:
                        return RowIndex__get_Index(el_1.fields[0])

                    else: 
                        return None


                class ObjectExpr273:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                cell_index_set: Any = of_seq(choose(chooser_2, elements_2), ObjectExpr273())
                def action(el_2: ColumnElement, col_1: Any=col_1) -> None:
                    nonlocal row_index_set
                    if el_2.tag == 1:
                        def _arrow274(__unit: None=None, el_2: Any=el_2) -> int:
                            nonlocal cell_index_set
                            i_6: int = 1
                            while FSharpSet__Contains(cell_index_set, i_6):
                                i_6 = (i_6 + 1) or 0
                            cell_index_set = add(i_6, cell_index_set)
                            return i_6

                        row_1: FsRow = sheet.Row((_arrow274() + base_row_index) - 1)
                        row_index_set = add(row_1.Index, row_index_set)
                        cell_1: FsCell = row_1.Item(col_i)
                        cell_1.DataType = el_2.fields[0][0]
                        cell_1.Value = el_2.fields[0][1]

                    else: 
                        i_7: RowIndex = el_2.fields[0]
                        row: FsRow = sheet.Row((RowIndex__get_Index(i_7) + base_row_index) - 1)
                        row_index_set = add(RowIndex__get_Index(i_7), row_index_set)
                        cell: FsCell = row.Item(col_i)
                        cell.DataType = el_2.fields[1][0]
                        cell.Value = el_2.fields[1][1]


                iterate(action, elements_2)

            iterate(action_1, columns)

        elif pattern_matching_result == 1:
            max_row: int = (sheet.CellCollection.MaxRowNumber + 1) or 0
            range: FsRangeAddress = FsRangeAddress(FsAddress(max_row, 1), FsAddress(max_row, 1))
            table: FsTable = sheet.Table(name, range)
            FsSpreadsheet_DSL_Workbook__Workbook_parseTable_Static(sheet.CellCollection, table, table_elements)

        elif pattern_matching_result == 2:
            def action_2(_arg_1: SheetElement, _arg: Any=_arg) -> None:
                if _arg_1.tag == 1:
                    row_2: FsRow = sheet.Row(RowIndex__get_Index(_arg_1.fields[0]))
                    FsSpreadsheet_DSL_Workbook__Workbook_parseRow_Static(sheet.CellCollection, row_2, _arg_1.fields[1])

                elif _arg_1.tag == 2:
                    def _arrow275(__unit: None=None, _arg_1: Any=_arg_1) -> int:
                        nonlocal row_index_set
                        i_1: int = 1
                        while FSharpSet__Contains(row_index_set, i_1):
                            i_1 = (i_1 + 1) or 0
                        row_index_set = add(i_1, row_index_set)
                        return i_1

                    row_4: FsRow = sheet.Row(_arrow275())
                    FsSpreadsheet_DSL_Workbook__Workbook_parseRow_Static(sheet.CellCollection, row_4, _arg_1.fields[0])

                else: 
                    raise Exception("Expected row elements")


            iterate(action_2, l_1)

        elif pattern_matching_result == 3:
            to_fail(printf("Invalid sheet element %s"))(s)


    iterate(action_3, split_rows_and_columns(els))


def FsSpreadsheet_DSL_Workbook__Workbook_Parse(self_1: Workbook) -> FsWorkbook:
    workbook: FsWorkbook = FsWorkbook()
    def action(i: int, wb_el: WorkbookElement, self_1: Any=self_1) -> None:
        if wb_el.tag == 1:
            worksheet_1: FsWorksheet = FsWorksheet(wb_el.fields[0])
            FsSpreadsheet_DSL_Workbook__Workbook_parseSheet_Static(worksheet_1, wb_el.fields[1])
            value_1: None = workbook.AddWorksheet(worksheet_1)
            ignore(None)

        else: 
            def _arrow276(__unit: None=None, i: Any=i, wb_el: Any=wb_el) -> str:
                arg: int = (i + 1) or 0
                return to_text(printf("Sheet%i"))(arg)

            worksheet: FsWorksheet = FsWorksheet(_arrow276())
            FsSpreadsheet_DSL_Workbook__Workbook_parseSheet_Static(worksheet, wb_el.fields[0])
            value: None = workbook.AddWorksheet(worksheet)
            ignore(None)


    iterate_indexed(action, self_1.fields[0])
    return workbook


__all__ = ["split_rows_and_columns", "FsSpreadsheet_DSL_Workbook__Workbook_parseTable_Static", "FsSpreadsheet_DSL_Workbook__Workbook_parseRow_Static", "FsSpreadsheet_DSL_Workbook__Workbook_parseSheet_Static", "FsSpreadsheet_DSL_Workbook__Workbook_Parse"]


from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from ...fable_modules.fable_library.list import (FSharpList, singleton, empty, append, cons, find, exists, initialize as initialize_1, map as map_2)
from ...fable_modules.fable_library.map import (of_seq, try_find)
from ...fable_modules.fable_library.map_util import (get_item_from_dict, add_to_dict)
from ...fable_modules.fable_library.option import (map as map_1, default_arg)
from ...fable_modules.fable_library.reflection import (TypeInfo, string_type, int32_type, tuple_type, class_type, list_type, record_type)
from ...fable_modules.fable_library.seq import (indexed, map, choose, initialize, max_by, try_pick, fold, iterate, is_empty, length as length_1, try_item, delay, append as append_1)
from ...fable_modules.fable_library.string_ import (to_fail, printf)
from ...fable_modules.fable_library.types import (Record, Array)
from ...fable_modules.fable_library.util import (IEnumerable_1, compare_primitives, equals, IEnumerator)
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import (FsCell, DataType)
from ...fable_modules.fs_spreadsheet.DSL.cell_builder import (CellBuilder__AsCellElement_6F87C2ED, CellBuilder__ctor)
from ...fable_modules.fs_spreadsheet.DSL.row_builder import (RowBuilder__ctor, RowBuilder__Combine_19F30600, RowBuilder_get_Empty)
from ...fable_modules.fs_spreadsheet.DSL.types import (SheetEntity_1_some_2B595, Messages_format)
from ...fable_modules.fs_spreadsheet.DSL.row_builder import RowBuilder
from ...fable_modules.fs_spreadsheet.DSL.types import (SheetEntity_1, RowElement, ColumnIndex)
from ...fable_modules.fs_spreadsheet.fs_address import FsAddress
from ...fable_modules.fs_spreadsheet.fs_row import FsRow
from ...fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ...fable_modules.fs_spreadsheet.Ranges.fs_range_address import FsRangeAddress
from ...Core.comment import (Remark, Comment)
from ...Core.Helper.collections_ import Dictionary_init
from ..collection_aux import (Dictionary_tryGetValue, Seq_trySkip)
from .comment import (Remark__007CRemark_007C__007C, Comment__007CComment_007C__007C, Comment_wrapCommentKey)

def SparseRowModule_fromValues(v: IEnumerable_1[str]) -> IEnumerable_1[tuple[int, str]]:
    return indexed(v)


def SparseRowModule_getValues(i: IEnumerable_1[tuple[int, str]]) -> IEnumerable_1[str]:
    def mapping(tuple: tuple[int, str], i: Any=i) -> str:
        return tuple[1]

    return map(mapping, i)


def SparseRowModule_fromAllValues(v: IEnumerable_1[str | None]) -> IEnumerable_1[tuple[int, str]]:
    def chooser(tupled_arg: tuple[int, str | None], v: Any=v) -> tuple[int, str] | None:
        def _arrow1060(v_1: str, tupled_arg: Any=tupled_arg) -> tuple[int, str]:
            return (tupled_arg[0], v_1)

        return map_1(_arrow1060, tupled_arg[1])

    return choose(chooser, indexed(v))


def SparseRowModule_getAllValues(i: IEnumerable_1[tuple[int, str]]) -> IEnumerable_1[str | None]:
    class ObjectExpr1061:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    m: Any = of_seq(i, ObjectExpr1061())
    def projection(tuple: tuple[int, str], i: Any=i) -> int:
        return tuple[0]

    class ObjectExpr1062:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    def _arrow1063(i_1: int, i: Any=i) -> str | None:
        return try_find(i_1, m)

    return initialize(max_by(projection, i, ObjectExpr1062())[0] + 1, _arrow1063)


def SparseRowModule_fromFsRow(r: FsRow) -> IEnumerable_1[tuple[int, str]]:
    def chooser(c: FsCell, r: Any=r) -> tuple[int, str] | None:
        if equals(c.Value, ""):
            return None

        else: 
            return (c.ColumnNumber - 1, c.ValueAsString())


    return choose(chooser, r.Cells)


def SparseRowModule_tryGetValueAt(i: int, vs: IEnumerable_1[tuple[int, str]]) -> str | None:
    def chooser(tupled_arg: tuple[int, str], i: Any=i, vs: Any=vs) -> str | None:
        if tupled_arg[0] == i:
            return tupled_arg[1]

        else: 
            return None


    return try_pick(chooser, vs)


def SparseRowModule_toDSLRow(vs: IEnumerable_1[tuple[int, str]]) -> FSharpList[RowElement]:
    _builder: RowBuilder = RowBuilder__ctor()
    this_9: SheetEntity_1[FSharpList[RowElement]]
    def f_2(_arg: str | None=None, vs: Any=vs) -> SheetEntity_1[FSharpList[RowElement]]:
        v: str | None = _arg
        if v is None:
            c_1: tuple[tuple[DataType, Any], int | None]
            this_5: SheetEntity_1[tuple[tuple[DataType, Any], int | None]] = CellBuilder__AsCellElement_6F87C2ED(CellBuilder__ctor(), SheetEntity_1_some_2B595(singleton((DataType(0), ""))))
            (pattern_matching_result, errs_1, f_1) = (None, None, None)
            if this_5.tag == 1:
                if equals(this_5.fields[0], empty()):
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            elif this_5.tag == 2:
                if equals(this_5.fields[0], empty()):
                    pattern_matching_result = 1

                else: 
                    pattern_matching_result = 2


            else: 
                pattern_matching_result = 0
                errs_1 = this_5.fields[1]
                f_1 = this_5.fields[0]

            if pattern_matching_result == 0:
                c_1 = f_1

            elif pattern_matching_result == 1:
                raise Exception("SheetEntity does not contain Value.")

            elif pattern_matching_result == 2:
                (pattern_matching_result_1, ms_3_1) = (None, None)
                if this_5.tag == 1:
                    pattern_matching_result_1 = 0
                    ms_3_1 = this_5.fields[0]

                elif this_5.tag == 2:
                    pattern_matching_result_1 = 0
                    ms_3_1 = this_5.fields[0]

                else: 
                    pattern_matching_result_1 = 1

                if pattern_matching_result_1 == 0:
                    raise Exception(("SheetEntity does not contain Value: \n\t" + Messages_format(ms_3_1)) + "")

                elif pattern_matching_result_1 == 1:
                    raise Exception("Match failure: FsSpreadsheet.DSL.SheetEntity`1")


            return SheetEntity_1_some_2B595(singleton(RowElement(1, c_1[0]) if (c_1[1] is None) else RowElement(0, ColumnIndex(0, c_1[1]), c_1[0])))

        else: 
            v_1: str = v
            c: tuple[tuple[DataType, Any], int | None]
            this_2: SheetEntity_1[tuple[tuple[DataType, Any], int | None]] = CellBuilder__AsCellElement_6F87C2ED(CellBuilder__ctor(), SheetEntity_1_some_2B595(singleton((DataType(0), v_1))))
            (pattern_matching_result_2, errs, f) = (None, None, None)
            if this_2.tag == 1:
                if equals(this_2.fields[0], empty()):
                    pattern_matching_result_2 = 1

                else: 
                    pattern_matching_result_2 = 2


            elif this_2.tag == 2:
                if equals(this_2.fields[0], empty()):
                    pattern_matching_result_2 = 1

                else: 
                    pattern_matching_result_2 = 2


            else: 
                pattern_matching_result_2 = 0
                errs = this_2.fields[1]
                f = this_2.fields[0]

            if pattern_matching_result_2 == 0:
                c = f

            elif pattern_matching_result_2 == 1:
                raise Exception("SheetEntity does not contain Value.")

            elif pattern_matching_result_2 == 2:
                (pattern_matching_result_3, ms_3) = (None, None)
                if this_2.tag == 1:
                    pattern_matching_result_3 = 0
                    ms_3 = this_2.fields[0]

                elif this_2.tag == 2:
                    pattern_matching_result_3 = 0
                    ms_3 = this_2.fields[0]

                else: 
                    pattern_matching_result_3 = 1

                if pattern_matching_result_3 == 0:
                    raise Exception(("SheetEntity does not contain Value: \n\t" + Messages_format(ms_3)) + "")

                elif pattern_matching_result_3 == 1:
                    raise Exception("Match failure: FsSpreadsheet.DSL.SheetEntity`1")


            return SheetEntity_1_some_2B595(singleton(RowElement(1, c[0]) if (c[1] is None) else RowElement(0, ColumnIndex(0, c[1]), c[0])))


    ns: IEnumerable_1[SheetEntity_1[FSharpList[RowElement]]] = map(f_2, SparseRowModule_getAllValues(vs))
    def folder(state: SheetEntity_1[FSharpList[RowElement]], we: SheetEntity_1[FSharpList[RowElement]], vs: Any=vs) -> SheetEntity_1[FSharpList[RowElement]]:
        return RowBuilder__Combine_19F30600(_builder, state, we)

    this_9 = fold(folder, RowBuilder_get_Empty(), ns)
    (pattern_matching_result_4, errs_2, f_3) = (None, None, None)
    if this_9.tag == 1:
        if equals(this_9.fields[0], empty()):
            pattern_matching_result_4 = 1

        else: 
            pattern_matching_result_4 = 2


    elif this_9.tag == 2:
        if equals(this_9.fields[0], empty()):
            pattern_matching_result_4 = 1

        else: 
            pattern_matching_result_4 = 2


    else: 
        pattern_matching_result_4 = 0
        errs_2 = this_9.fields[1]
        f_3 = this_9.fields[0]

    if pattern_matching_result_4 == 0:
        return f_3

    elif pattern_matching_result_4 == 1:
        raise Exception("SheetEntity does not contain Value.")

    elif pattern_matching_result_4 == 2:
        (pattern_matching_result_5, ms_3_2) = (None, None)
        if this_9.tag == 1:
            pattern_matching_result_5 = 0
            ms_3_2 = this_9.fields[0]

        elif this_9.tag == 2:
            pattern_matching_result_5 = 0
            ms_3_2 = this_9.fields[0]

        else: 
            pattern_matching_result_5 = 1

        if pattern_matching_result_5 == 0:
            raise Exception(("SheetEntity does not contain Value: \n\t" + Messages_format(ms_3_2)) + "")

        elif pattern_matching_result_5 == 1:
            raise Exception("Match failure: FsSpreadsheet.DSL.SheetEntity`1")




def SparseRowModule_readFromSheet(sheet: FsWorksheet) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    def mapping(r: FsRow, sheet: Any=sheet) -> IEnumerable_1[tuple[int, str]]:
        return SparseRowModule_fromFsRow(r)

    return map(mapping, sheet.Rows)


def SparseRowModule_writeToSheet(row_i: int, row: IEnumerable_1[tuple[int, str]], sheet: FsWorksheet) -> None:
    fs_row: FsRow = sheet.RowWithRange(FsRangeAddress(FsAddress(row_i, 1), FsAddress(row_i, 1)), True)
    def action(tupled_arg: tuple[int, str], row_i: Any=row_i, row: Any=row, sheet: Any=sheet) -> None:
        v: str = tupled_arg[1]
        if v.strip() != "":
            fs_row.Item(tupled_arg[0] + 1).SetValueAs(v)


    iterate(action, row)


def _expr1066() -> TypeInfo:
    return record_type("ARCtrl.Spreadsheet.SparseTable", [], SparseTable, lambda: [("Matrix", class_type("System.Collections.Generic.Dictionary`2", [tuple_type(string_type, int32_type), string_type])), ("Keys", list_type(string_type)), ("CommentKeys", list_type(string_type)), ("ColumnCount", int32_type)])


@dataclass(eq = False, repr = False, slots = True)
class SparseTable(Record):
    Matrix: Any
    Keys: FSharpList[str]
    CommentKeys: FSharpList[str]
    ColumnCount: int

SparseTable_reflection = _expr1066

def SparseTable__TryGetValue_11FD62A8(this: SparseTable, key: tuple[str, int]) -> str | None:
    return Dictionary_tryGetValue(key, this.Matrix)


def SparseTable__TryGetValueDefault_5BAE6133(this: SparseTable, default_value: str, key: tuple[str, int]) -> str:
    if key in this.Matrix:
        return get_item_from_dict(this.Matrix, key)

    else: 
        return default_value



def SparseTable_Create_Z2192E64B(matrix: Any | None=None, keys: FSharpList[str] | None=None, comment_keys: FSharpList[str] | None=None, length: int | None=None) -> SparseTable:
    return SparseTable(default_arg(matrix, Dictionary_init()), default_arg(keys, empty()), default_arg(comment_keys, empty()), default_arg(length, 0))


def SparseTable_AddRow(key: str, values: IEnumerable_1[tuple[int, str]], matrix: SparseTable) -> SparseTable:
    def action(tupled_arg: tuple[int, str], key: Any=key, values: Any=values, matrix: Any=matrix) -> None:
        add_to_dict(matrix.Matrix, (key, tupled_arg[0]), tupled_arg[1])

    iterate(action, values)
    def _arrow1067(tuple: tuple[int, str], key: Any=key, values: Any=values, matrix: Any=matrix) -> int:
        return tuple[0]

    class ObjectExpr1068:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    length: int = (0 if is_empty(values) else (1 + max_by(_arrow1067, values, ObjectExpr1068())[0])) or 0
    return SparseTable(matrix.Matrix, append(matrix.Keys, singleton(key)), matrix.CommentKeys, length if (length > matrix.ColumnCount) else matrix.ColumnCount)


def SparseTable_AddEmptyComment(key: str, matrix: SparseTable) -> SparseTable:
    return SparseTable(matrix.Matrix, matrix.Keys, append(matrix.CommentKeys, singleton(key)), matrix.ColumnCount)


def SparseTable_AddComment(key: str, values: IEnumerable_1[tuple[int, str]], matrix: SparseTable) -> SparseTable:
    if length_1(values) == 0:
        return SparseTable_AddEmptyComment(key, matrix)

    else: 
        def action(tupled_arg: tuple[int, str], key: Any=key, values: Any=values, matrix: Any=matrix) -> None:
            add_to_dict(matrix.Matrix, (key, tupled_arg[0]), tupled_arg[1])

        iterate(action, values)
        def _arrow1069(tuple: tuple[int, str], key: Any=key, values: Any=values, matrix: Any=matrix) -> int:
            return tuple[0]

        class ObjectExpr1070:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        length: int = (0 if is_empty(values) else (1 + max_by(_arrow1069, values, ObjectExpr1070())[0])) or 0
        return SparseTable(matrix.Matrix, matrix.Keys, append(matrix.CommentKeys, singleton(key)), length if (length > matrix.ColumnCount) else matrix.ColumnCount)



def SparseTable_FromRows_Z5579EC29(en: IEnumerator[IEnumerable_1[tuple[int, str]]], labels: FSharpList[str], line_number: int, prefix: str | None=None) -> tuple[str | None, int, FSharpList[Remark], SparseTable]:
    try: 
        prefix_1: str = "" if (prefix is None) else (prefix + " ")
        def loop(matrix_mut: SparseTable, remarks_mut: FSharpList[Remark], line_number_1_mut: int) -> tuple[str | None, int, FSharpList[Remark], SparseTable]:
            while True:
                (matrix, remarks, line_number_1) = (matrix_mut, remarks_mut, line_number_1_mut)
                if en.System_Collections_IEnumerator_MoveNext():
                    def mapping(tupled_arg: tuple[int, str], matrix: Any=matrix, remarks: Any=remarks, line_number_1: Any=line_number_1) -> tuple[int, str]:
                        return (tupled_arg[0] - 1, tupled_arg[1])

                    row: IEnumerable_1[tuple[int, str]] = map(mapping, en.System_Collections_Generic_IEnumerator_1_get_Current())
                    def mapping_1(tuple: tuple[int, str], matrix: Any=matrix, remarks: Any=remarks, line_number_1: Any=line_number_1) -> str:
                        return tuple[1]

                    match_value: str | None = map_1(mapping_1, try_item(0, row))
                    vals: IEnumerable_1[tuple[int, str]] | None = Seq_trySkip(1, row)
                    key: str | None = match_value
                    (pattern_matching_result, k, v_1) = (None, None, None)
                    if key is not None:
                        active_pattern_result: str | None = Comment__007CComment_007C__007C(key)
                        if active_pattern_result is not None:
                            if vals is not None:
                                pattern_matching_result = 0
                                k = active_pattern_result
                                v_1 = vals

                            else: 
                                pattern_matching_result = 1


                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1

                    if pattern_matching_result == 0:
                        matrix_mut = SparseTable_AddComment(k, v_1, matrix)
                        remarks_mut = remarks
                        line_number_1_mut = line_number_1 + 1
                        continue

                    elif pattern_matching_result == 1:
                        (pattern_matching_result_1, k_2, k_3, v_3, k_4) = (None, None, None, None, None)
                        active_pattern_result_1: str | None = Remark__007CRemark_007C__007C(key)
                        if active_pattern_result_1 is not None:
                            pattern_matching_result_1 = 0
                            k_2 = active_pattern_result_1

                        elif key is not None:
                            if vals is not None:
                                def _arrow1073(__unit: None=None, matrix: Any=matrix, remarks: Any=remarks, line_number_1: Any=line_number_1) -> bool:
                                    v_2: IEnumerable_1[tuple[int, str]] = vals
                                    k_1: str = key
                                    def _arrow1072(label: str) -> bool:
                                        return k_1 == (prefix_1 + label)

                                    return exists(_arrow1072, labels)

                                if _arrow1073():
                                    pattern_matching_result_1 = 1
                                    k_3 = key
                                    v_3 = vals

                                else: 
                                    pattern_matching_result_1 = 2
                                    k_4 = key


                            else: 
                                pattern_matching_result_1 = 2
                                k_4 = key


                        else: 
                            pattern_matching_result_1 = 3

                        if pattern_matching_result_1 == 0:
                            matrix_mut = matrix
                            remarks_mut = cons(Remark.make(line_number_1, k_2), remarks)
                            line_number_1_mut = line_number_1 + 1
                            continue

                        elif pattern_matching_result_1 == 1:
                            def _arrow1071(label_1: str, matrix: Any=matrix, remarks: Any=remarks, line_number_1: Any=line_number_1) -> bool:
                                return k_3 == (prefix_1 + label_1)

                            matrix_mut = SparseTable_AddRow(find(_arrow1071, labels), v_3, matrix)
                            remarks_mut = remarks
                            line_number_1_mut = line_number_1 + 1
                            continue

                        elif pattern_matching_result_1 == 2:
                            return (k_4, line_number_1, remarks, matrix)

                        elif pattern_matching_result_1 == 3:
                            return (None, line_number_1, remarks, matrix)



                else: 
                    return (None, line_number_1, remarks, matrix)

                break

        return loop(SparseTable_Create_Z2192E64B(), empty(), line_number)

    except Exception as err:
        arg_1: str = str(err)
        return to_fail(printf("Error parsing block in investigation file starting from line number %i: %s"))(line_number)(arg_1)



def SparseTable_ToRows_759CAFC1(matrix: SparseTable, prefix: str | None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
    prefix_1: str = "" if (prefix is None) else (prefix + " ")
    def _arrow1079(__unit: None=None, matrix: Any=matrix, prefix: Any=prefix) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
        def _arrow1075(key: str) -> IEnumerable_1[tuple[int, str]]:
            def _arrow1074(i: int) -> str:
                return SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (key, i + 1))

            return SparseRowModule_fromValues(cons(prefix_1 + key, initialize_1(matrix.ColumnCount - 1, _arrow1074)))

        def _arrow1078(__unit: None=None) -> IEnumerable_1[IEnumerable_1[tuple[int, str]]]:
            def _arrow1077(key_1: str) -> IEnumerable_1[tuple[int, str]]:
                def _arrow1076(i_1: int) -> str:
                    return SparseTable__TryGetValueDefault_5BAE6133(matrix, "", (key_1, i_1 + 1))

                return SparseRowModule_fromValues(cons(Comment_wrapCommentKey(key_1), initialize_1(matrix.ColumnCount - 1, _arrow1076)))

            return map(_arrow1077, matrix.CommentKeys)

        return append_1(map(_arrow1075, matrix.Keys), delay(_arrow1078))

    return delay(_arrow1079)


def SparseTable_GetEmptyComments_3ECCA699(matrix: SparseTable) -> Array[Comment]:
    def mapping(key: str, matrix: Any=matrix) -> Comment:
        return Comment.create(key)

    return list(map_2(mapping, matrix.CommentKeys))


__all__ = ["SparseRowModule_fromValues", "SparseRowModule_getValues", "SparseRowModule_fromAllValues", "SparseRowModule_getAllValues", "SparseRowModule_fromFsRow", "SparseRowModule_tryGetValueAt", "SparseRowModule_toDSLRow", "SparseRowModule_readFromSheet", "SparseRowModule_writeToSheet", "SparseTable_reflection", "SparseTable__TryGetValue_11FD62A8", "SparseTable__TryGetValueDefault_5BAE6133", "SparseTable_Create_Z2192E64B", "SparseTable_AddRow", "SparseTable_AddEmptyComment", "SparseTable_AddComment", "SparseTable_FromRows_Z5579EC29", "SparseTable_ToRows_759CAFC1", "SparseTable_GetEmptyComments_3ECCA699"]


from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import insert_range_in_place
from ...fable_modules.fable_library.list import FSharpList
from ...fable_modules.fable_library.map import (of_seq as of_seq_1, try_find)
from ...fable_modules.fable_library.map_util import (add_to_dict, add_to_set)
from ...fable_modules.fable_library.option import (value as value_2, default_arg, map as map_2, bind)
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.seq import (try_find_index, find_index, length, to_list, delay, map as map_1, choose, reduce, append)
from ...fable_modules.fable_library.seq2 import distinct
from ...fable_modules.fable_library.set import (intersect, of_seq, FSharpSet__get_IsEmpty)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (get_enumerator, dispose, compare, string_hash, IEnumerable_1, compare_primitives, equals, ignore, IEnumerator, to_iterator)
from ..Helper.collections_ import (Dictionary_tryFind, ResizeArray_iter, ResizeArray_fold, ResizeArray_map, ResizeArray_groupBy, ResizeArray_collect)
from .arc_table import ArcTable
from .composite_cell import CompositeCell
from .composite_column import CompositeColumn
from .composite_header import (IOType, CompositeHeader)

def ArcTablesAux_tryFindIndexByTableName(name: str, tables: Array[ArcTable]) -> int | None:
    def predicate(t: ArcTable, name: Any=name, tables: Any=tables) -> bool:
        return t.Name == name

    return try_find_index(predicate, tables)


def ArcTablesAux_findIndexByTableName(name: str, tables: Array[ArcTable]) -> int:
    def predicate(t: ArcTable, name: Any=name, tables: Any=tables) -> bool:
        return t.Name == name

    match_value: int | None = try_find_index(predicate, tables)
    if match_value is None:
        raise Exception(("Unable to find table with name \'" + name) + "\'!")

    else: 
        return match_value



def ArcTablesAux_getIOMap(tables: Array[ArcTable]) -> Any:
    mappings: Any = dict([])
    def include_in_map(name: str, io_type: IOType, tables: Any=tables) -> None:
        if name != "":
            match_value: IOType | None = Dictionary_tryFind(name, mappings)
            if match_value is None:
                add_to_dict(mappings, name, io_type)

            else: 
                old_iotype: IOType = match_value
                new_iotype: IOType = old_iotype.Merge(io_type)
                mappings[name] = new_iotype



    enumerator: Any = get_enumerator(tables)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            table: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            match_value_1: CompositeColumn | None = table.TryGetInputColumn()
            if match_value_1 is None:
                pass

            else: 
                ic: CompositeColumn = match_value_1
                io_type_1: IOType = value_2(ic.Header.TryInput())
                def f(c: CompositeCell) -> None:
                    include_in_map(c.ToFreeTextCell().AsFreeText, io_type_1)

                ResizeArray_iter(f, ic.Cells)

            match_value_2: CompositeColumn | None = table.TryGetOutputColumn()
            if match_value_2 is None:
                pass

            else: 
                oc: CompositeColumn = match_value_2
                io_type_2: IOType = value_2(oc.Header.TryOutput())
                def f_1(c_1: CompositeCell) -> None:
                    include_in_map(c_1.ToFreeTextCell().AsFreeText, io_type_2)

                ResizeArray_iter(f_1, oc.Cells)


    finally: 
        dispose(enumerator)

    return mappings


def ArcTablesAux_applyIOMap(map: Any, tables: Array[ArcTable]) -> None:
    enumerator: Any = get_enumerator(tables)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            table: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            match_value: CompositeColumn | None = table.TryGetInputColumn()
            if match_value is None:
                pass

            else: 
                ic: CompositeColumn = match_value
                def predicate(x: CompositeHeader) -> bool:
                    return x.is_input

                index: int = find_index(predicate, table.Headers) or 0
                def f(io: IOType, c: CompositeCell) -> IOType:
                    match_value_1: IOType | None = Dictionary_tryFind(c.ToFreeTextCell().AsFreeText, map)
                    if match_value_1 is None:
                        return io

                    else: 
                        new_io: IOType = match_value_1
                        return io.Merge(new_io)


                new_iotype: IOType = ResizeArray_fold(f, value_2(ic.Header.TryInput()), ic.Cells)
                table.UpdateHeader(index, CompositeHeader(11, new_iotype))

            match_value_2: CompositeColumn | None = table.TryGetOutputColumn()
            if match_value_2 is None:
                pass

            else: 
                oc: CompositeColumn = match_value_2
                def predicate_1(x_1: CompositeHeader) -> bool:
                    return x_1.is_output

                index_1: int = find_index(predicate_1, table.Headers) or 0
                def f_1(io_1: IOType, c_1: CompositeCell) -> IOType:
                    match_value_3: IOType | None = Dictionary_tryFind(c_1.ToFreeTextCell().AsFreeText, map)
                    if match_value_3 is None:
                        return io_1

                    else: 
                        new_io_1: IOType = match_value_3
                        return io_1.Merge(new_io_1)


                new_iotype_1: IOType = ResizeArray_fold(f_1, value_2(oc.Header.TryOutput()), oc.Cells)
                table.UpdateHeader(index_1, CompositeHeader(12, new_iotype_1))


    finally: 
        dispose(enumerator)



def ArcTablesAux_SanityChecks_validateSheetIndex(index: int, allow_append: bool, sheets: Array[ArcTable]) -> None:
    if index < 0:
        raise Exception("Cannot insert ArcTable at index < 0.")

    def _arrow888(__unit: None=None, index: Any=index, allow_append: Any=allow_append, sheets: Any=sheets) -> bool:
        x: int = index or 0
        y: int = len(sheets) or 0
        return (compare(x, y) > 0) if allow_append else (compare(x, y) >= 0)

    if _arrow888():
        raise Exception(("Specified index is out of range! Assay contains only " + str(len(sheets))) + " tables.")



def ArcTablesAux_SanityChecks_validateNamesUnique(names: IEnumerable_1[str]) -> None:
    class ObjectExpr890:
        @property
        def Equals(self) -> Callable[[str, str], bool]:
            def _arrow889(x: str, y: str) -> bool:
                return x == y

            return _arrow889

        @property
        def GetHashCode(self) -> Callable[[str], int]:
            return string_hash

    if not (length(names) == length(distinct(names, ObjectExpr890()))):
        raise Exception("Cannot add multiple tables with the same name! Table names inside one assay must be unqiue")



def ArcTablesAux_SanityChecks_validateNewNameUnique(new_name: str, existing_names: IEnumerable_1[str]) -> None:
    def _arrow891(x: str, new_name: Any=new_name, existing_names: Any=existing_names) -> bool:
        return x == new_name

    match_value: int | None = try_find_index(_arrow891, existing_names)
    if match_value is None:
        pass

    else: 
        raise Exception(((("Cannot create table with name " + new_name) + ", as table names must be unique and table at index ") + str(match_value)) + " has the same name.")



def ArcTablesAux_SanityChecks_validateNewNameAtUnique(index: int, new_name: str, existing_names: IEnumerable_1[str]) -> None:
    def _arrow892(x: str, index: Any=index, new_name: Any=new_name, existing_names: Any=existing_names) -> bool:
        return x == new_name

    match_value: int | None = try_find_index(_arrow892, existing_names)
    if match_value is None:
        pass

    elif index == match_value:
        i_1: int = match_value or 0

    else: 
        i_2: int = match_value or 0
        raise Exception(((("Cannot create table with name " + new_name) + ", as table names must be unique and table at index ") + str(i_2)) + " has the same name.")



def ArcTablesAux_SanityChecks_validateNewNamesUnique(new_names: IEnumerable_1[str], existing_names: IEnumerable_1[str]) -> None:
    ArcTablesAux_SanityChecks_validateNamesUnique(new_names)
    class ObjectExpr893:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    class ObjectExpr894:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    same: Any = intersect(of_seq(new_names, ObjectExpr893()), of_seq(existing_names, ObjectExpr894()))
    if not FSharpSet__get_IsEmpty(same):
        raise Exception(("Cannot create tables with the names " + str(same)) + ", as table names must be unique.")



def _expr917() -> TypeInfo:
    return class_type("ARCtrl.ArcTables", None, ArcTables)


class ArcTables:
    def __init__(self, init_tables: Array[ArcTable]) -> None:
        def _expr916():
            def mapping(t: ArcTable) -> str:
                return t.Name

            ArcTablesAux_SanityChecks_validateNamesUnique(map_1(mapping, init_tables))
            return init_tables

        self.tables: Array[ArcTable] = _expr916()

    @property
    def Tables(self, __unit: None=None) -> Array[ArcTable]:
        this: ArcTables = self
        return this.tables

    @Tables.setter
    def Tables(self, new_tables: Array[ArcTable]) -> None:
        this: ArcTables = self
        this.tables = new_tables

    def get_item(self, index: int) -> ArcTable:
        this: ArcTables = self
        return this.Tables[index]

    @property
    def TableNames(self, __unit: None=None) -> FSharpList[str]:
        this: ArcTables = self
        def _arrow896(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow895(s: ArcTable) -> str:
                return s.Name

            return map_1(_arrow895, this.Tables)

        return to_list(delay(_arrow896))

    @property
    def TableCount(self, __unit: None=None) -> int:
        this: ArcTables = self
        return len(this.Tables)

    def AddTable(self, table: ArcTable, index: int | None=None) -> None:
        this: ArcTables = self
        index_1: int = default_arg(index, this.TableCount) or 0
        ArcTablesAux_SanityChecks_validateSheetIndex(index_1, True, this.Tables)
        ArcTablesAux_SanityChecks_validateNewNameUnique(table.Name, this.TableNames)
        this.Tables.insert(index_1, table)

    def AddTables(self, tables: IEnumerable_1[ArcTable], index: int | None=None) -> None:
        this: ArcTables = self
        index_1: int = default_arg(index, this.TableCount) or 0
        ArcTablesAux_SanityChecks_validateSheetIndex(index_1, True, this.Tables)
        def mapping(x: ArcTable) -> str:
            return x.Name

        ArcTablesAux_SanityChecks_validateNewNamesUnique(map_1(mapping, tables), this.TableNames)
        insert_range_in_place(index_1, tables, this.Tables)

    def InitTable(self, table_name: str, index: int | None=None) -> ArcTable:
        this: ArcTables = self
        index_1: int = default_arg(index, this.TableCount) or 0
        table: ArcTable = ArcTable.init(table_name)
        ArcTablesAux_SanityChecks_validateSheetIndex(index_1, True, this.Tables)
        ArcTablesAux_SanityChecks_validateNewNameUnique(table.Name, this.TableNames)
        this.Tables.insert(index_1, table)
        return table

    def InitTables(self, table_names: IEnumerable_1[str], index: int | None=None) -> None:
        this: ArcTables = self
        index_1: int = default_arg(index, this.TableCount) or 0
        def mapping(x: str) -> ArcTable:
            return ArcTable.init(x)

        tables: IEnumerable_1[ArcTable] = map_1(mapping, table_names)
        ArcTablesAux_SanityChecks_validateSheetIndex(index_1, True, this.Tables)
        def mapping_1(x_1: ArcTable) -> str:
            return x_1.Name

        ArcTablesAux_SanityChecks_validateNewNamesUnique(map_1(mapping_1, tables), this.TableNames)
        insert_range_in_place(index_1, tables, this.Tables)

    def GetTableAt(self, index: int) -> ArcTable:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, False, this.Tables)
        return this.Tables[index]

    def GetTable(self, name: str) -> ArcTable:
        this: ArcTables = self
        index: int = ArcTablesAux_findIndexByTableName(name, this.Tables) or 0
        return this.GetTableAt(index)

    def UpdateTableAt(self, index: int, table: ArcTable) -> None:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, False, this.Tables)
        ArcTablesAux_SanityChecks_validateNewNameAtUnique(index, table.Name, this.TableNames)
        this.Tables[index] = table

    def UpdateTable(self, name: str, table: ArcTable) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, ArcTable] = (ArcTablesAux_findIndexByTableName(name, this.Tables), table)
        this.UpdateTableAt(tupled_arg[0], tupled_arg[1])

    def SetTableAt(self, index: int, table: ArcTable) -> None:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, True, this.Tables)
        ArcTablesAux_SanityChecks_validateNewNameAtUnique(index, table.Name, this.TableNames)
        this.Tables[index] = table

    def SetTable(self, name: str, table: ArcTable) -> None:
        this: ArcTables = self
        match_value: int | None = ArcTablesAux_tryFindIndexByTableName(name, this.Tables)
        if match_value is None:
            this.AddTable(table)

        else: 
            index: int = match_value or 0
            this.SetTableAt(index, table)


    def RemoveTableAt(self, index: int) -> None:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, False, this.Tables)
        this.Tables.pop(index)

    def RemoveTable(self, name: str) -> None:
        this: ArcTables = self
        index: int = ArcTablesAux_findIndexByTableName(name, this.Tables) or 0
        this.RemoveTableAt(index)

    def MapTableAt(self, index: int, update_fun: Callable[[ArcTable], None]) -> None:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, False, this.Tables)
        update_fun(this.Tables[index])

    def MapTable(self, name: str, update_fun: Callable[[ArcTable], None]) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, Callable[[ArcTable], None]] = (ArcTablesAux_findIndexByTableName(name, this.Tables), update_fun)
        this.MapTableAt(tupled_arg[0], tupled_arg[1])

    def RenameTableAt(self, index: int, new_name: str) -> None:
        this: ArcTables = self
        ArcTablesAux_SanityChecks_validateSheetIndex(index, False, this.Tables)
        ArcTablesAux_SanityChecks_validateNewNameUnique(new_name, this.TableNames)
        table: ArcTable = this.GetTableAt(index)
        table.Name = new_name

    def RenameTable(self, name: str, new_name: str) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, str] = (ArcTablesAux_findIndexByTableName(name, this.Tables), new_name)
        this.RenameTableAt(tupled_arg[0], tupled_arg[1])

    def AddColumnAt(self, table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> None:
        this: ArcTables = self
        def _arrow897(table: ArcTable) -> None:
            table.AddColumn(header, cells, column_index, force_replace)

        this.MapTableAt(table_index, _arrow897)

    def AddColumn(self, table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> None:
        this: ArcTables = self
        i: int = ArcTablesAux_findIndexByTableName(table_name, this.Tables) or 0
        this.AddColumnAt(i, header, cells, column_index, force_replace)

    def RemoveColumnAt(self, table_index: int, column_index: int) -> None:
        this: ArcTables = self
        def _arrow898(table: ArcTable) -> None:
            table.RemoveColumn(column_index)

        this.MapTableAt(table_index, _arrow898)

    def RemoveColumn(self, table_name: str, column_index: int) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, int] = (ArcTablesAux_findIndexByTableName(table_name, this.Tables), column_index)
        this.RemoveColumnAt(tupled_arg[0], tupled_arg[1])

    def UpdateColumnAt(self, table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTables = self
        def _arrow899(table: ArcTable) -> None:
            table.UpdateColumn(column_index, header, cells)

        this.MapTableAt(table_index, _arrow899)

    def UpdateColumn(self, table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTables = self
        table_index: int = ArcTablesAux_findIndexByTableName(table_name, this.Tables) or 0
        this.UpdateColumnAt(table_index, column_index, header, cells)

    def GetColumnAt(self, table_index: int, column_index: int) -> CompositeColumn:
        this: ArcTables = self
        table: ArcTable = this.GetTableAt(table_index)
        return table.GetColumn(column_index)

    def GetColumn(self, table_name: str, column_index: int) -> CompositeColumn:
        this: ArcTables = self
        tupled_arg: tuple[int, int] = (ArcTablesAux_findIndexByTableName(table_name, this.Tables), column_index)
        return this.GetColumnAt(tupled_arg[0], tupled_arg[1])

    def AddRowAt(self, table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> None:
        this: ArcTables = self
        def _arrow904(table: ArcTable) -> None:
            table.AddRow(cells, row_index)

        this.MapTableAt(table_index, _arrow904)

    def AddRow(self, table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> None:
        this: ArcTables = self
        i: int = ArcTablesAux_findIndexByTableName(table_name, this.Tables) or 0
        this.AddRowAt(i, cells, row_index)

    def RemoveRowAt(self, table_index: int, row_index: int) -> None:
        this: ArcTables = self
        def _arrow905(table: ArcTable) -> None:
            table.RemoveRow(row_index)

        this.MapTableAt(table_index, _arrow905)

    def RemoveRow(self, table_name: str, row_index: int) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, int] = (ArcTablesAux_findIndexByTableName(table_name, this.Tables), row_index)
        this.RemoveRowAt(tupled_arg[0], tupled_arg[1])

    def UpdateRowAt(self, table_index: int, row_index: int, cells: Array[CompositeCell]) -> None:
        this: ArcTables = self
        def _arrow906(table: ArcTable) -> None:
            table.UpdateRow(row_index, cells)

        this.MapTableAt(table_index, _arrow906)

    def UpdateRow(self, table_name: str, row_index: int, cells: Array[CompositeCell]) -> None:
        this: ArcTables = self
        tupled_arg: tuple[int, int, Array[CompositeCell]] = (ArcTablesAux_findIndexByTableName(table_name, this.Tables), row_index, cells)
        this.UpdateRowAt(tupled_arg[0], tupled_arg[1], tupled_arg[2])

    def GetRowAt(self, table_index: int, row_index: int) -> Array[CompositeCell]:
        this: ArcTables = self
        table: ArcTable = this.GetTableAt(table_index)
        return table.GetRow(row_index)

    def GetRow(self, table_name: str, row_index: int) -> Array[CompositeCell]:
        this: ArcTables = self
        tupled_arg: tuple[int, int] = (ArcTablesAux_findIndexByTableName(table_name, this.Tables), row_index)
        return this.GetRowAt(tupled_arg[0], tupled_arg[1])

    @staticmethod
    def of_seq(tables: IEnumerable_1[ArcTable]) -> ArcTables:
        return ArcTables(list(tables))

    def MoveTable(self, old_index: int, new_index: int) -> None:
        this: ArcTables = self
        table: ArcTable = this.GetTableAt(old_index)
        this.Tables.pop(old_index)
        this.Tables.insert(new_index, table)

    @staticmethod
    def update_reference_tables_by_sheets(reference_tables: ArcTables, sheet_tables: ArcTables, keep_unused_ref_tables: bool | None=None) -> ArcTables:
        keep_unused_ref_tables_1: bool = default_arg(keep_unused_ref_tables, False)
        used_tables: Any = set([])
        def chooser(t: ArcTable) -> tuple[str, ArcTable] | None:
            def mapping(c: CompositeColumn, t: Any=t) -> tuple[str, ArcTable]:
                return (c.Cells[0].AsFreeText, t)

            return map_2(mapping, t.TryGetProtocolNameColumn())

        class ObjectExpr911:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        reference_table_map: Any = of_seq_1(choose(chooser, reference_tables.Tables), ObjectExpr911())
        def _arrow914(__unit: None=None) -> IEnumerable_1[ArcTable]:
            def f_3(tupled_arg: tuple[str, Array[ArcTable]]) -> ArcTable:
                def reduction(table: ArcTable, table_1: ArcTable, tupled_arg: Any=tupled_arg) -> ArcTable:
                    return ArcTable.append(table, table_1)

                return reduce(reduction, tupled_arg[1])

            def f_2(t_2: ArcTable) -> str:
                return t_2.Name

            def f_1(t_1: ArcTable) -> ArcTable:
                def binder_1(c_1: CompositeCell, t_1: Any=t_1) -> str | None:
                    if c_1.AsFreeText == "":
                        return None

                    else: 
                        return c_1.AsFreeText


                def binder(i: int, t_1: Any=t_1) -> CompositeCell | None:
                    return t_1.TryGetCellAt(i, 0)

                def predicate(x_1: CompositeHeader, t_1: Any=t_1) -> bool:
                    return equals(x_1, CompositeHeader(8))

                k: str = default_arg(bind(binder_1, bind(binder, try_find_index(predicate, t_1.Headers))), t_1.Name)
                match_value: ArcTable | None = try_find(k, reference_table_map)
                if match_value is None:
                    return t_1

                else: 
                    rt: ArcTable = match_value
                    ignore(add_to_set(k, used_tables))
                    updated_table: ArcTable = ArcTable.update_reference_by_annotation_table(rt, t_1)
                    return ArcTable.from_arc_table_values(t_1.Name, updated_table.Headers, updated_table.Values)


            def _arrow913(__unit: None=None) -> Array[ArcTable]:
                a: Array[ArcTable] = sheet_tables.Tables
                return ResizeArray_collect(ArcTable.SplitByProtocolREF(), a)

            s: Array[ArcTable] = ResizeArray_map(f_3, ResizeArray_groupBy(f_2, ResizeArray_map(f_1, _arrow913())))
            def chooser_1(kv: Any) -> ArcTable | None:
                if kv[0] in used_tables:
                    return None

                else: 
                    return kv[1]


            return append(choose(chooser_1, reference_table_map), s) if keep_unused_ref_tables_1 else s

        return ArcTables(list(_arrow914()))

    def GetEnumerator(self, __unit: None=None) -> IEnumerator[ArcTable]:
        this: ArcTables = self
        return get_enumerator(this.Tables)

    def __iter__(self) -> IEnumerator[ArcTable]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None=None) -> IEnumerator[Any]:
        this: ArcTables = self
        return get_enumerator(this.Tables)


ArcTables_reflection = _expr917

def ArcTables__ctor_Z420F2E1A(init_tables: Array[ArcTable]) -> ArcTables:
    return ArcTables(init_tables)


__all__ = ["ArcTablesAux_tryFindIndexByTableName", "ArcTablesAux_findIndexByTableName", "ArcTablesAux_getIOMap", "ArcTablesAux_applyIOMap", "ArcTablesAux_SanityChecks_validateSheetIndex", "ArcTablesAux_SanityChecks_validateNamesUnique", "ArcTablesAux_SanityChecks_validateNewNameUnique", "ArcTablesAux_SanityChecks_validateNewNameAtUnique", "ArcTablesAux_SanityChecks_validateNewNamesUnique", "ArcTables_reflection"]


from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.int32 import op_unary_negation_int32
from ...fable_modules.fable_library.list import (cons, is_empty as is_empty_1, tail as tail_1, head, FSharpList, empty as empty_1, of_seq, length as length_1, exists, pick, map_indexed)
from ...fable_modules.fable_library.map_util import (add_to_dict, get_item_from_dict, remove_from_dict, try_get_value)
from ...fable_modules.fable_library.option import (value as value_3, bind)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.reflection import (TypeInfo, int32_type, class_type, union_type)
from ...fable_modules.fable_library.seq import (max_by, iterate, length, item, iterate_indexed, max, is_empty, to_list, delay, collect, singleton, empty, map, try_find_index, filter)
from ...fable_modules.fable_library.string_ import (to_fail, printf, to_console)
from ...fable_modules.fable_library.types import (Array, Union, to_string)
from ...fable_modules.fable_library.util import (safe_hash, compare_primitives, get_enumerator, dispose, ignore, IEnumerable_1, IEnumerator, to_iterator, equals, compare, max as max_1)
from ...fable_modules.fable_library.types import FSharpRef
from ..Helper.collections_ import (ResizeArray_init, ResizeArray_create, ResizeArray_map, ResizeArray_iteri, List_tryPickAndRemove)
from .composite_cell import CompositeCell
from .composite_column import CompositeColumn
from .composite_header import CompositeHeader

def get_empty_cell_for_header(header: CompositeHeader, colum_cell_option: CompositeCell | None=None) -> CompositeCell:
    match_value: bool = header.IsTermColumn
    if match_value:
        (pattern_matching_result,) = (None,)
        if colum_cell_option is None:
            pattern_matching_result = 0

        elif colum_cell_option.tag == 0:
            pattern_matching_result = 0

        elif colum_cell_option.tag == 2:
            pattern_matching_result = 1

        else: 
            pattern_matching_result = 2

        if pattern_matching_result == 0:
            return CompositeCell.empty_term()

        elif pattern_matching_result == 1:
            return CompositeCell.empty_unitized()

        elif pattern_matching_result == 2:
            raise Exception("[extendBodyCells] This should never happen, IsTermColumn header must be paired with either term or unitized cell.")


    else: 
        return CompositeCell.empty_free_text()



def ensure_cell_hash_in_value_map(value: CompositeCell, value_map: Any) -> int:
    hash_1: int = safe_hash(value) or 0
    if hash_1 in value_map:
        return hash_1

    else: 
        add_to_dict(value_map, hash_1, value)
        return hash_1



def _expr821() -> TypeInfo:
    return union_type("ARCtrl.ArcTableAux.ColumnValueRefs", [], ColumnValueRefs, lambda: [[("Item", int32_type)], [("Item", class_type("System.Collections.Generic.Dictionary`2", [int32_type, int32_type]))]])


class ColumnValueRefs(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Constant", "Sparse"]


ColumnValueRefs_reflection = _expr821

def ColumnValueRefs__get_RowCount(this: ColumnValueRefs) -> Any | None:
    if this.tag == 1:
        def projection(kv: Any, this: Any=this) -> int:
            return kv[0]

        class ObjectExpr822:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        return max_by(projection, this.fields[0], ObjectExpr822())

    else: 
        return None



def ColumnValueRefs__Copy(this: ColumnValueRefs) -> ColumnValueRefs:
    if this.tag == 1:
        d: Any = dict([])
        def action(v: Any, this: Any=this) -> None:
            add_to_dict(d, v[0], v[1])

        iterate(action, this.fields[0])
        return ColumnValueRefs(1, d)

    else: 
        return ColumnValueRefs(0, this.fields[0])



def ColumnValueRefs__ToSparse_Z524259A4(this: ColumnValueRefs, row_count: int) -> ColumnValueRefs:
    if this.tag == 1:
        return ColumnValueRefs(1, this.fields[0])

    else: 
        d: Any = dict([])
        for i in range(0, (row_count - 1) + 1, 1):
            add_to_dict(d, i, this.fields[0])
        return ColumnValueRefs(1, d)



def ColumnValueRefs__AsSparse(this: ColumnValueRefs) -> Any:
    if this.tag == 1:
        return this.fields[0]

    else: 
        raise Exception("Cannot convert a constant column to sparse. Use ToSparse first.")



def ColumnValueRefs__AsConstant(this: ColumnValueRefs) -> int:
    if this.tag == 1:
        raise Exception("Cannot convert a sparse column to constant. Use ToSparse first.")

    else: 
        return this.fields[0]



def ColumnValueRefs_fromCellColumn_14896151(column: Any, previous_row_count: int, value_map: Any) -> ColumnValueRefs:
    l: int = length(column) or 0
    cells: Any = dict([])
    if l == 0:
        return ColumnValueRefs(1, cells)

    else: 
        current: ColumnValueRefs
        hash_1: int = ensure_cell_hash_in_value_map(item(0, column), value_map) or 0
        if l >= previous_row_count:
            current = ColumnValueRefs(0, hash_1)

        else: 
            add_to_dict(cells, 0, hash_1)
            current = ColumnValueRefs(1, cells)

        def action(i: int, cell: CompositeCell, column: Any=column, previous_row_count: Any=previous_row_count, value_map: Any=value_map) -> None:
            nonlocal current
            hash_2: int = ensure_cell_hash_in_value_map(cell, value_map) or 0
            if current.tag == 1:
                cells_2: Any = current.fields[0]
                cells_2[i] = hash_2

            elif current.fields[0] == hash_2:
                cell_hash_1: int = current.fields[0] or 0

            else: 
                cell_hash_2: int = current.fields[0] or 0
                cells_1: Any = dict([])
                for j in range(0, (i - 1) + 1, 1):
                    cells_1[j] = cell_hash_2
                cells_1[i] = hash_2
                current = ColumnValueRefs(1, cells_1)


        iterate_indexed(action, column)
        return current



def ColumnValueRefs__ToCellColumn_Z2609C9DD(this: ColumnValueRefs, value_map: Any, row_count: int, header: CompositeHeader) -> Array[CompositeCell]:
    if this.tag == 1:
        values: Any = this.fields[0]
        class ObjectExpr823:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        default_cell: CompositeCell = get_empty_cell_for_header(header, None) if (len(values) == 0) else get_empty_cell_for_header(header, get_item_from_dict(value_map, get_item_from_dict(values, max(values.keys(), ObjectExpr823()) - 1)))
        def _arrow824(i_1: int, this: Any=this, value_map: Any=value_map, row_count: Any=row_count, header: Any=header) -> CompositeCell:
            return get_item_from_dict(value_map, get_item_from_dict(values, i_1)) if (i_1 in values) else default_cell

        return ResizeArray_init(row_count, _arrow824)

    else: 
        return ResizeArray_create(row_count, get_item_from_dict(value_map, this.fields[0]))



def _expr838() -> TypeInfo:
    return class_type("ARCtrl.ArcTableAux.ArcTableValues", None, ArcTableValues)


class ArcTableValues:
    def __init__(self, cols: Any, value_map: Any, row_count: int) -> None:
        self._columns: Any = cols
        self._valueMap: Any = value_map
        self._rowCount: int = row_count or 0

    @property
    def Columns(self, __unit: None=None) -> Any:
        this: ArcTableValues = self
        return this._columns

    @Columns.setter
    def Columns(self, columns: Any) -> None:
        this: ArcTableValues = self
        this._columns = columns

    @property
    def ColumnCount(self, __unit: None=None) -> int:
        this: ArcTableValues = self
        class ObjectExpr825:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        return 0 if is_empty(this._columns) else (1 + max(this._columns.keys(), ObjectExpr825()))

    @property
    def ValueMap(self, __unit: None=None) -> Any:
        this: ArcTableValues = self
        return this._valueMap

    @ValueMap.setter
    def ValueMap(self, value_map: Any) -> None:
        this: ArcTableValues = self
        this._valueMap = value_map

    @property
    def RowCount(self, __unit: None=None) -> int:
        this: ArcTableValues = self
        return this._rowCount

    @RowCount.setter
    def RowCount(self, row_count: int) -> None:
        this: ArcTableValues = self
        if (row_count < this._rowCount) if (row_count > 0) else False:
            enumerator: Any = get_enumerator(this._columns)
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    match_value: ColumnValueRefs = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()[1]
                    if match_value.tag == 1:
                        values: Any = match_value.fields[0]
                        with get_enumerator(to_list(values.keys())) as enumerator_1:
                            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                                key: int = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current() or 0
                                if key >= row_count:
                                    ignore(remove_from_dict(values, key))



            finally: 
                dispose(enumerator)


        this._rowCount = row_count or 0

    @staticmethod
    def from_cell_columns(columns: Array[Array[CompositeCell]]) -> ArcTableValues:
        class ObjectExpr826:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        row_count: int = (0 if (len(columns) == 0) else max(ResizeArray_map(len, columns), ObjectExpr826())) or 0
        value_map: Any = dict([])
        parsed_columns: Any = dict([])
        def action(i: int, column: Array[CompositeCell]) -> None:
            add_to_dict(parsed_columns, i, ColumnValueRefs_fromCellColumn_14896151(column, row_count, value_map))

        iterate_indexed(action, columns)
        return ArcTableValues(parsed_columns, value_map, row_count)

    @staticmethod
    def from_ref_columns(columns: Any, value_map: Any, row_count: int) -> ArcTableValues:
        parsed_columns: Any = dict([])
        def action(i: int, column: ColumnValueRefs) -> None:
            add_to_dict(parsed_columns, i, column)

        iterate_indexed(action, columns)
        return ArcTableValues(parsed_columns, value_map, row_count)

    @staticmethod
    def init(__unit: None=None) -> ArcTableValues:
        value_map: Any = dict([])
        return ArcTableValues(dict([]), value_map, 0)

    def ToCellColumns(self, headers: Array[CompositeHeader]) -> Array[Array[CompositeCell]]:
        this: ArcTableValues = self
        def _arrow827(i: int) -> Array[CompositeCell]:
            header: CompositeHeader = headers[i]
            return ColumnValueRefs__ToCellColumn_Z2609C9DD(get_item_from_dict(this._columns, i), this._valueMap, this._rowCount, header)

        return ResizeArray_init(len(headers), _arrow827)

    def RescanValueMap(self, __unit: None=None) -> None:
        this: ArcTableValues = self
        new_value_map: Any = dict([])
        enumerator: Any = get_enumerator(this._columns)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                match_value: ColumnValueRefs = kv[1]
                if match_value.tag == 1:
                    values: Any = match_value.fields[0]
                    enumerator_1: Any = get_enumerator(values)
                    try: 
                        while enumerator_1.System_Collections_IEnumerator_MoveNext():
                            ckv: Any = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                            hash_2: int = ensure_cell_hash_in_value_map(get_item_from_dict(this._valueMap, ckv[1]), new_value_map) or 0
                            values[ckv[0]] = hash_2

                    finally: 
                        dispose(enumerator_1)


                else: 
                    hash_1: int = ensure_cell_hash_in_value_map(get_item_from_dict(this._valueMap, match_value.fields[0]), new_value_map) or 0
                    this._columns[kv[0]] = ColumnValueRefs(0, hash_1)


        finally: 
            dispose(enumerator)

        this._valueMap = new_value_map

    def Copy(self, __unit: None=None) -> ArcTableValues:
        this: ArcTableValues = self
        next_value_map: Any = dict([])
        def action(kv: Any) -> None:
            add_to_dict(next_value_map, kv[0], kv[1].Copy())

        iterate(action, this._valueMap)
        next_columns: Any = dict([])
        def action_1(kv_1: Any) -> None:
            add_to_dict(next_columns, kv_1[0], ColumnValueRefs__Copy(kv_1[1]))

        iterate(action_1, this._columns)
        return ArcTableValues(next_columns, next_value_map, this._rowCount)

    def __hash__(self, __unit: None=None) -> int:
        this: ArcTableValues = self
        hash_1: int = 0
        for i in range(0, (this.ColumnCount - 1) + 1, 1):
            match_value: ColumnValueRefs | None
            pattern_input: tuple[bool, ColumnValueRefs]
            out_arg: ColumnValueRefs = None
            def _arrow828(__unit: None=None) -> ColumnValueRefs:
                return out_arg

            def _arrow829(v: ColumnValueRefs) -> None:
                nonlocal out_arg
                out_arg = v

            pattern_input = (try_get_value(this._columns, i, FSharpRef(_arrow828, _arrow829)), out_arg)
            match_value = pattern_input[1] if pattern_input[0] else None
            if match_value is not None:
                if match_value.tag == 1:
                    values: Any = match_value.fields[0]
                    enumerator: Any = get_enumerator(values)
                    try: 
                        while enumerator.System_Collections_IEnumerator_MoveNext():
                            kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                            hash_1 = (((-1640531527 + kv[0]) + (hash_1 << 6)) + (hash_1 >> 2)) or 0
                            hash_1 = (((-1640531527 + kv[1]) + (hash_1 << 6)) + (hash_1 >> 2)) or 0

                    finally: 
                        dispose(enumerator)


                else: 
                    value_hash: int = match_value.fields[0] or 0
                    for i_1 in range(0, (this._rowCount - 1) + 1, 1):
                        hash_1 = (((-1640531527 + i_1) + (hash_1 << 6)) + (hash_1 >> 2)) or 0
                        hash_1 = (((-1640531527 + value_hash) + (hash_1 << 6)) + (hash_1 >> 2)) or 0


        return hash_1

    def __eq__(self, other: Any=None) -> bool:
        this: ArcTableValues = self
        return (safe_hash(this) == safe_hash(other)) if isinstance(other, ArcTableValues) else False

    def Item(self, cr_indices: tuple[int, int]) -> CompositeCell:
        this: ArcTableValues = self
        row: int = cr_indices[1] or 0
        col: int = cr_indices[0] or 0
        if row > (this.RowCount - 1):
            arg_1: int = this.RowCount or 0
            to_fail(printf("Row index %d is out of bounds for ArcTableValues with row count %d."))(row)(arg_1)

        if col > (this.ColumnCount - 1):
            arg_3: int = this.ColumnCount or 0
            to_fail(printf("Column index %d is out of bounds for ArcTableValues with column count %d."))(col)(arg_3)

        match_value: ColumnValueRefs | None
        pattern_input: tuple[bool, ColumnValueRefs]
        out_arg: ColumnValueRefs = None
        def _arrow830(__unit: None=None) -> ColumnValueRefs:
            return out_arg

        def _arrow831(v: ColumnValueRefs) -> None:
            nonlocal out_arg
            out_arg = v

        pattern_input = (try_get_value(this._columns, col, FSharpRef(_arrow830, _arrow831)), out_arg)
        match_value = pattern_input[1] if pattern_input[0] else None
        if match_value is not None:
            col_value_refs: ColumnValueRefs = match_value
            if col_value_refs.tag == 1:
                values: Any = col_value_refs.fields[0]
                return get_item_from_dict(this._valueMap, get_item_from_dict(values, row)) if (row in values) else to_fail(printf("Row value for index %d does not exist in column %d of ArcTableValues."))(row)(col)

            else: 
                return get_item_from_dict(this._valueMap, col_value_refs.fields[0])


        else: 
            return to_fail(printf("Column %d does not exist in ArcTableValues."))(col)


    def GetEnumerator(self, __unit: None=None) -> IEnumerator[Any]:
        this: ArcTableValues = self
        def _arrow837(__unit: None=None) -> IEnumerable_1[Any]:
            def _arrow836(col_i: int) -> IEnumerable_1[Any]:
                match_value: ColumnValueRefs | None
                pattern_input: tuple[bool, ColumnValueRefs]
                out_arg: ColumnValueRefs = None
                def _arrow832(__unit: None=None) -> ColumnValueRefs:
                    return out_arg

                def _arrow833(v: ColumnValueRefs) -> None:
                    nonlocal out_arg
                    out_arg = v

                pattern_input = (try_get_value(this._columns, col_i, FSharpRef(_arrow832, _arrow833)), out_arg)
                match_value = pattern_input[1] if pattern_input[0] else None
                if match_value is not None:
                    match_value_1: ColumnValueRefs = match_value
                    if match_value_1.tag == 1:
                        values: Any = match_value_1.fields[0]
                        def _arrow834(row_i_1: int) -> IEnumerable_1[Any]:
                            return singleton(((col_i, row_i_1), get_item_from_dict(this._valueMap, get_item_from_dict(values, row_i_1)))) if (row_i_1 in values) else empty()

                        return collect(_arrow834, range_big_int(0, 1, this._rowCount - 1))

                    else: 
                        def _arrow835(row_i: int) -> tuple[tuple[int, int], CompositeCell]:
                            return ((col_i, row_i), get_item_from_dict(this._valueMap, match_value_1.fields[0]))

                        return map(_arrow835, range_big_int(0, 1, this._rowCount - 1))


                else: 
                    return empty()


            return collect(_arrow836, range_big_int(0, 1, this.ColumnCount - 1))

        return get_enumerator(delay(_arrow837))

    def __iter__(self) -> IEnumerator[Any]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None=None) -> IEnumerator[Any]:
        this: ArcTableValues = self
        return get_enumerator(this)


ArcTableValues_reflection = _expr838

def ArcTableValues__ctor_39436F7C(cols: Any, value_map: Any, row_count: int) -> ArcTableValues:
    return ArcTableValues(cols, value_map, row_count)


def _007CIsUniqueExistingHeader_007C__007C(existing_headers: IEnumerable_1[CompositeHeader], input: CompositeHeader) -> int | None:
    if ((((input.tag == 3) or (input.tag == 2)) or (input.tag == 1)) or (input.tag == 0)) or (input.tag == 13):
        return None

    elif input.tag == 12:
        def _arrow839(h: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return True if (h.tag == 12) else False

        return try_find_index(_arrow839, existing_headers)

    elif input.tag == 11:
        def _arrow840(h_1: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return True if (h_1.tag == 11) else False

        return try_find_index(_arrow840, existing_headers)

    else: 
        def _arrow841(h_2: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return equals(h_2, input)

        return try_find_index(_arrow841, existing_headers)



def try_find_duplicate_unique(new_header: CompositeHeader, existing_headers: IEnumerable_1[CompositeHeader]) -> int | None:
    active_pattern_result: int | None = _007CIsUniqueExistingHeader_007C__007C(existing_headers, new_header)
    if active_pattern_result is not None:
        index: int = active_pattern_result or 0
        return index

    else: 
        return None



def try_find_duplicate_unique_in_array(existing_headers: IEnumerable_1[CompositeHeader]) -> FSharpList[dict[str, Any]]:
    def loop(i_mut: int, duplicate_list_mut: FSharpList[dict[str, Any]], header_list_mut: FSharpList[CompositeHeader], existing_headers: Any=existing_headers) -> FSharpList[dict[str, Any]]:
        while True:
            (i, duplicate_list, header_list) = (i_mut, duplicate_list_mut, header_list_mut)
            (pattern_matching_result, header, tail) = (None, None, None)
            if is_empty_1(header_list):
                pattern_matching_result = 0

            elif is_empty_1(tail_1(header_list)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1
                header = head(header_list)
                tail = tail_1(header_list)

            if pattern_matching_result == 0:
                return duplicate_list

            elif pattern_matching_result == 1:
                has_duplicate: int | None = try_find_duplicate_unique(header, tail)
                i_mut = i + 1
                duplicate_list_mut = cons({
                    "HeaderType": header,
                    "Index1": i,
                    "Index2": value_3(has_duplicate)
                }, duplicate_list) if (has_duplicate is not None) else duplicate_list
                header_list_mut = tail
                continue

            break

    def predicate(x: CompositeHeader, existing_headers: Any=existing_headers) -> bool:
        return not x.IsTermColumn

    return loop(0, empty_1(), of_seq(filter(predicate, existing_headers)))


def SanityChecks_validateColumnIndex(index: int, column_count: int, allow_append: bool) -> None:
    if index < 0:
        raise Exception("Cannot insert CompositeColumn at index < 0.")

    def _arrow842(__unit: None=None, index: Any=index, column_count: Any=column_count, allow_append: Any=allow_append) -> bool:
        x: int = index or 0
        y: int = column_count or 0
        return (compare(x, y) > 0) if allow_append else (compare(x, y) >= 0)

    if _arrow842():
        raise Exception(("Specified index is out of table range! Table contains only " + str(column_count)) + " columns.")



def SanityChecks_validateRowIndex(index: int, row_count: int, allow_append: bool) -> None:
    if index < 0:
        raise Exception("Cannot insert CompositeColumn at index < 0.")

    def _arrow843(__unit: None=None, index: Any=index, row_count: Any=row_count, allow_append: Any=allow_append) -> bool:
        x: int = index or 0
        y: int = row_count or 0
        return (compare(x, y) > 0) if allow_append else (compare(x, y) >= 0)

    if _arrow843():
        raise Exception(("Specified index is out of table range! Table contains only " + str(row_count)) + " rows.")



def SanityChecks_validateColumn(column: CompositeColumn) -> None:
    ignore(column.Validate(True))


def SanityChecks_validateCellColumns(headers: Array[CompositeHeader], columns: Array[Array[CompositeCell]], raise_exception: bool) -> bool:
    is_valid: bool = True
    en: Any = get_enumerator(headers)
    col_index: int = 0
    if (len(columns) != 0) if (len(headers) != len(columns)) else False:
        def _arrow844(message: str, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> None:
            raise Exception(message)

        def _arrow846(__unit: None=None, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> Callable[[str], None]:
            clo: Callable[[str], None] = to_console(printf("%s"))
            def _arrow845(arg: str) -> None:
                clo(arg)

            return _arrow845

        (_arrow844 if raise_exception else _arrow846())(((("Invalid table. Number of headers (" + str(len(headers))) + ") does not match number of columns (") + str(len(columns))) + ").")
        is_valid = False

    while (len(columns) != 0) if (en.System_Collections_IEnumerator_MoveNext() if is_valid else False) else False:
        header: CompositeHeader = en.System_Collections_Generic_IEnumerator_1_get_Current()
        col_en: Any = get_enumerator(columns[col_index])
        col_index = (col_index + 1) or 0
        while col_en.System_Collections_IEnumerator_MoveNext() if is_valid else False:
            cell: CompositeCell = col_en.System_Collections_Generic_IEnumerator_1_get_Current()
            header_is_data: bool = header.IsDataColumn
            header_is_freetext: bool = (not header.IsDataColumn) if (not header.IsTermColumn) else False
            cell_is_not_freetext: bool = not cell.is_free_text
            if (cell_is_not_freetext if (not cell.is_data) else False) if header_is_data else False:
                def _arrow847(message_1: str, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> None:
                    raise Exception(message_1)

                def _arrow849(__unit: None=None, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> Callable[[str], None]:
                    clo_1: Callable[[str], None] = to_console(printf("%s"))
                    def _arrow848(arg_1: str) -> None:
                        clo_1(arg_1)

                    return _arrow848

                (_arrow847 if raise_exception else _arrow849())(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`. Data header should contain either Data or Freetext cells.")
                is_valid = False

            if cell_is_not_freetext if header_is_freetext else False:
                def _arrow850(message_2: str, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> None:
                    raise Exception(message_2)

                def _arrow852(__unit: None=None, headers: Any=headers, columns: Any=columns, raise_exception: Any=raise_exception) -> Callable[[str], None]:
                    clo_2: Callable[[str], None] = to_console(printf("%s"))
                    def _arrow851(arg_2: str) -> None:
                        clo_2(arg_2)

                    return _arrow851

                (_arrow850 if raise_exception else _arrow852())(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`. Freetext header should not contain non-freetext cells.")
                is_valid = False

    return is_valid


def SanityChecks_validateArcTableValues(headers: Array[CompositeHeader], values: ArcTableValues, raise_exception: bool) -> bool:
    is_valid: bool = True
    col_index: int = 0
    if (values.ColumnCount != 0) if (len(headers) != values.ColumnCount) else False:
        def _arrow853(message: str, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> None:
            raise Exception(message)

        def _arrow855(__unit: None=None, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> Callable[[str], None]:
            clo: Callable[[str], None] = to_console(printf("%s"))
            def _arrow854(arg: str) -> None:
                clo(arg)

            return _arrow854

        (_arrow853 if raise_exception else _arrow855())(((("Invalid table. Number of headers (" + str(len(headers))) + ") does not match number of columns (") + str(values.ColumnCount)) + ").")
        is_valid = False

    if (values.ColumnCount != 0) if (values.RowCount != 0) else False:
        while (col_index < values.ColumnCount) if is_valid else False:
            header: CompositeHeader = headers[col_index]
            match_value: ColumnValueRefs | None
            key: int = col_index or 0
            pattern_input: tuple[bool, ColumnValueRefs]
            out_arg: ColumnValueRefs = None
            def _arrow856(__unit: None=None, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> ColumnValueRefs:
                return out_arg

            def _arrow857(v: ColumnValueRefs, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> None:
                nonlocal out_arg
                out_arg = v

            pattern_input = (try_get_value(values.Columns, key, FSharpRef(_arrow856, _arrow857)), out_arg)
            match_value = pattern_input[1] if pattern_input[0] else None
            if match_value is not None:
                if match_value.tag == 1:
                    column: Any = match_value.fields[0]
                    enumerator: Any = get_enumerator(column)
                    try: 
                        while enumerator.System_Collections_IEnumerator_MoveNext():
                            kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                            cell_1: CompositeCell = get_item_from_dict(values.ValueMap, kv[1])
                            if not cell_1.ValidateAgainstHeader(header, raise_exception):
                                is_valid = False


                    finally: 
                        dispose(enumerator)


                else: 
                    hash_1: int = match_value.fields[0] or 0
                    cell: CompositeCell = get_item_from_dict(values.ValueMap, hash_1)
                    if not cell.ValidateAgainstHeader(header, raise_exception):
                        is_valid = False



            col_index = (col_index + 1) or 0

    return is_valid


def Unchecked_tryGetCellAt(column: int, row: int, values: ArcTableValues) -> CompositeCell | None:
    def binder(col: ColumnValueRefs, column: Any=column, row: Any=row, values: Any=values) -> CompositeCell | None:
        if col.tag == 1:
            vals: Any = col.fields[0]
            if row in vals:
                return get_item_from_dict(values.ValueMap, get_item_from_dict(vals, row))

            else: 
                return None


        else: 
            return get_item_from_dict(values.ValueMap, col.fields[0])


    def _arrow860(__unit: None=None, column: Any=column, row: Any=row, values: Any=values) -> ColumnValueRefs | None:
        pattern_input: tuple[bool, ColumnValueRefs]
        out_arg: ColumnValueRefs = None
        def _arrow858(__unit: None=None) -> ColumnValueRefs:
            return out_arg

        def _arrow859(v: ColumnValueRefs) -> None:
            nonlocal out_arg
            out_arg = v

        pattern_input = (try_get_value(values.Columns, column, FSharpRef(_arrow858, _arrow859)), out_arg)
        return pattern_input[1] if pattern_input[0] else None

    return bind(binder, _arrow860())


def Unchecked_getCellWithDefault(column: int, row: int, headers: Array[CompositeHeader], values: ArcTableValues) -> CompositeCell:
    if len(headers) <= column:
        arg_1: int = len(headers) or 0
        to_fail(printf("Column index %d is out of bounds for ArcTableValues with column count %d."))(column)(arg_1)

    match_value: ColumnValueRefs | None
    pattern_input: tuple[bool, ColumnValueRefs]
    out_arg: ColumnValueRefs = None
    def _arrow861(__unit: None=None, column: Any=column, row: Any=row, headers: Any=headers, values: Any=values) -> ColumnValueRefs:
        return out_arg

    def _arrow862(v: ColumnValueRefs, column: Any=column, row: Any=row, headers: Any=headers, values: Any=values) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(values.Columns, column, FSharpRef(_arrow861, _arrow862)), out_arg)
    match_value = pattern_input[1] if pattern_input[0] else None
    if match_value is None:
        if row < values.RowCount:
            return CompositeCell.empty_free_text()

        else: 
            return get_empty_cell_for_header(headers[column], None)


    else: 
        col: ColumnValueRefs = match_value
        if col.tag == 1:
            vals: Any = col.fields[0]
            if row in vals:
                return get_item_from_dict(values.ValueMap, get_item_from_dict(vals, row))

            elif len(vals) == 0:
                return get_empty_cell_for_header(headers[column], None)

            else: 
                header_1: CompositeHeader = headers[column]
                class ObjectExpr863:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                max_i: int = max(vals.keys(), ObjectExpr863()) or 0
                return get_empty_cell_for_header(header_1, get_item_from_dict(values.ValueMap, get_item_from_dict(vals, max_i)))


        else: 
            return get_item_from_dict(values.ValueMap, col.fields[0])




def Unchecked_setCellAt(column_index: int, row_index: int, c: CompositeCell, values: ArcTableValues) -> None:
    if (row_index + 1) > values.RowCount:
        values.RowCount = (row_index + 1) or 0

    match_value: ColumnValueRefs | None
    pattern_input: tuple[bool, ColumnValueRefs]
    out_arg: ColumnValueRefs = None
    def _arrow864(__unit: None=None, column_index: Any=column_index, row_index: Any=row_index, c: Any=c, values: Any=values) -> ColumnValueRefs:
        return out_arg

    def _arrow865(v: ColumnValueRefs, column_index: Any=column_index, row_index: Any=row_index, c: Any=c, values: Any=values) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(values.Columns, column_index, FSharpRef(_arrow864, _arrow865)), out_arg)
    match_value = pattern_input[1] if pattern_input[0] else None
    if match_value is not None:
        col: ColumnValueRefs = match_value
        if col.tag == 1:
            key_1: int = row_index or 0
            value: int = ensure_cell_hash_in_value_map(c, values.ValueMap) or 0
            dict_1_1: Any = col.fields[0]
            if key_1 in dict_1_1:
                dict_1_1[key_1] = value

            else: 
                add_to_dict(dict_1_1, key_1, value)


        else: 
            value_hash: int = col.fields[0] or 0
            hash_3: int = ensure_cell_hash_in_value_map(c, values.ValueMap) or 0
            if hash_3 == value_hash:
                pass

            else: 
                d: Any = dict([])
                for i in range(0, (values.RowCount - 1) + 1, 1):
                    if i == row_index:
                        add_to_dict(d, i, hash_3)

                    else: 
                        add_to_dict(d, i, value_hash)

                values.Columns[column_index] = ColumnValueRefs(1, d)



    elif (row_index == 0) if (values.RowCount <= 1) else False:
        hash_1: int = ensure_cell_hash_in_value_map(c, values.ValueMap) or 0
        add_to_dict(values.Columns, column_index, ColumnValueRefs(0, hash_1))

    else: 
        new_column: Any = dict([])
        add_to_dict(new_column, row_index, ensure_cell_hash_in_value_map(c, values.ValueMap))
        add_to_dict(values.Columns, column_index, ColumnValueRefs(1, new_column))



def Unchecked_removeCellAt(column_index: int, row_index: int, values: ArcTableValues) -> None:
    match_value: ColumnValueRefs | None
    pattern_input: tuple[bool, ColumnValueRefs]
    out_arg: ColumnValueRefs = None
    def _arrow866(__unit: None=None, column_index: Any=column_index, row_index: Any=row_index, values: Any=values) -> ColumnValueRefs:
        return out_arg

    def _arrow867(v: ColumnValueRefs, column_index: Any=column_index, row_index: Any=row_index, values: Any=values) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(values.Columns, column_index, FSharpRef(_arrow866, _arrow867)), out_arg)
    match_value = pattern_input[1] if pattern_input[0] else None
    if match_value is not None:
        col: ColumnValueRefs = match_value
        if col.tag == 1:
            vals: Any = col.fields[0]
            if row_index in vals:
                ignore(remove_from_dict(vals, row_index))
                if len(vals) == 0:
                    ignore(remove_from_dict(values.Columns, column_index))



        elif (values.RowCount == 1) if (row_index == 0) else False:
            ignore(remove_from_dict(values.Columns, column_index))




def Unchecked_moveCellTo(from_col: int, from_row: int, to_col: int, to_row: int, values: ArcTableValues) -> None:
    match_value: CompositeCell | None = Unchecked_tryGetCellAt(from_col, from_row, values)
    if match_value is None:
        pass

    else: 
        cell: CompositeCell = match_value
        Unchecked_removeCellAt(from_col, from_row, values)
        Unchecked_setCellAt(to_col, to_row, cell, values)



def Unchecked_removeHeader(index: int, headers: Array[CompositeHeader]) -> None:
    headers.pop(index)


def Unchecked_removeColumnCells(col_index: int, values: ArcTableValues) -> None:
    ignore(remove_from_dict(values.Columns, col_index))


def Unchecked_removeColumnCells_withIndexChange(col_index: int, column_count: int, values: ArcTableValues) -> None:
    if col_index < (column_count - 1):
        cols: Any = dict([])
        def action(kv: Any, col_index: Any=col_index, column_count: Any=column_count, values: Any=values) -> None:
            c_i: int = kv[0] or 0
            if c_i > col_index:
                add_to_dict(cols, c_i - 1, kv[1])

            elif c_i < col_index:
                add_to_dict(cols, c_i, kv[1])


        iterate(action, values.Columns)
        values.Columns = cols

    else: 
        value: None = Unchecked_removeColumnCells(col_index, values)
        ignore(None)



def Unchecked_removeRowCells(row_index: int, column_count: int, values: ArcTableValues) -> None:
    for c in range(0, (column_count - 1) + 1, 1):
        Unchecked_removeCellAt(c, row_index, values)


def Unchecked_removeRowCells_withIndexChange(row_index: int, values: ArcTableValues) -> None:
    if (values.RowCount == 1) if (row_index == 0) else False:
        values.RowCount = 0
        values.Columns = dict([])

    else: 
        def action_1(kv: Any, row_index: Any=row_index, values: Any=values) -> None:
            match_value: ColumnValueRefs = kv[1]
            if match_value.tag == 1:
                vals: Any = match_value.fields[0]
                if row_index < (values.RowCount - 1):
                    col: Any = dict([])
                    def action(kv_1: Any, kv: Any=kv) -> None:
                        r_i: int = kv_1[0] or 0
                        if r_i > row_index:
                            add_to_dict(col, r_i - 1, kv_1[1])

                        elif r_i < row_index:
                            add_to_dict(col, r_i, kv_1[1])


                    iterate(action, vals)
                    values.Columns[kv[0]] = ColumnValueRefs(1, col)

                else: 
                    ignore(remove_from_dict(vals, row_index))



        iterate(action_1, values.Columns)
        values.RowCount = (values.RowCount - 1) or 0



def Unchecked_removeRowRange_withIndexChange(row_start_index: int, row_end_index: int, values: ArcTableValues) -> None:
    if (values.RowCount == row_end_index) if (row_start_index == 0) else False:
        values.RowCount = 0
        values.Columns = dict([])

    else: 
        def action_1(kv: Any, row_start_index: Any=row_start_index, row_end_index: Any=row_end_index, values: Any=values) -> None:
            match_value: ColumnValueRefs = kv[1]
            if match_value.tag == 1:
                vals: Any = match_value.fields[0]
                range: int = ((row_end_index - row_start_index) + 1) or 0
                if row_end_index < (values.RowCount - 1):
                    col: Any = dict([])
                    def action(kv_1: Any, kv: Any=kv) -> None:
                        r_i: int = kv_1[0] or 0
                        if r_i > row_end_index:
                            add_to_dict(col, r_i - range, kv_1[1])

                        elif r_i < row_start_index:
                            add_to_dict(col, r_i, kv_1[1])


                    iterate(action, vals)
                    values.Columns[kv[0]] = ColumnValueRefs(1, col)

                else: 
                    for row_index in range(row_start_index, row_end_index + 1, 1):
                        ignore(remove_from_dict(vals, row_index))



        iterate(action_1, values.Columns)
        values.RowCount = (values.RowCount - ((row_end_index - row_start_index) + 1)) or 0



def Unchecked_moveColumnCellsTo(from_col: int, to_col: int, values: ArcTableValues) -> None:
    match_value: ColumnValueRefs | None
    pattern_input: tuple[bool, ColumnValueRefs]
    out_arg: ColumnValueRefs = None
    def _arrow868(__unit: None=None, from_col: Any=from_col, to_col: Any=to_col, values: Any=values) -> ColumnValueRefs:
        return out_arg

    def _arrow869(v: ColumnValueRefs, from_col: Any=from_col, to_col: Any=to_col, values: Any=values) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(values.Columns, from_col, FSharpRef(_arrow868, _arrow869)), out_arg)
    match_value = pattern_input[1] if pattern_input[0] else None
    if match_value is not None:
        col: ColumnValueRefs = match_value
        Unchecked_removeColumnCells(from_col, values)
        key_1: int = to_col or 0
        value: ColumnValueRefs = col
        dict_1_1: Any = values.Columns
        if key_1 in dict_1_1:
            dict_1_1[key_1] = value

        else: 
            add_to_dict(dict_1_1, key_1, value)




def Unchecked_addRefColumn(new_header: CompositeHeader, new_col: ColumnValueRefs, row_count: int, index: int, force_replace: bool, only_headers: bool, headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    number_of_new_columns: int = 1
    index_1: int = index or 0
    has_duplicate_unique: int | None = try_find_duplicate_unique(new_header, headers)
    if (has_duplicate_unique is not None) if (not force_replace) else False:
        raise Exception(((("Invalid new column `" + str(new_header)) + "`. Table already contains header of the same type on index `") + str(value_3(has_duplicate_unique))) + "`")

    if row_count > values.RowCount:
        values.RowCount = row_count or 0
        enumerator: Any = get_enumerator(values.Columns)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                values.Columns[kv[0]] = ColumnValueRefs__ToSparse_Z524259A4(kv[1], values.RowCount)

        finally: 
            dispose(enumerator)


    if (len(values.Columns) == 1) if (force_replace if ((has_duplicate_unique is not None) if (row_count < values.RowCount) else False) else False) else False:
        values.RowCount = row_count or 0

    if has_duplicate_unique is not None:
        number_of_new_columns = 0
        index_1 = value_3(has_duplicate_unique) or 0

    match_value: int = len(headers) or 0
    match_value_1: int = values.RowCount or 0
    start_col_count: int = match_value or 0
    if has_duplicate_unique is not None:
        Unchecked_removeHeader(index_1, headers)

    headers.insert(index_1, new_header)
    if (has_duplicate_unique is None) if (index_1 < start_col_count) else False:
        def _arrow870(x: int, y: int, new_header: Any=new_header, new_col: Any=new_col, row_count: Any=row_count, index: Any=index, force_replace: Any=force_replace, only_headers: Any=only_headers, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_column_index: int = max_1(_arrow870, start_col_count - 1, 0) or 0
        for column_index in range(last_column_index, index_1 - 1, -1):
            Unchecked_moveColumnCellsTo(column_index, column_index + number_of_new_columns, values)

    if not only_headers:
        key: int = index_1 or 0
        value: ColumnValueRefs = new_col
        dict_1: Any = values.Columns
        if key in dict_1:
            dict_1[key] = value

        else: 
            add_to_dict(dict_1, key, value)




def Unchecked_addColumn(new_header: CompositeHeader, new_cells: Any, index: int, force_replace: bool, only_headers: bool, headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    Unchecked_addRefColumn(new_header, ColumnValueRefs_fromCellColumn_14896151(new_cells, values.RowCount, values.ValueMap), length(new_cells), index, force_replace, only_headers, headers, values)


def Unchecked_addColumnFill(new_header: CompositeHeader, new_cell: CompositeCell, index: int, force_replace: bool, only_headers: bool, headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    Unchecked_addRefColumn(new_header, ColumnValueRefs(0, ensure_cell_hash_in_value_map(new_cell, values.ValueMap)), 1, index, force_replace, only_headers, headers, values)


def Unchecked_fillMissingCells(headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    if values.RowCount == 0:
        pass

    else: 
        for i in range(0, (values.ColumnCount - 1) + 1, 1):
            match_value: ColumnValueRefs | None
            pattern_input: tuple[bool, ColumnValueRefs]
            out_arg: ColumnValueRefs = None
            def _arrow871(__unit: None=None, headers: Any=headers, values: Any=values) -> ColumnValueRefs:
                return out_arg

            def _arrow872(v: ColumnValueRefs, headers: Any=headers, values: Any=values) -> None:
                nonlocal out_arg
                out_arg = v

            pattern_input = (try_get_value(values.Columns, i, FSharpRef(_arrow871, _arrow872)), out_arg)
            match_value = pattern_input[1] if pattern_input[0] else None
            if match_value is not None:
                if match_value.tag == 1:
                    vals: Any = match_value.fields[0]
                    if len(vals) < values.RowCount:
                        header: CompositeHeader = headers[i]
                        def _arrow874(__unit: None=None, headers: Any=headers, values: Any=values) -> CompositeCell:
                            class ObjectExpr873:
                                @property
                                def Compare(self) -> Callable[[int, int], int]:
                                    return compare_primitives

                            i_1: int = max(vals.keys(), ObjectExpr873()) or 0
                            return get_empty_cell_for_header(header, get_item_from_dict(values.ValueMap, get_item_from_dict(vals, i_1)))

                        default_hash: int = ensure_cell_hash_in_value_map(get_empty_cell_for_header(header, None) if (len(vals) == 0) else _arrow874(), values.ValueMap) or 0
                        for j in range(len(vals), (values.RowCount - 1) + 1, 1):
                            if not (j in vals):
                                add_to_dict(vals, j, default_hash)




            else: 
                col: ColumnValueRefs = ColumnValueRefs(0, ensure_cell_hash_in_value_map(get_empty_cell_for_header(headers[i], None), values.ValueMap))
                value: None = add_to_dict(values.Columns, i, col)
                ignore(None)




def Unchecked_addEmptyRow(index: int, values: ArcTableValues) -> None:
    if (values.ColumnCount != 0) if (index < values.RowCount) else False:
        enumerator: Any = get_enumerator(values.Columns)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                match_value: ColumnValueRefs = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()[1]
                if match_value.tag == 1:
                    dict_1: Any = match_value.fields[0]
                    class ObjectExpr875:
                        @property
                        def Compare(self) -> Callable[[int, int], int]:
                            return compare_primitives

                    max_index: int = max(dict_1.keys(), ObjectExpr875()) or 0
                    for i in range(max_index, ((index + 1) - 1) - 1, -1):
                        if i in dict_1:
                            v: int = get_item_from_dict(dict_1, i) or 0
                            ignore(remove_from_dict(dict_1, i))
                            add_to_dict(dict_1, i + 1, v)



        finally: 
            dispose(enumerator)


    values.RowCount = (values.RowCount + 1) or 0


def Unchecked_addRow(index: int, new_cells: Array[CompositeCell], headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    row_count: int = values.RowCount or 0
    column_count: int = values.ColumnCount or 0
    increase_row_indices: None
    if index < row_count:
        def _arrow876(x: int, y: int, index: Any=index, new_cells: Any=new_cells, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_row_index: int = max_1(_arrow876, row_count - 1, 0) or 0
        for row_index in range(last_row_index, index - 1, -1):
            for column_index in range(0, (column_count - 1) + 1, 1):
                Unchecked_moveCellTo(column_index, row_index, column_index, row_index + 1, values)

    else: 
        increase_row_indices = None

    def f(column_index_1: int, cell: CompositeCell, index: Any=index, new_cells: Any=new_cells, headers: Any=headers, values: Any=values) -> None:
        Unchecked_setCellAt(column_index_1, index, cell, values)

    set_new_cells: None = ResizeArray_iteri(f, new_cells)


def Unchecked_addRows(index: int, new_rows: Array[Array[CompositeCell]], headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    row_count: int = values.RowCount or 0
    column_count: int = values.ColumnCount or 0
    num_new_rows: int = len(new_rows) or 0
    increase_row_indices: None
    if index < row_count:
        def _arrow877(x: int, y: int, index: Any=index, new_rows: Any=new_rows, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_row_index: int = max_1(_arrow877, row_count - 1, 0) or 0
        for row_index in range(last_row_index, index - 1, -1):
            for column_index in range(0, (column_count - 1) + 1, 1):
                Unchecked_moveCellTo(column_index, row_index, column_index, row_index + num_new_rows, values)

    else: 
        increase_row_indices = None

    current_row_index: int = index or 0
    enumerator: Any = get_enumerator(new_rows)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            def f(column_index_1: int, cell: CompositeCell) -> None:
                Unchecked_setCellAt(column_index_1, current_row_index, cell, values)

            set_new_cells: None = ResizeArray_iteri(f, enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
            current_row_index = (current_row_index + 1) or 0

    finally: 
        dispose(enumerator)



def Unchecked_compositeHeaderMainColumnEqual(ch1: CompositeHeader, ch2: CompositeHeader) -> bool:
    return to_string(ch1) == to_string(ch2)


def Unchecked_moveColumnTo(from_col: int, to_col: int, headers: Array[CompositeHeader], values: ArcTableValues) -> None:
    pattern_input: tuple[int, int, int] = ((-1, from_col + 1, to_col)) if (from_col < to_col) else ((1, from_col - 1, to_col))
    shift_start: int = pattern_input[1] or 0
    shift_end: int = pattern_input[2] or 0
    shift: int = pattern_input[0] or 0
    header: CompositeHeader = headers[from_col]
    with get_enumerator(to_list(range_big_int(shift_start, op_unary_negation_int32(shift), shift_end))) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            c: int = enumerator.System_Collections_Generic_IEnumerator_1_get_Current() or 0
            headers[c + shift] = headers[c]
    headers[to_col] = header
    col: ColumnValueRefs = get_item_from_dict(values.Columns, from_col)
    with get_enumerator(to_list(range_big_int(shift_start, op_unary_negation_int32(shift), shift_end))) as enumerator_1:
        while enumerator_1.System_Collections_IEnumerator_MoveNext():
            c_1: int = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current() or 0
            values.Columns[c_1 + shift] = get_item_from_dict(values.Columns, c_1)
    values.Columns[to_col] = col


def Unchecked_alignByHeaders(keep_order: bool, rows: FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]) -> tuple[Array[CompositeHeader], ArcTableValues]:
    headers: Array[CompositeHeader] = []
    values: ArcTableValues = ArcTableValues.init()
    values.RowCount = length_1(rows) or 0
    def loop(col_i_mut: int, rows_2_mut: FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]], keep_order: Any=keep_order, rows: Any=rows) -> tuple[Array[CompositeHeader], ArcTableValues]:
        while True:
            (col_i, rows_2) = (col_i_mut, rows_2_mut)
            def _arrow878(arg: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> bool:
                return not is_empty_1(arg)

            if not exists(_arrow878, rows_2):
                return (headers, values)

            else: 
                def _arrow879(l: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> tuple[CompositeHeader, CompositeCell] | None:
                    return None if is_empty_1(l) else head(l)

                first_elem: CompositeHeader = pick(_arrow879, rows_2)[0]
                (headers.append(first_elem))
                col_i_mut = col_i + 1
                def mapping(row_i: int, l_1: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> FSharpList[tuple[CompositeHeader, CompositeCell]]:
                    if keep_order:
                        if not is_empty_1(l_1):
                            if Unchecked_compositeHeaderMainColumnEqual(head(l_1)[0], first_elem):
                                Unchecked_setCellAt(col_i, row_i, head(l_1)[1], values)
                                return tail_1(l_1)

                            else: 
                                return l_1


                        else: 
                            return empty_1()


                    else: 
                        def f(tupled_arg: tuple[CompositeHeader, CompositeCell], row_i: Any=row_i, l_1: Any=l_1) -> CompositeCell | None:
                            if Unchecked_compositeHeaderMainColumnEqual(tupled_arg[0], first_elem):
                                return tupled_arg[1]

                            else: 
                                return None


                        pattern_input: tuple[CompositeCell | None, FSharpList[tuple[CompositeHeader, CompositeCell]]] = List_tryPickAndRemove(f, l_1)
                        new_l: FSharpList[tuple[CompositeHeader, CompositeCell]] = pattern_input[1]
                        first_match: CompositeCell | None = pattern_input[0]
                        if first_match is None:
                            return new_l

                        else: 
                            Unchecked_setCellAt(col_i, row_i, first_match, values)
                            return new_l



                rows_2_mut = map_indexed(mapping, rows_2)
                continue

            break

    return loop(0, rows)


__all__ = ["get_empty_cell_for_header", "ensure_cell_hash_in_value_map", "ColumnValueRefs_reflection", "ColumnValueRefs__get_RowCount", "ColumnValueRefs__Copy", "ColumnValueRefs__ToSparse_Z524259A4", "ColumnValueRefs__AsSparse", "ColumnValueRefs__AsConstant", "ColumnValueRefs_fromCellColumn_14896151", "ColumnValueRefs__ToCellColumn_Z2609C9DD", "ArcTableValues_reflection", "_007CIsUniqueExistingHeader_007C__007C", "try_find_duplicate_unique", "try_find_duplicate_unique_in_array", "SanityChecks_validateColumnIndex", "SanityChecks_validateRowIndex", "SanityChecks_validateColumn", "SanityChecks_validateCellColumns", "SanityChecks_validateArcTableValues", "Unchecked_tryGetCellAt", "Unchecked_getCellWithDefault", "Unchecked_setCellAt", "Unchecked_removeCellAt", "Unchecked_moveCellTo", "Unchecked_removeHeader", "Unchecked_removeColumnCells", "Unchecked_removeColumnCells_withIndexChange", "Unchecked_removeRowCells", "Unchecked_removeRowCells_withIndexChange", "Unchecked_removeRowRange_withIndexChange", "Unchecked_moveColumnCellsTo", "Unchecked_addRefColumn", "Unchecked_addColumn", "Unchecked_addColumnFill", "Unchecked_fillMissingCells", "Unchecked_addEmptyRow", "Unchecked_addRow", "Unchecked_addRows", "Unchecked_compositeHeaderMainColumnEqual", "Unchecked_moveColumnTo", "Unchecked_alignByHeaders"]


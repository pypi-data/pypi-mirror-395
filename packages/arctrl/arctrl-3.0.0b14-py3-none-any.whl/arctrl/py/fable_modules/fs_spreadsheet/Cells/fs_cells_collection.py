from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.map_util import (get_item_from_dict, add_to_dict, remove_from_dict, add_to_set)
from ...fable_library.option import (some, value as value_6)
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (map, iterate, is_empty, max, collect, delay, empty, singleton, min, min_by)
from ...fable_library.util import (IEnumerable_1, ignore, compare_primitives)
from ..fs_address import FsAddress
from .fs_cell import FsCell

def Dictionary_tryGet(k: Any, dict_1: Any) -> Any | None:
    if k in dict_1:
        return some(get_item_from_dict(dict_1, k))

    else: 
        return None



def _expr183() -> TypeInfo:
    return class_type("FsSpreadsheet.FsCellsCollection", None, FsCellsCollection)


class FsCellsCollection:
    def __init__(self, __unit: None=None) -> None:
        self._columnsUsed: Any = dict([])
        self._deleted: Any = dict([])
        self._rowsCollection: Any = dict([])
        self._maxColumnUsed: int = 0
        self._maxRowUsed: int = 0
        self._rowsUsed: Any = dict([])
        self._count: int = 0

    @property
    def Count(self, __unit: None=None) -> int:
        this: FsCellsCollection = self
        return this._count

    @Count.setter
    def Count(self, count: int) -> None:
        this: FsCellsCollection = self
        this._count = count or 0

    @property
    def MaxRowNumber(self, __unit: None=None) -> int:
        this: FsCellsCollection = self
        return this._maxRowUsed

    @property
    def MaxColumnNumber(self, __unit: None=None) -> int:
        this: FsCellsCollection = self
        return this._maxColumnUsed

    def Copy(self, __unit: None=None) -> FsCellsCollection:
        this: FsCellsCollection = self
        def mapping(c: FsCell) -> FsCell:
            return c.Copy()

        cells: IEnumerable_1[FsCell] = map(mapping, this.GetCells())
        return FsCellsCollection.create_from_cells(cells)

    @staticmethod
    def copy(cells_collection: FsCellsCollection) -> FsCellsCollection:
        return cells_collection.Copy()

    @staticmethod
    def IncrementUsage(dictionary: Any, key: int) -> None:
        match_value: int | None = Dictionary_tryGet(key, dictionary)
        if match_value is None:
            add_to_dict(dictionary, key, 1)

        else: 
            count: int = match_value or 0
            dictionary[key] = count + 1


    @staticmethod
    def DecrementUsage(dictionary: Any, key: int) -> bool:
        match_value: int | None = Dictionary_tryGet(key, dictionary)
        if match_value is None:
            return False

        elif match_value > 1:
            count_1: int = match_value or 0
            dictionary[key] = count_1 - 1
            return False

        else: 
            ignore(remove_from_dict(dictionary, key))
            return True


    @staticmethod
    def create_from_cells(cells: IEnumerable_1[FsCell]) -> FsCellsCollection:
        fcc: FsCellsCollection = FsCellsCollection()
        fcc.AddMany(cells)
        return fcc

    def Clear(self, __unit: None=None) -> FsCellsCollection:
        this: FsCellsCollection = self
        this._count = 0
        this._rowsUsed.clear()
        this._columnsUsed.clear()
        this._rowsCollection.clear()
        this._maxRowUsed = 0
        this._maxColumnUsed = 0
        return this

    def Add(self, cell: FsCell, row: int | None=None, column: int | None=None) -> None:
        this: FsCellsCollection = self
        if row is not None:
            cell.RowNumber = value_6(row) or 0

        if column is not None:
            cell.ColumnNumber = value_6(column) or 0

        row_1: int = cell.RowNumber or 0
        column_1: int = cell.ColumnNumber or 0
        this._count = (this._count + 1) or 0
        FsCellsCollection.IncrementUsage(this._rowsUsed, row_1)
        FsCellsCollection.IncrementUsage(this._columnsUsed, column_1)
        def _arrow167(__unit: None=None) -> Any:
            match_value: Any | None = Dictionary_tryGet(row_1, this._rowsCollection)
            if match_value is None:
                columns_collection_1: Any = dict([])
                add_to_dict(this._rowsCollection, row_1, columns_collection_1)
                return columns_collection_1

            else: 
                return match_value


        add_to_dict(_arrow167(), column_1, cell)
        if row_1 > this._maxRowUsed:
            this._maxRowUsed = row_1 or 0

        if column_1 > this._maxColumnUsed:
            this._maxColumnUsed = column_1 or 0

        match_value_1: Any | None = Dictionary_tryGet(row_1, this._deleted)
        if match_value_1 is None:
            pass

        else: 
            del_hash: Any = match_value_1
            ignore(del_hash.delete(column_1))


    @staticmethod
    def add_cell_with_indeces(row_index: int, col_index: int, cell: FsCell, cells_collection: FsCellsCollection) -> None:
        cells_collection.Add(cell, row_index, col_index)

    @staticmethod
    def add_cell(cell: FsCell, cells_collection: FsCellsCollection) -> FsCellsCollection:
        cells_collection.Add(cell)
        return cells_collection

    def AddMany(self, cells: IEnumerable_1[FsCell]) -> None:
        this: FsCellsCollection = self
        def action(arg: FsCell) -> None:
            value: None = this.Add(arg)
            ignore(None)

        iterate(action, cells)

    @staticmethod
    def add_cells(cells: IEnumerable_1[FsCell], cells_collection: FsCellsCollection) -> FsCellsCollection:
        cells_collection.AddMany(cells)
        return cells_collection

    def ContainsCellAt(self, row_index: int, col_index: int) -> bool:
        this: FsCellsCollection = self
        match_value: Any | None = Dictionary_tryGet(row_index, this._rowsCollection)
        if match_value is None:
            return False

        else: 
            cols_collection: Any = match_value
            return cols_collection.has(col_index)


    @staticmethod
    def contains_cell_at(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> bool:
        return cells_collection.ContainsCellAt(row_index, col_index)

    def RemoveCellAt(self, row: int, column: int) -> None:
        this: FsCellsCollection = self
        this._count = (this._count - 1) or 0
        row_removed: bool = FsCellsCollection.DecrementUsage(this._rowsUsed, row)
        column_removed: bool = FsCellsCollection.DecrementUsage(this._columnsUsed, column)
        if (row == this._maxRowUsed) if row_removed else False:
            class ObjectExpr168:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            this._maxRowUsed = (max(this._rowsUsed.keys(), ObjectExpr168()) if (not is_empty(this._rowsUsed.keys())) else 0) or 0

        if (column == this._maxColumnUsed) if column_removed else False:
            class ObjectExpr169:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            this._maxColumnUsed = (max(this._columnsUsed.keys(), ObjectExpr169()) if (not is_empty(this._columnsUsed.keys())) else 0) or 0

        match_value: Any | None = Dictionary_tryGet(row, this._deleted)
        if match_value is None:
            del_hash_3: Any = set([])
            ignore(add_to_set(column, del_hash_3))
            add_to_dict(this._deleted, row, del_hash_3)

        else: 
            def _arrow170(__unit: None=None) -> bool:
                del_hash: Any = match_value
                return del_hash.has(column)

            if _arrow170():
                del_hash_1: Any = match_value

            else: 
                del_hash_2: Any = match_value
                ignore(add_to_set(column, del_hash_2))


        match_value_1: Any | None = Dictionary_tryGet(row, this._rowsCollection)
        if match_value_1 is None:
            pass

        else: 
            columns_collection: Any = match_value_1
            ignore(remove_from_dict(columns_collection, column))
            if len(columns_collection) == 0:
                ignore(remove_from_dict(this._rowsCollection, row))



    @staticmethod
    def remove_cell_at(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
        cells_collection.RemoveCellAt(row_index, col_index)
        return cells_collection

    def TryRemoveValueAt(self, row_index: int, col_index: int) -> None:
        this: FsCellsCollection = self
        match_value: Any | None = Dictionary_tryGet(row_index, this._rowsCollection)
        if match_value is None:
            pass

        else: 
            cols_collection: Any = match_value
            try: 
                get_item_from_dict(cols_collection, col_index).Value = ""

            except Exception as match_value_1:
                pass



    @staticmethod
    def try_remove_value_at(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
        cells_collection.TryRemoveValueAt(row_index, col_index)
        return cells_collection

    def RemoveValueAt(self, row_index: int, col_index: int) -> None:
        this: FsCellsCollection = self
        get_item_from_dict(get_item_from_dict(this._rowsCollection, row_index), col_index).Value = ""

    @staticmethod
    def remove_value_at(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
        cells_collection.RemoveValueAt(row_index, col_index)
        return cells_collection

    def GetCells(self, __unit: None=None) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        def mapping(columns_collection: Any) -> Any:
            return columns_collection.values()

        return collect(mapping, this._rowsCollection.values())

    @staticmethod
    def get_cells(cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCells()

    def GetCellsInRangeBy(self, row_start: int, column_start: int, row_end: int, column_end: int, predicate: Callable[[FsCell], bool]) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        final_row: int = (this._maxRowUsed if (row_end > this._maxRowUsed) else row_end) or 0
        final_column: int = (this._maxColumnUsed if (column_end > this._maxColumnUsed) else column_end) or 0
        def _arrow174(__unit: None=None) -> IEnumerable_1[FsCell]:
            def _arrow173(ro: int) -> IEnumerable_1[FsCell]:
                match_value: Any | None = Dictionary_tryGet(ro, this._rowsCollection)
                if match_value is None:
                    return empty()

                else: 
                    columns_collection: Any = match_value
                    def _arrow172(co: int) -> IEnumerable_1[FsCell]:
                        match_value_1: FsCell | None = Dictionary_tryGet(co, columns_collection)
                        (pattern_matching_result, cell_1) = (None, None)
                        if match_value_1 is not None:
                            if predicate(match_value_1):
                                pattern_matching_result = 0
                                cell_1 = match_value_1

                            else: 
                                pattern_matching_result = 1


                        else: 
                            pattern_matching_result = 1

                        if pattern_matching_result == 0:
                            return singleton(cell_1)

                        elif pattern_matching_result == 1:
                            return empty()


                    return collect(_arrow172, range_big_int(column_start, 1, final_column))


            return collect(_arrow173, range_big_int(row_start, 1, final_row))

        return delay(_arrow174)

    @staticmethod
    def filter_cells_from_to(row_start: int, column_start: int, row_end: int, column_end: int, predicate: Callable[[FsCell], bool], cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInRangeBy(row_start, column_start, row_end, column_end, predicate)

    def GetCellsInStringRangeBy(self, start_address: FsAddress, last_address: FsAddress, predicate: Callable[[FsCell], bool]) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        return this.GetCellsInRangeBy(start_address.RowNumber, start_address.ColumnNumber, last_address.RowNumber, last_address.ColumnNumber, predicate)

    @staticmethod
    def filter_cells_from_to_address(start_address: FsAddress, last_address: FsAddress, predicate: Callable[[FsCell], bool], cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInStringRangeBy(start_address, last_address, predicate)

    def GetCellsInRange(self, row_start: int, column_start: int, row_end: int, column_end: int) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        final_row: int = (this._maxRowUsed if (row_end > this._maxRowUsed) else row_end) or 0
        final_column: int = (this._maxColumnUsed if (column_end > this._maxColumnUsed) else column_end) or 0
        def _arrow177(__unit: None=None) -> IEnumerable_1[FsCell]:
            def _arrow176(ro: int) -> IEnumerable_1[FsCell]:
                match_value: Any | None = Dictionary_tryGet(ro, this._rowsCollection)
                if match_value is None:
                    return empty()

                else: 
                    columns_collection: Any = match_value
                    def _arrow175(co: int) -> IEnumerable_1[FsCell]:
                        match_value_1: FsCell | None = Dictionary_tryGet(co, columns_collection)
                        if match_value_1 is not None:
                            return singleton(match_value_1)

                        else: 
                            return empty()


                    return collect(_arrow175, range_big_int(column_start, 1, final_column))


            return collect(_arrow176, range_big_int(row_start, 1, final_row))

        return delay(_arrow177)

    @staticmethod
    def get_cells_from_to(row_start: int, column_start: int, row_end: int, column_end: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInRange(row_start, column_start, row_end, column_end)

    def GetCellsInStringRange(self, start_address: FsAddress, last_address: FsAddress) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        return this.GetCellsInRange(start_address.RowNumber, start_address.ColumnNumber, last_address.RowNumber, last_address.ColumnNumber)

    @staticmethod
    def get_cells_from_to_address(start_address: FsAddress, last_address: FsAddress, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInStringRange(start_address, last_address)

    def TryGetCell(self, row: int, column: int) -> FsCell | None:
        this: FsCellsCollection = self
        if True if (row > this._maxRowUsed) else (column > this._maxColumnUsed):
            return None

        else: 
            match_value: Any | None = Dictionary_tryGet(row, this._rowsCollection)
            if match_value is None:
                return None

            else: 
                match_value_1: FsCell | None = Dictionary_tryGet(column, match_value)
                return None if (match_value_1 is None) else match_value_1



    @staticmethod
    def try_get_cell(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCell | None:
        return cells_collection.TryGetCell(row_index, col_index)

    def GetCellsInColumn(self, col_index: int) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        return this.GetCellsInRange(1, col_index, this._maxRowUsed, col_index)

    @staticmethod
    def get_cells_in_column(col_index: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInColumn(col_index)

    def GetCellsInRow(self, row_index: int) -> IEnumerable_1[FsCell]:
        this: FsCellsCollection = self
        return this.GetCellsInRange(row_index, 1, row_index, this._maxColumnUsed)

    @staticmethod
    def get_cells_in_row(row_index: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
        return cells_collection.GetCellsInRow(row_index)

    def GetFirstAddress(self, __unit: None=None) -> FsAddress:
        this: FsCellsCollection = self
        class ObjectExpr178:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        def _arrow182(__unit: None=None) -> int:
            def projection(d: Any) -> int:
                class ObjectExpr179:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return min(d.keys(), ObjectExpr179())

            class ObjectExpr180:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            d_1: Any = min_by(projection, this._rowsCollection.values(), ObjectExpr180())
            class ObjectExpr181:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            return min(d_1.keys(), ObjectExpr181())

        return FsAddress(0, 0) if (True if is_empty(this._rowsCollection) else is_empty(this._rowsCollection.keys())) else FsAddress(min(this._rowsCollection.keys(), ObjectExpr178()), _arrow182())

    @staticmethod
    def get_first_address(cells: FsCellsCollection) -> FsAddress:
        return cells.GetFirstAddress()

    def GetLastAddress(self, __unit: None=None) -> FsAddress:
        this: FsCellsCollection = self
        return FsAddress(this.MaxRowNumber, this.MaxColumnNumber)

    @staticmethod
    def get_last_address(cells: FsCellsCollection) -> FsAddress:
        return cells.GetLastAddress()


FsCellsCollection_reflection = _expr183

def FsCellsCollection__ctor(__unit: None=None) -> FsCellsCollection:
    return FsCellsCollection(__unit)


__all__ = ["Dictionary_tryGet", "FsCellsCollection_reflection"]


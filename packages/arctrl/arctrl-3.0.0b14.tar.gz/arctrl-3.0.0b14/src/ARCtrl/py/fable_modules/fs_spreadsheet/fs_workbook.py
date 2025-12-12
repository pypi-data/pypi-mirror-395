from __future__ import annotations
from collections.abc import Callable
from ..fable_library.array_ import (map, remove_in_place, try_find as try_find_1, collect)
from ..fable_library.option import (value as value_1, default_arg)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (exists, iterate, try_item, try_find)
from ..fable_library.string_ import (to_fail, printf)
from ..fable_library.types import Array
from ..fable_library.util import (IEnumerable_1, ignore, equals, safe_hash, IDisposable)
from .fs_worksheet import FsWorksheet
from .Tables.fs_table import FsTable

def _expr222() -> TypeInfo:
    return class_type("FsSpreadsheet.FsWorkbook", None, FsWorkbook)


class FsWorkbook(IDisposable):
    def __init__(self, __unit: None=None) -> None:
        self._worksheets: Array[FsWorksheet] = []

    def Copy(self, __unit: None=None) -> FsWorkbook:
        self_1: FsWorkbook = self
        def mapping(s: FsWorksheet) -> FsWorksheet:
            return s.Copy()

        shts: Array[FsWorksheet] = map(mapping, self_1.GetWorksheets()[:], None)
        wb: FsWorkbook = FsWorkbook()
        wb.AddWorksheets(shts)
        return wb

    @staticmethod
    def copy(workbook: FsWorkbook) -> FsWorkbook:
        return workbook.Copy()

    def InitWorksheet(self, name: str) -> FsWorksheet:
        self_1: FsWorkbook = self
        sheet: FsWorksheet = FsWorksheet(name)
        (self_1._worksheets.append(sheet))
        return sheet

    @staticmethod
    def init_worksheet(name: str, workbook: FsWorkbook) -> FsWorksheet:
        return workbook.InitWorksheet(name)

    def AddWorksheet(self, sheet: FsWorksheet) -> None:
        self_1: FsWorkbook = self
        def predicate(ws: FsWorksheet) -> bool:
            return ws.Name == sheet.Name

        if exists(predicate, self_1._worksheets):
            arg: str = sheet.Name
            to_fail(printf("Could not add worksheet with name \"%s\" to workbook as it already contains a worksheet with the same name"))(arg)

        else: 
            (self_1._worksheets.append(sheet))


    @staticmethod
    def add_worksheet(sheet: FsWorksheet, workbook: FsWorkbook) -> FsWorkbook:
        workbook.AddWorksheet(sheet)
        return workbook

    def AddWorksheets(self, sheets: IEnumerable_1[FsWorksheet]) -> None:
        self_1: FsWorkbook = self
        def action(sheet: FsWorksheet) -> None:
            self_1.AddWorksheet(sheet)

        iterate(action, sheets)

    @staticmethod
    def add_worksheets(sheets: IEnumerable_1[FsWorksheet], workbook: FsWorkbook) -> FsWorkbook:
        workbook.AddWorksheets(sheets)
        return workbook

    def GetWorksheets(self, __unit: None=None) -> Array[FsWorksheet]:
        self_1: FsWorkbook = self
        return self_1._worksheets

    @staticmethod
    def get_worksheets(workbook: FsWorkbook) -> Array[FsWorksheet]:
        return workbook.GetWorksheets()

    def TryGetWorksheetAt(self, index: int) -> FsWorksheet | None:
        self_1: FsWorkbook = self
        return try_item(index - 1, self_1._worksheets)

    @staticmethod
    def try_get_worksheet_at(index: int, workbook: FsWorkbook) -> FsWorksheet | None:
        return workbook.TryGetWorksheetAt(index)

    def GetWorksheetAt(self, index: int) -> FsWorksheet:
        self_1: FsWorkbook = self
        match_value: FsWorksheet | None = self_1.TryGetWorksheetAt(index)
        if match_value is None:
            raise Exception(("FsWorksheet at position " + str(index)) + " is not present in the FsWorkbook.")

        else: 
            return match_value


    @staticmethod
    def get_worksheet_at(index: int, workbook: FsWorkbook) -> FsWorksheet:
        return workbook.GetWorksheetAt(index)

    def TryGetWorksheetByName(self, sheet_name: str) -> FsWorksheet | None:
        self_1: FsWorkbook = self
        def predicate(w: FsWorksheet) -> bool:
            return w.Name == sheet_name

        return try_find(predicate, self_1._worksheets)

    @staticmethod
    def try_get_worksheet_by_name(sheet_name: str, workbook: FsWorkbook) -> FsWorksheet | None:
        return workbook.TryGetWorksheetByName(sheet_name)

    def GetWorksheetByName(self, sheet_name: str) -> FsWorksheet:
        self_1: FsWorkbook = self
        try: 
            return value_1(self_1.TryGetWorksheetByName(sheet_name))

        except Exception as match_value:
            raise Exception(("FsWorksheet with name " + sheet_name) + " is not present in the FsWorkbook.")


    @staticmethod
    def get_worksheet_by_name(sheet_name: str, workbook: FsWorkbook) -> FsWorksheet:
        return workbook.GetWorksheetByName(sheet_name)

    def RemoveWorksheet(self, name: str) -> None:
        self_1: FsWorkbook = self
        def _arrow220(__unit: None=None) -> FsWorksheet:
            try: 
                def _arrow219(ws: FsWorksheet) -> bool:
                    return ws.Name == name

                return default_arg(try_find_1(_arrow219, self_1._worksheets), None)

            except Exception as match_value:
                raise Exception(("FsWorksheet with name " + name) + " was not found in FsWorkbook.")


        class ObjectExpr221:
            @property
            def Equals(self) -> Callable[[FsWorksheet, FsWorksheet], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[FsWorksheet], int]:
                return safe_hash

        ignore(remove_in_place(_arrow220(), self_1._worksheets, ObjectExpr221()))

    @staticmethod
    def remove_worksheet(name: str, workbook: FsWorkbook) -> FsWorkbook:
        workbook.RemoveWorksheet(name)
        return workbook

    def GetTables(self, __unit: None=None) -> Array[FsTable]:
        self_1: FsWorkbook = self
        def mapping(s: FsWorksheet) -> Array[FsTable]:
            return list(s.Tables)

        return collect(mapping, self_1.GetWorksheets()[:], None)

    @staticmethod
    def get_tables(workbook: FsWorkbook) -> Array[FsTable]:
        return workbook.GetTables()

    @staticmethod
    def validate_for_write(workbook: FsWorkbook) -> None:
        try: 
            def action(ws: FsWorksheet) -> None:
                FsWorksheet.validate_for_write(ws)

            iterate(action, workbook.GetWorksheets())

        except Exception as ex:
            raise Exception(("FsWorkbook could not be validated for write: " + str(ex)) + "")


    def Dispose(self, __unit: None=None) -> None:
        pass


FsWorkbook_reflection = _expr222

def FsWorkbook__ctor(__unit: None=None) -> FsWorkbook:
    return FsWorkbook(__unit)


__all__ = ["FsWorkbook_reflection"]


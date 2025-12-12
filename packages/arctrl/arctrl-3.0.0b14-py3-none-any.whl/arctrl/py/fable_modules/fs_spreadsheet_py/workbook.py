from __future__ import annotations
from openpyxl import Workbook
from typing import Any
from ..fable_library.array_ import iterate as iterate_1
from ..fable_library.seq import iterate
from ..fable_library.util import ignore
from ..fable_openpyxl.openpyxl import (Workbook as Workbook_1, Worksheet)
from ..fs_spreadsheet.fs_workbook import FsWorkbook
from ..fs_spreadsheet.fs_worksheet import FsWorksheet
from .worksheet import (from_fs_worksheet, to_fs_worksheet)

def from_fs_workbook(fs_wb: FsWorkbook) -> Workbook:
    FsWorkbook.validate_for_write(fs_wb)
    if len(fs_wb.GetWorksheets()) == 0:
        raise Exception("Workbook must contain at least one worksheet")

    py_wb: Workbook = Workbook(None)
    py_wb.remove(py_wb.active)
    def action(ws: FsWorksheet, fs_wb: Any=fs_wb) -> None:
        ignore(from_fs_worksheet(py_wb, ws))

    iterate(action, fs_wb.GetWorksheets())
    return py_wb


def to_fs_workbook(py_wb: Workbook) -> FsWorkbook:
    fs_wb: FsWorkbook = FsWorkbook()
    def action(ws: Worksheet, py_wb: Any=py_wb) -> None:
        if (len([list(inner_tuple) for inner_tuple in ws.values]) != 0) if (ws.title != "Sheet") else False:
            w: FsWorksheet = to_fs_worksheet(ws)
            w.RescanRows()
            value: None = fs_wb.AddWorksheet(w)
            ignore(None)


    iterate_1(action, py_wb.worksheets)
    return fs_wb


__all__ = ["from_fs_workbook", "to_fs_workbook"]


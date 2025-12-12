from __future__ import annotations
from typing import Any
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_openpyxl.openpyxl import (Xlsx_readFile_Z721C83C5, Xlsx_load_4E60E31B, Xlsx_read_Z3F6BC7B1, Xlsx_writeFile_A9E7E13, Xlsx_write_Z22AEA2D8)
from ..fs_spreadsheet.fs_workbook import FsWorkbook
from .workbook import (to_fs_workbook, from_fs_workbook)

def _expr358() -> TypeInfo:
    return class_type("FsSpreadsheet.Py.Xlsx", None, Xlsx)


class Xlsx:
    @staticmethod
    def from_xlsx_file(path: str) -> FsWorkbook:
        return to_fs_workbook(Xlsx_readFile_Z721C83C5(path))

    @staticmethod
    def from_xlsx_stream(stream: Any) -> FsWorkbook:
        return to_fs_workbook(Xlsx_load_4E60E31B(stream))

    @staticmethod
    def from_xlsx_bytes(bytes: bytearray) -> FsWorkbook:
        return to_fs_workbook(Xlsx_read_Z3F6BC7B1(bytes))

    @staticmethod
    def to_xlsx_file(path: str, wb: FsWorkbook) -> None:
        Xlsx_writeFile_A9E7E13(from_fs_workbook(wb), path)

    @staticmethod
    def to_xlsx_bytes(wb: FsWorkbook) -> bytearray:
        return Xlsx_write_Z22AEA2D8(from_fs_workbook(wb))


Xlsx_reflection = _expr358

__all__ = ["Xlsx_reflection"]


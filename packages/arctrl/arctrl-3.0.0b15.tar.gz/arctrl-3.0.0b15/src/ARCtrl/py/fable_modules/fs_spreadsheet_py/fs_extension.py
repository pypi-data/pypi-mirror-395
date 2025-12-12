from __future__ import annotations
from typing import Any
from ..fs_spreadsheet.fs_workbook import FsWorkbook
from .json import Json
from .xlsx import Xlsx

def FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5(path: str) -> FsWorkbook:
    return Xlsx.from_xlsx_file(path)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxStream_Static_4D976C1A(stream: Any) -> FsWorkbook:
    return Xlsx.from_xlsx_stream(stream)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxBytes_Static_Z3F6BC7B1(bytes: bytearray) -> FsWorkbook:
    return Xlsx.from_xlsx_bytes(bytes)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path: str, wb: FsWorkbook) -> None:
    Xlsx.to_xlsx_file(path, wb)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxBytes_Static_32154C9D(wb: FsWorkbook) -> bytearray:
    return Xlsx.to_xlsx_bytes(wb)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToXlsxFile_Z721C83C5(this: FsWorkbook, path: str) -> None:
    FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, this)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToXlsxBytes(this: FsWorkbook) -> bytearray:
    return FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxBytes_Static_32154C9D(this)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromRowsJsonString_Static_Z721C83C5(json: str) -> FsWorkbook:
    return Json.from_rows_json_string(json)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toRowsJsonString_Static_Z2B6E0EF5(wb: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
    return Json.to_rows_json_string(wb, spaces, no_numbering)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToRowsJsonString_Z3B036AA(this: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
    return FsSpreadsheet_FsWorkbook__FsWorkbook_toRowsJsonString_Static_Z2B6E0EF5(this, spaces, no_numbering)


def FsSpreadsheet_FsWorkbook__FsWorkbook_fromColumnsJsonString_Static_Z721C83C5(json: str) -> FsWorkbook:
    return Json.from_columns_json_string(json)


def FsSpreadsheet_FsWorkbook__FsWorkbook_toColumnsJsonString_Static_Z2B6E0EF5(wb: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
    return Json.to_columns_json_string(wb, spaces, no_numbering)


def FsSpreadsheet_FsWorkbook__FsWorkbook_ToColumnsJsonString_Z3B036AA(this: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
    return FsSpreadsheet_FsWorkbook__FsWorkbook_toColumnsJsonString_Static_Z2B6E0EF5(this, spaces, no_numbering)


__all__ = ["FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxStream_Static_4D976C1A", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxBytes_Static_Z3F6BC7B1", "FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static", "FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxBytes_Static_32154C9D", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToXlsxFile_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToXlsxBytes", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromRowsJsonString_Static_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_toRowsJsonString_Static_Z2B6E0EF5", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToRowsJsonString_Z3B036AA", "FsSpreadsheet_FsWorkbook__FsWorkbook_fromColumnsJsonString_Static_Z721C83C5", "FsSpreadsheet_FsWorkbook__FsWorkbook_toColumnsJsonString_Static_Z2B6E0EF5", "FsSpreadsheet_FsWorkbook__FsWorkbook_ToColumnsJsonString_Z3B036AA"]


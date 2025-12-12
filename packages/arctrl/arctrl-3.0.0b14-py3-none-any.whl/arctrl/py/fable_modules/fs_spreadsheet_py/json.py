from __future__ import annotations
from ..fable_library.option import default_arg
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.result import FSharpResult_2
from ..fable_library.string_ import (to_fail, printf)
from ..fs_spreadsheet.fs_workbook import FsWorkbook
from ..fs_spreadsheet.Json.workbook import (decode_rows, encode_rows, decode_columns, encode_columns)
from ..thoth_json_python.decode import Decode_fromString
from ..thoth_json_python.encode import to_string

def _expr359() -> TypeInfo:
    return class_type("FsSpreadsheet.Py.Json", None, Json)


class Json:
    @staticmethod
    def try_from_rows_json_string(json: str) -> FSharpResult_2[FsWorkbook, str]:
        return Decode_fromString(decode_rows, json)

    @staticmethod
    def from_rows_json_string(json: str) -> FsWorkbook:
        match_value: FSharpResult_2[FsWorkbook, str] = Json.try_from_rows_json_string(json)
        return to_fail(printf("Could not deserialize json Workbook: \n%s"))(match_value.fields[0]) if (match_value.tag == 1) else match_value.fields[0]

    @staticmethod
    def to_rows_json_string(wb: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
        no_numbering_1: bool = default_arg(no_numbering, False)
        return to_string(default_arg(spaces, 2), encode_rows(no_numbering_1, wb))

    @staticmethod
    def try_from_columns_json_string(json: str) -> FSharpResult_2[FsWorkbook, str]:
        return Decode_fromString(decode_columns, json)

    @staticmethod
    def from_columns_json_string(json: str) -> FsWorkbook:
        match_value: FSharpResult_2[FsWorkbook, str] = Json.try_from_columns_json_string(json)
        return to_fail(printf("Could not deserialize json Workbook: \n%s"))(match_value.fields[0]) if (match_value.tag == 1) else match_value.fields[0]

    @staticmethod
    def to_columns_json_string(wb: FsWorkbook, spaces: int | None=None, no_numbering: bool | None=None) -> str:
        return to_string(default_arg(spaces, 2), encode_columns(default_arg(no_numbering, False), wb))


Json_reflection = _expr359

__all__ = ["Json_reflection"]


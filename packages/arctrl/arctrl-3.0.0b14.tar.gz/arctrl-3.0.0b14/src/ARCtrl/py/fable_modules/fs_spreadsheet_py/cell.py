from __future__ import annotations
from abc import abstractmethod
from datetime import datetime as datetime_1
from typing import (Protocol, Any)
from ..fable_library.date import to_universal_time
from ..fable_library.option import some
from ..fable_library.util import equals
from ..fable_openpyxl.openpyxl import Cell
from ..fs_spreadsheet.Cells.fs_cell import (DataType, FsCell)
from ..fs_spreadsheet.fs_address import FsAddress

class datetime(Protocol):
    @abstractmethod
    def decoy(self) -> None:
        ...


class DateTimeStatic(Protocol):
    @abstractmethod
    def from_time_stamp(self, timestamp: float) -> datetime:
        ...


def to_universal_time_py(dt: Any) -> datetime:
    timestamp: float = to_universal_time(dt).timestamp()
    return datetime_1.fromtimestamp(timestamp=timestamp)


def from_fs_cell(fs_cell: FsCell) -> Any | None:
    match_value: DataType = fs_cell.DataType
    if match_value.tag == 2:
        return some(fs_cell.ValueAsFloat())

    elif match_value.tag == 3:
        return some(to_universal_time_py(fs_cell.ValueAsDateTime()))

    elif match_value.tag == 0:
        return some(fs_cell.Value)

    elif match_value.tag == 4:
        return some(fs_cell.Value)

    else: 
        return some(fs_cell.ValueAsBool())



def to_fs_cell(worksheet_name: Any, row_index: int, column_index: int, py_cell: Cell) -> FsCell:
    fsadress: FsAddress = FsAddress(row_index, column_index)
    pattern_input_1: tuple[DataType, Any]
    pattern_input: tuple[DataType, Any]
    value_1: Any = py_cell.value
    pattern_input = ((DataType(0), value_1)) if (str(type(value_1)) == "<class \'str\'>") else ((((DataType(1), True)) if value_1 else ((DataType(1), False))) if (str(type(value_1)) == "<class \'bool\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<fable_modules.fable_library.types.uint8\'>>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.int8\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'int\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.int16\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.int64\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.uint32>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.uint16\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.uint32\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'fable_modules.fable_library.types.float32\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'float\'>") else (((DataType(2), value_1)) if (str(type(value_1)) == "<class \'int\'>") else (((DataType(3), value_1)) if isinstance(value_1, datetime_1) else (((DataType(0), value_1)) if (str(type(value_1)) == "<class \'str\'>") else ((DataType(0), value_1))))))))))))))))
    v: Any = pattern_input[1]
    pattern_input_1 = ((DataType(1), True)) if (True if equals(v, "=TRUE()") else equals(v, "=True()")) else (((DataType(1), False)) if (True if equals(v, "=FALSE()") else equals(v, "=False()")) else ((pattern_input[0], v)))
    return FsCell(pattern_input_1[1], pattern_input_1[0], fsadress)


__all__ = ["to_universal_time_py", "from_fs_cell", "to_fs_cell"]


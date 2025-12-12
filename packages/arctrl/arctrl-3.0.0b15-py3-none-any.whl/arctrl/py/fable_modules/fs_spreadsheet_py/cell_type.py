from __future__ import annotations
from ..fable_library.string_ import (to_text, printf, to_console)
from ..fable_openpyxl.openpyxl import CellType
from ..fs_spreadsheet.Cells.fs_cell import DataType

def from_data_tyoe(t: DataType) -> CellType:
    if t.tag == 1:
        return CellType(3)

    elif t.tag == 2:
        return CellType(0)

    elif t.tag == 3:
        return CellType(4)

    elif t.tag == 0:
        return CellType(2)

    else: 
        msg: str = to_text(printf("ValueType \'%A\' is not fully implemented in FsSpreadsheet and is handled as string input."))(t)
        to_console(printf("%s"))(msg)
        return CellType(2)



def to_data_type(t: CellType) -> DataType:
    if t.tag == 3:
        return DataType(1)

    elif t.tag == 0:
        return DataType(2)

    elif t.tag == 1:
        return DataType(2)

    elif t.tag == 4:
        return DataType(3)

    elif t.tag == 2:
        return DataType(0)

    else: 
        msg: str = to_text(printf("ValueType \'%A\' is not fully implemented in FsSpreadsheet and is handled as string input."))(t)
        to_console(printf("%s"))(msg)
        return DataType(0)



__all__ = ["from_data_tyoe", "to_data_type"]


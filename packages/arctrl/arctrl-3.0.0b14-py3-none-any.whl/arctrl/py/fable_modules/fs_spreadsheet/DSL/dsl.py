from __future__ import annotations
from typing import Any
from ...fable_library.list import (FSharpList, singleton)
from ...fable_library.reflection import (TypeInfo, class_type)
from ..Cells.fs_cell import DataType
from .types import (SheetEntity_1, Message, RowElement, ColumnElement, SheetElement, WorkbookElement)

def _expr290() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.DSL", None, DSL)


class DSL:
    ...

DSL_reflection = _expr290

def DSL_opt_Z6AB9374C(elem: SheetEntity_1[FSharpList[Any]]) -> SheetEntity_1[FSharpList[Any]]:
    if elem.tag == 1:
        return SheetEntity_1(1, elem.fields[0])

    elif elem.tag == 2:
        return SheetEntity_1(1, elem.fields[0])

    else: 
        return elem



def DSL_dropCell_6CC5727E(message: Message) -> SheetEntity_1[tuple[DataType, Any]]:
    return SheetEntity_1(2, singleton(message))


def DSL_dropRow_6CC5727E(message: Message) -> SheetEntity_1[RowElement]:
    return SheetEntity_1(2, singleton(message))


def DSL_dropColumn_6CC5727E(message: Message) -> SheetEntity_1[ColumnElement]:
    return SheetEntity_1(2, singleton(message))


def DSL_dropSheet_6CC5727E(message: Message) -> SheetEntity_1[SheetElement]:
    return SheetEntity_1(2, singleton(message))


def DSL_dropWorkbook_6CC5727E(message: Message) -> SheetEntity_1[WorkbookElement]:
    return SheetEntity_1(2, singleton(message))


__all__ = ["DSL_reflection", "DSL_opt_Z6AB9374C", "DSL_dropCell_6CC5727E", "DSL_dropRow_6CC5727E", "DSL_dropColumn_6CC5727E", "DSL_dropSheet_6CC5727E", "DSL_dropWorkbook_6CC5727E"]


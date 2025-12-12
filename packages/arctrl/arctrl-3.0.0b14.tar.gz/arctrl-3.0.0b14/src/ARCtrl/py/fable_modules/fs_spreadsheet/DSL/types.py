from __future__ import annotations
from collections.abc import Callable
from typing import (Any, Generic, TypeVar)
from ...fable_library.list import (reduce, map, FSharpList, exists, pick, empty)
from ...fable_library.reflection import (TypeInfo, string_type, class_type, union_type, list_type, int32_type, obj_type, tuple_type)
from ...fable_library.string_ import (to_console, printf)
from ...fable_library.types import (Array, Union)
from ..Cells.fs_cell import DataType_reflection

_T = TypeVar("_T")

def _expr256() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.Message", [], Message, lambda: [[("Item", string_type)], [("Item", class_type("System.Exception"))]])


class Message(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Text", "Exception"]


Message_reflection = _expr256

def Message_message_Z721C83C5(s: str) -> Message:
    return Message(0, s)


def Message_message_2BC701FD(e: Any | None=None) -> Message:
    return Message(1, e)


def Message__MapText_11D407F6(this: Message, m: Callable[[str], str]) -> Message:
    if this.tag == 1:
        return this

    else: 
        return Message(0, m(this.fields[0]))



def Message__AsString(this: Message) -> str:
    if this.tag == 1:
        return str(this.fields[0])

    else: 
        return this.fields[0]



def Message__TryText(this: Message) -> str | None:
    if this.tag == 0:
        return this.fields[0]

    else: 
        return None



def Message__TryException(this: Message) -> Exception | None:
    if this.tag == 1:
        return this.fields[0]

    else: 
        return None



def Message__get_IsTxt(this: Message) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def Message__get_IsExc(this: Message) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def Messages_format(ms: FSharpList[Message]) -> str:
    def reduction(a: str, b: str, ms: Any=ms) -> str:
        return (a + ";") + b

    def mapping(m: Message, ms: Any=ms) -> str:
        return Message__AsString(m)

    return reduce(reduction, map(mapping, ms))


def Messages_fail(ms: FSharpList[Message]) -> Any:
    s: str = Messages_format(ms)
    def predicate(m: Message, ms: Any=ms) -> bool:
        return Message__get_IsExc(m)

    if exists(predicate, ms):
        to_console(printf("s"))
        def chooser(m_1: Message, ms: Any=ms) -> Exception | None:
            return Message__TryException(m_1)

        raise pick(chooser, ms)

    else: 
        raise Exception(s)



def _expr258(gen0: TypeInfo) -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.SheetEntity`1", [gen0], SheetEntity_1, lambda: [[("Item1", gen0), ("Item2", list_type(Message_reflection()))], [("Item", list_type(Message_reflection()))], [("Item", list_type(Message_reflection()))]])


class SheetEntity_1(Union, Generic[_T]):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Some", "NoneOptional", "NoneRequired"]


SheetEntity_1_reflection = _expr258

def SheetEntity_1_some_2B595(v: Any | None=None) -> SheetEntity_1[Any]:
    return SheetEntity_1(0, v, empty())


def SheetEntity_1__get_Messages(this: SheetEntity_1[Any]) -> FSharpList[Message]:
    if this.tag == 1:
        return this.fields[0]

    elif this.tag == 2:
        return this.fields[0]

    else: 
        return this.fields[1]



def _expr259() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.ColumnIndex", [], ColumnIndex, lambda: [[("Item", int32_type)]])


class ColumnIndex(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Col"]


ColumnIndex_reflection = _expr259

def ColumnIndex__get_Index(self_1: ColumnIndex) -> int:
    return self_1.fields[0]


def _expr260() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.RowIndex", [], RowIndex, lambda: [[("Item", int32_type)]])


class RowIndex(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Row"]


RowIndex_reflection = _expr260

def RowIndex__get_Index(self_1: RowIndex) -> int:
    return self_1.fields[0]


def _expr261() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.ColumnElement", [], ColumnElement, lambda: [[("Item1", RowIndex_reflection()), ("Item2", tuple_type(DataType_reflection(), obj_type))], [("Item", tuple_type(DataType_reflection(), obj_type))]])


class ColumnElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["IndexedCell", "UnindexedCell"]


ColumnElement_reflection = _expr261

def _expr262() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.RowElement", [], RowElement, lambda: [[("Item1", ColumnIndex_reflection()), ("Item2", tuple_type(DataType_reflection(), obj_type))], [("Item", tuple_type(DataType_reflection(), obj_type))]])


class RowElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["IndexedCell", "UnindexedCell"]


RowElement_reflection = _expr262

def _expr263() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.TableElement", [], TableElement, lambda: [[("Item", list_type(RowElement_reflection()))], [("Item", list_type(ColumnElement_reflection()))]])


class TableElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["UnindexedRow", "UnindexedColumn"]


TableElement_reflection = _expr263

def TableElement__get_IsRow(this: TableElement) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def TableElement__get_IsColumn(this: TableElement) -> bool:
    if this.tag == 1:
        return True

    else: 
        return False



def _expr264() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.SheetElement", [], SheetElement, lambda: [[("Item1", string_type), ("Item2", list_type(TableElement_reflection()))], [("Item1", RowIndex_reflection()), ("Item2", list_type(RowElement_reflection()))], [("Item", list_type(RowElement_reflection()))], [("Item1", ColumnIndex_reflection()), ("Item2", list_type(ColumnElement_reflection()))], [("Item", list_type(ColumnElement_reflection()))], [("Item1", RowIndex_reflection()), ("Item2", ColumnIndex_reflection()), ("Item3", tuple_type(DataType_reflection(), obj_type))], [("Item", tuple_type(DataType_reflection(), obj_type))]])


class SheetElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Table", "IndexedRow", "UnindexedRow", "IndexedColumn", "UnindexedColumn", "IndexedCell", "UnindexedCell"]


SheetElement_reflection = _expr264

def _expr265() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.WorkbookElement", [], WorkbookElement, lambda: [[("Item", list_type(SheetElement_reflection()))], [("Item1", string_type), ("Item2", list_type(SheetElement_reflection()))]])


class WorkbookElement(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["UnnamedSheet", "NamedSheet"]


WorkbookElement_reflection = _expr265

def _expr266() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.Workbook", [], Workbook, lambda: [[("Item", list_type(WorkbookElement_reflection()))]])


class Workbook(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Workbook"]


Workbook_reflection = _expr266

__all__ = ["Message_reflection", "Message_message_Z721C83C5", "Message_message_2BC701FD", "Message__MapText_11D407F6", "Message__AsString", "Message__TryText", "Message__TryException", "Message__get_IsTxt", "Message__get_IsExc", "Messages_format", "Messages_fail", "SheetEntity_1_reflection", "SheetEntity_1_some_2B595", "SheetEntity_1__get_Messages", "ColumnIndex_reflection", "ColumnIndex__get_Index", "RowIndex_reflection", "RowIndex__get_Index", "ColumnElement_reflection", "RowElement_reflection", "TableElement_reflection", "TableElement__get_IsRow", "TableElement__get_IsColumn", "SheetElement_reflection", "WorkbookElement_reflection", "Workbook_reflection"]


from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (reduce, map, FSharpList, empty, append, is_empty, tail, head)
from ...fable_library.reflection import (TypeInfo, char_type, union_type, class_type)
from ...fable_library.string_ import (to_text, printf)
from ...fable_library.types import (Array, Union, to_string)
from ..Cells.fs_cell import DataType
from .expression import (RequiredSource_1__ctor_2B595, RequiredSource_1, OptionalSource_1__ctor_2B595, OptionalSource_1, RequiredSource_1__get_Source, OptionalSource_1__get_Source)
from .types import (SheetEntity_1, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr277() -> TypeInfo:
    return union_type("FsSpreadsheet.DSL.ReduceOperation", [], ReduceOperation, lambda: [[("Item", char_type)]])


class ReduceOperation(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["Concat"]


ReduceOperation_reflection = _expr277

def ReduceOperation__Reduce_70D1A69E(this: ReduceOperation, values: FSharpList[tuple[DataType, Any]]) -> tuple[DataType, Any]:
    def reduction(a: str, b: str, this: Any=this, values: Any=values) -> str:
        return ((((("" + a) + "") + str(this.fields[0])) + "") + b) + ""

    def mapping(arg: tuple[DataType, Any], this: Any=this, values: Any=values) -> str:
        return to_string(arg[1])

    return (DataType(0), reduce(reduction, map(mapping, values)))


def _expr278() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.CellBuilder", None, CellBuilder)


class CellBuilder:
    def __init__(self, __unit: None=None) -> None:
        self.reducer: ReduceOperation = ReduceOperation(0, ",")


CellBuilder_reflection = _expr278

def CellBuilder__ctor(__unit: None=None) -> CellBuilder:
    return CellBuilder(__unit)


def CellBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[tuple[DataType, Any]]]:
    return SheetEntity_1(1, empty())


def CellBuilder__SignMessages_3F89FFFC(this: CellBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow279(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo: Callable[[str], str] = to_text(printf("In Cell: %s"))
            return clo

        return Message__MapText_11D407F6(m, _arrow279())

    return map(mapping, messages)


def CellBuilder__Yield_36B9E420(this: CellBuilder, ro: ReduceOperation) -> SheetEntity_1[FSharpList[tuple[DataType, Any]]]:
    this.reducer = ro
    return SheetEntity_1(1, empty())


def CellBuilder__Combine_F07E260(this: CellBuilder, wx1: SheetEntity_1[FSharpList[tuple[DataType, Any]]], wx2: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> SheetEntity_1[FSharpList[tuple[DataType, Any]]]:
    (pattern_matching_result, l1, l2, messages1, messages2, messages2_1, messages1_1, f1, messages1_2, messages2_2, f2, messages1_3, messages2_3, messages1_4, messages2_4) = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
    if wx1.tag == 2:
        if wx2.tag == 2:
            pattern_matching_result = 1
            messages2_1 = wx2.fields[0]

        else: 
            pattern_matching_result = 2
            messages1_1 = wx1.fields[0]


    elif wx1.tag == 1:
        if wx2.tag == 0:
            pattern_matching_result = 4
            f2 = wx2.fields[0]
            messages1_3 = wx1.fields[0]
            messages2_3 = wx2.fields[1]

        elif wx2.tag == 1:
            pattern_matching_result = 5
            messages1_4 = wx1.fields[0]
            messages2_4 = wx2.fields[0]

        else: 
            pattern_matching_result = 1
            messages2_1 = wx2.fields[0]


    elif wx2.tag == 2:
        pattern_matching_result = 1
        messages2_1 = wx2.fields[0]

    elif wx2.tag == 1:
        pattern_matching_result = 3
        f1 = wx1.fields[0]
        messages1_2 = wx1.fields[1]
        messages2_2 = wx2.fields[0]

    else: 
        pattern_matching_result = 0
        l1 = wx1.fields[0]
        l2 = wx2.fields[0]
        messages1 = wx1.fields[1]
        messages2 = wx2.fields[1]

    if pattern_matching_result == 0:
        return SheetEntity_1(0, append(l1, l2), append(messages1, messages2))

    elif pattern_matching_result == 1:
        return SheetEntity_1(2, append(SheetEntity_1__get_Messages(wx1), messages2_1))

    elif pattern_matching_result == 2:
        return SheetEntity_1(2, append(messages1_1, SheetEntity_1__get_Messages(wx2)))

    elif pattern_matching_result == 3:
        return SheetEntity_1(0, f1, append(messages1_2, messages2_2))

    elif pattern_matching_result == 4:
        return SheetEntity_1(0, f2, append(messages1_3, messages2_3))

    elif pattern_matching_result == 5:
        return SheetEntity_1(1, append(messages1_4, messages2_4))



def CellBuilder__Combine_4BCE267E(this: CellBuilder, wx1: RequiredSource_1[None], wx2: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return RequiredSource_1__ctor_2B595(wx2)


def CellBuilder__Combine_Z2CF9C142(this: CellBuilder, wx1: SheetEntity_1[FSharpList[tuple[DataType, Any]]], wx2: RequiredSource_1[None]) -> RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return RequiredSource_1__ctor_2B595(wx1)


def CellBuilder__Combine_583F6A19(this: CellBuilder, wx1: OptionalSource_1[None], wx2: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return OptionalSource_1__ctor_2B595(wx2)


def CellBuilder__Combine_168D7AF9(this: CellBuilder, wx1: SheetEntity_1[FSharpList[tuple[DataType, Any]]], wx2: OptionalSource_1[None]) -> OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return OptionalSource_1__ctor_2B595(wx1)


def CellBuilder__Combine_32507AAF(this: CellBuilder, wx1: RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]], wx2: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return RequiredSource_1__ctor_2B595(CellBuilder__Combine_F07E260(this, RequiredSource_1__get_Source(wx1), wx2))


def CellBuilder__Combine_Z3ABF6771(this: CellBuilder, wx1: SheetEntity_1[FSharpList[tuple[DataType, Any]]], wx2: RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]) -> RequiredSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return RequiredSource_1__ctor_2B595(CellBuilder__Combine_F07E260(this, wx1, RequiredSource_1__get_Source(wx2)))


def CellBuilder__Combine_Z2BFC83F8(this: CellBuilder, wx1: OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]], wx2: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return OptionalSource_1__ctor_2B595(CellBuilder__Combine_F07E260(this, OptionalSource_1__get_Source(wx1), wx2))


def CellBuilder__Combine_245D6C8(this: CellBuilder, wx1: SheetEntity_1[FSharpList[tuple[DataType, Any]]], wx2: OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]) -> OptionalSource_1[SheetEntity_1[FSharpList[tuple[DataType, Any]]]]:
    return OptionalSource_1__ctor_2B595(CellBuilder__Combine_F07E260(this, wx1, OptionalSource_1__get_Source(wx2)))


def CellBuilder__AsCellElement_6F87C2ED(this: CellBuilder, children: SheetEntity_1[FSharpList[tuple[DataType, Any]]]) -> SheetEntity_1[tuple[tuple[DataType, Any], int | None]]:
    (pattern_matching_result, messages, v, messages_1, vals, messages_2, messages_3) = (None, None, None, None, None, None, None)
    if children.tag == 2:
        pattern_matching_result = 2
        messages_2 = children.fields[0]

    elif children.tag == 1:
        pattern_matching_result = 3
        messages_3 = children.fields[0]

    elif not is_empty(children.fields[0]):
        if is_empty(tail(children.fields[0])):
            pattern_matching_result = 0
            messages = children.fields[1]
            v = head(children.fields[0])

        else: 
            pattern_matching_result = 1
            messages_1 = children.fields[1]
            vals = children.fields[0]


    else: 
        pattern_matching_result = 1
        messages_1 = children.fields[1]
        vals = children.fields[0]

    if pattern_matching_result == 0:
        return SheetEntity_1(0, (v, None), messages)

    elif pattern_matching_result == 1:
        return SheetEntity_1(0, (ReduceOperation__Reduce_70D1A69E(this.reducer, vals), None), messages_1)

    elif pattern_matching_result == 2:
        return SheetEntity_1(2, messages_2)

    elif pattern_matching_result == 3:
        return SheetEntity_1(1, messages_3)



__all__ = ["ReduceOperation_reflection", "ReduceOperation__Reduce_70D1A69E", "CellBuilder_reflection", "CellBuilder_get_Empty", "CellBuilder__SignMessages_3F89FFFC", "CellBuilder__Yield_36B9E420", "CellBuilder__Combine_F07E260", "CellBuilder__Combine_4BCE267E", "CellBuilder__Combine_Z2CF9C142", "CellBuilder__Combine_583F6A19", "CellBuilder__Combine_168D7AF9", "CellBuilder__Combine_32507AAF", "CellBuilder__Combine_Z3ABF6771", "CellBuilder__Combine_Z2BFC83F8", "CellBuilder__Combine_245D6C8", "CellBuilder__AsCellElement_6F87C2ED"]


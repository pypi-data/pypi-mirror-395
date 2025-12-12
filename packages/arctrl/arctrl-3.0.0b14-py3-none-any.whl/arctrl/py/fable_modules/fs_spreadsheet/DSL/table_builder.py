from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (empty, FSharpList, map, append)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from .types import (SheetEntity_1_some_2B595, SheetEntity_1, TableElement, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr284() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.TableBuilder", None, TableBuilder)


class TableBuilder:
    def __init__(self, name: str) -> None:
        self.name: str = name


TableBuilder_reflection = _expr284

def TableBuilder__ctor_Z721C83C5(name: str) -> TableBuilder:
    return TableBuilder(name)


def TableBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[TableElement]]:
    return SheetEntity_1_some_2B595(empty())


def TableBuilder__get_Name(this: TableBuilder) -> str:
    return this.name


def TableBuilder__SignMessages_3F89FFFC(this: TableBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow285(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo_1: Callable[[str], str] = to_text(printf("In Sheet %s: %s"))(this.name)
            return clo_1

        return Message__MapText_11D407F6(m, _arrow285())

    return map(mapping, messages)


def TableBuilder__Run_15698F84(this: TableBuilder, children: SheetEntity_1[FSharpList[TableElement]]) -> SheetEntity_1[tuple[str, FSharpList[TableElement]]]:
    if children.tag == 1:
        return SheetEntity_1(1, children.fields[0])

    elif children.tag == 2:
        return SheetEntity_1(2, children.fields[0])

    else: 
        return SheetEntity_1(0, (this.name, children.fields[0]), children.fields[1])



def TableBuilder__Combine_Z280DF080(this: TableBuilder, wx1: SheetEntity_1[FSharpList[TableElement]], wx2: SheetEntity_1[FSharpList[TableElement]]) -> SheetEntity_1[FSharpList[TableElement]]:
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



__all__ = ["TableBuilder_reflection", "TableBuilder_get_Empty", "TableBuilder__get_Name", "TableBuilder__SignMessages_3F89FFFC", "TableBuilder__Run_15698F84", "TableBuilder__Combine_Z280DF080"]


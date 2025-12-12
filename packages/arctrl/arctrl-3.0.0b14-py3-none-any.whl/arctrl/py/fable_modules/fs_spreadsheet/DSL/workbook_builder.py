from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (empty, FSharpList, map, append)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from .types import (SheetEntity_1_some_2B595, SheetEntity_1, WorkbookElement, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr288() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.WorkbookBuilder", None, WorkbookBuilder)


class WorkbookBuilder:
    def __init__(self, __unit: None=None) -> None:
        pass


WorkbookBuilder_reflection = _expr288

def WorkbookBuilder__ctor(__unit: None=None) -> WorkbookBuilder:
    return WorkbookBuilder(__unit)


def WorkbookBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[WorkbookElement]]:
    return SheetEntity_1_some_2B595(empty())


def WorkbookBuilder__SignMessages_3F89FFFC(this: WorkbookBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow289(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo: Callable[[str], str] = to_text(printf("In Workbook: %s"))
            return clo

        return Message__MapText_11D407F6(m, _arrow289())

    return map(mapping, messages)


def WorkbookBuilder__Combine_49CE2EC0(this: WorkbookBuilder, wx1: SheetEntity_1[FSharpList[WorkbookElement]], wx2: SheetEntity_1[FSharpList[WorkbookElement]]) -> SheetEntity_1[FSharpList[WorkbookElement]]:
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



__all__ = ["WorkbookBuilder_reflection", "WorkbookBuilder_get_Empty", "WorkbookBuilder__SignMessages_3F89FFFC", "WorkbookBuilder__Combine_49CE2EC0"]


from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (empty, FSharpList, map, append)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from .types import (SheetEntity_1_some_2B595, SheetEntity_1, SheetElement, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr286() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.SheetBuilder", None, SheetBuilder)


class SheetBuilder:
    def __init__(self, name: str) -> None:
        self.name: str = name


SheetBuilder_reflection = _expr286

def SheetBuilder__ctor_Z721C83C5(name: str) -> SheetBuilder:
    return SheetBuilder(name)


def SheetBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[SheetElement]]:
    return SheetEntity_1_some_2B595(empty())


def SheetBuilder__SignMessages_3F89FFFC(this: SheetBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow287(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo_1: Callable[[str], str] = to_text(printf("In Sheet %s: %s"))(this.name)
            return clo_1

        return Message__MapText_11D407F6(m, _arrow287())

    return map(mapping, messages)


def SheetBuilder__Run_5EFE5A35(this: SheetBuilder, children: SheetEntity_1[FSharpList[SheetElement]]) -> SheetEntity_1[tuple[str, FSharpList[SheetElement]]]:
    if children.tag == 1:
        return SheetEntity_1(1, children.fields[0])

    elif children.tag == 2:
        return SheetEntity_1(2, children.fields[0])

    else: 
        return SheetEntity_1(0, (this.name, children.fields[0]), children.fields[1])



def SheetBuilder__Combine_6037FAE0(this: SheetBuilder, wx1: SheetEntity_1[FSharpList[SheetElement]], wx2: SheetEntity_1[FSharpList[SheetElement]]) -> SheetEntity_1[FSharpList[SheetElement]]:
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



__all__ = ["SheetBuilder_reflection", "SheetBuilder_get_Empty", "SheetBuilder__SignMessages_3F89FFFC", "SheetBuilder__Run_5EFE5A35", "SheetBuilder__Combine_6037FAE0"]


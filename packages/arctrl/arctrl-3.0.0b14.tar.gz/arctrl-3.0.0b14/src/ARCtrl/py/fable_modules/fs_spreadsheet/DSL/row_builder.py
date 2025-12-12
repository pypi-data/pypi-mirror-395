from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (empty, FSharpList, map, append)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from .expression import (RequiredSource_1__ctor_2B595, RequiredSource_1, OptionalSource_1__ctor_2B595, OptionalSource_1, RequiredSource_1__get_Source, OptionalSource_1__get_Source)
from .types import (SheetEntity_1_some_2B595, SheetEntity_1, RowElement, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr280() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.RowBuilder", None, RowBuilder)


class RowBuilder:
    def __init__(self, __unit: None=None) -> None:
        pass


RowBuilder_reflection = _expr280

def RowBuilder__ctor(__unit: None=None) -> RowBuilder:
    return RowBuilder(__unit)


def RowBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[RowElement]]:
    return SheetEntity_1_some_2B595(empty())


def RowBuilder__SignMessages_3F89FFFC(this: RowBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow281(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo: Callable[[str], str] = to_text(printf("In Row: %s"))
            return clo

        return Message__MapText_11D407F6(m, _arrow281())

    return map(mapping, messages)


def RowBuilder__Combine_19F30600(this: RowBuilder, wx1: SheetEntity_1[FSharpList[RowElement]], wx2: SheetEntity_1[FSharpList[RowElement]]) -> SheetEntity_1[FSharpList[RowElement]]:
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



def RowBuilder__Combine_ZC028CBD(this: RowBuilder, wx1: RequiredSource_1[None], wx2: SheetEntity_1[FSharpList[RowElement]]) -> RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return RequiredSource_1__ctor_2B595(wx2)


def RowBuilder__Combine_7DC18FE3(this: RowBuilder, wx1: SheetEntity_1[FSharpList[RowElement]], wx2: RequiredSource_1[None]) -> RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return RequiredSource_1__ctor_2B595(wx1)


def RowBuilder__Combine_Z1FF3C0DC(this: RowBuilder, wx1: OptionalSource_1[None], wx2: SheetEntity_1[FSharpList[RowElement]]) -> OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return OptionalSource_1__ctor_2B595(wx2)


def RowBuilder__Combine_Z47B5345C(this: RowBuilder, wx1: SheetEntity_1[FSharpList[RowElement]], wx2: OptionalSource_1[None]) -> OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return OptionalSource_1__ctor_2B595(wx1)


def RowBuilder__Combine_385AF66F(this: RowBuilder, wx1: RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]], wx2: SheetEntity_1[FSharpList[RowElement]]) -> RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return RequiredSource_1__ctor_2B595(RowBuilder__Combine_19F30600(this, RequiredSource_1__get_Source(wx1), wx2))


def RowBuilder__Combine_16FE340F(this: RowBuilder, wx1: SheetEntity_1[FSharpList[RowElement]], wx2: RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]]) -> RequiredSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return RequiredSource_1__ctor_2B595(RowBuilder__Combine_19F30600(this, wx1, RequiredSource_1__get_Source(wx2)))


def RowBuilder__Combine_Z4C077C38(this: RowBuilder, wx1: OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]], wx2: SheetEntity_1[FSharpList[RowElement]]) -> OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return OptionalSource_1__ctor_2B595(RowBuilder__Combine_19F30600(this, OptionalSource_1__get_Source(wx1), wx2))


def RowBuilder__Combine_Z23359F38(this: RowBuilder, wx1: SheetEntity_1[FSharpList[RowElement]], wx2: OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]]) -> OptionalSource_1[SheetEntity_1[FSharpList[RowElement]]]:
    return OptionalSource_1__ctor_2B595(RowBuilder__Combine_19F30600(this, wx1, OptionalSource_1__get_Source(wx2)))


__all__ = ["RowBuilder_reflection", "RowBuilder_get_Empty", "RowBuilder__SignMessages_3F89FFFC", "RowBuilder__Combine_19F30600", "RowBuilder__Combine_ZC028CBD", "RowBuilder__Combine_7DC18FE3", "RowBuilder__Combine_Z1FF3C0DC", "RowBuilder__Combine_Z47B5345C", "RowBuilder__Combine_385AF66F", "RowBuilder__Combine_16FE340F", "RowBuilder__Combine_Z4C077C38", "RowBuilder__Combine_Z23359F38"]


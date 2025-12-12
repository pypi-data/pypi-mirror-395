from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.list import (empty, FSharpList, map, append)
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from .expression import (RequiredSource_1__ctor_2B595, RequiredSource_1, OptionalSource_1__ctor_2B595, OptionalSource_1, RequiredSource_1__get_Source, OptionalSource_1__get_Source)
from .types import (SheetEntity_1_some_2B595, SheetEntity_1, ColumnElement, Message__MapText_11D407F6, Message, SheetEntity_1__get_Messages)

def _expr282() -> TypeInfo:
    return class_type("FsSpreadsheet.DSL.ColumnBuilder", None, ColumnBuilder)


class ColumnBuilder:
    def __init__(self, __unit: None=None) -> None:
        pass


ColumnBuilder_reflection = _expr282

def ColumnBuilder__ctor(__unit: None=None) -> ColumnBuilder:
    return ColumnBuilder(__unit)


def ColumnBuilder_get_Empty(__unit: None=None) -> SheetEntity_1[FSharpList[ColumnElement]]:
    return SheetEntity_1_some_2B595(empty())


def ColumnBuilder__SignMessages_3F89FFFC(this: ColumnBuilder, messages: FSharpList[Message]) -> FSharpList[Message]:
    def mapping(m: Message, this: Any=this, messages: Any=messages) -> Message:
        def _arrow283(__unit: None=None, m: Any=m) -> Callable[[str], str]:
            clo: Callable[[str], str] = to_text(printf("In Column: %s"))
            return clo

        return Message__MapText_11D407F6(m, _arrow283())

    return map(mapping, messages)


def ColumnBuilder__Combine_Z14A04580(this: ColumnBuilder, wx1: SheetEntity_1[FSharpList[ColumnElement]], wx2: SheetEntity_1[FSharpList[ColumnElement]]) -> SheetEntity_1[FSharpList[ColumnElement]]:
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



def ColumnBuilder__Combine_89C473F(this: ColumnBuilder, wx1: RequiredSource_1[None], wx2: SheetEntity_1[FSharpList[ColumnElement]]) -> RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return RequiredSource_1__ctor_2B595(wx2)


def ColumnBuilder__Combine_740C071F(this: ColumnBuilder, wx1: SheetEntity_1[FSharpList[ColumnElement]], wx2: RequiredSource_1[None]) -> RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return RequiredSource_1__ctor_2B595(wx1)


def ColumnBuilder__Combine_1B6D0B58(this: ColumnBuilder, wx1: OptionalSource_1[None], wx2: SheetEntity_1[FSharpList[ColumnElement]]) -> OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return OptionalSource_1__ctor_2B595(wx2)


def ColumnBuilder__Combine_Z4E78BCA8(this: ColumnBuilder, wx1: SheetEntity_1[FSharpList[ColumnElement]], wx2: OptionalSource_1[None]) -> OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return OptionalSource_1__ctor_2B595(wx1)


def ColumnBuilder__Combine_F0E07EF(this: ColumnBuilder, wx1: RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]], wx2: SheetEntity_1[FSharpList[ColumnElement]]) -> RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return RequiredSource_1__ctor_2B595(ColumnBuilder__Combine_Z14A04580(this, RequiredSource_1__get_Source(wx1), wx2))


def ColumnBuilder__Combine_48CBECF(this: ColumnBuilder, wx1: SheetEntity_1[FSharpList[ColumnElement]], wx2: RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]]) -> RequiredSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return RequiredSource_1__ctor_2B595(ColumnBuilder__Combine_Z14A04580(this, wx1, RequiredSource_1__get_Source(wx2)))


def ColumnBuilder__Combine_Z172253D8(this: ColumnBuilder, wx1: OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]], wx2: SheetEntity_1[FSharpList[ColumnElement]]) -> OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return OptionalSource_1__ctor_2B595(ColumnBuilder__Combine_Z14A04580(this, OptionalSource_1__get_Source(wx1), wx2))


def ColumnBuilder__Combine_Z73B7C9D8(this: ColumnBuilder, wx1: SheetEntity_1[FSharpList[ColumnElement]], wx2: OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]]) -> OptionalSource_1[SheetEntity_1[FSharpList[ColumnElement]]]:
    return OptionalSource_1__ctor_2B595(ColumnBuilder__Combine_Z14A04580(this, wx1, OptionalSource_1__get_Source(wx2)))


__all__ = ["ColumnBuilder_reflection", "ColumnBuilder_get_Empty", "ColumnBuilder__SignMessages_3F89FFFC", "ColumnBuilder__Combine_Z14A04580", "ColumnBuilder__Combine_89C473F", "ColumnBuilder__Combine_740C071F", "ColumnBuilder__Combine_1B6D0B58", "ColumnBuilder__Combine_Z4E78BCA8", "ColumnBuilder__Combine_F0E07EF", "ColumnBuilder__Combine_48CBECF", "ColumnBuilder__Combine_Z172253D8", "ColumnBuilder__Combine_Z73B7C9D8"]


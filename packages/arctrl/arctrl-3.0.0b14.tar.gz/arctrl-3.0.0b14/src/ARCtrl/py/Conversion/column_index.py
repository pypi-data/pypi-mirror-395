from __future__ import annotations
from typing import Any
from ..ROCrate.ldobject import LDNode
from ..fable_modules.fable_library.int32 import try_parse
from ..fable_modules.fable_library.option import value
from ..fable_modules.fable_library.types import FSharpRef
from ..fable_modules.fable_library.util import int32_to_string

def try_int(str_1: str) -> int | None:
    match_value: tuple[bool, int]
    out_arg: int = 0
    def _arrow3872(__unit: None=None, str_1: Any=str_1) -> int:
        return out_arg

    def _arrow3873(v: int, str_1: Any=str_1) -> None:
        nonlocal out_arg
        out_arg = v or 0

    match_value = (try_parse(str_1, 511, False, 32, FSharpRef(_arrow3872, _arrow3873)), out_arg)
    if match_value[0]:
        return match_value[1]

    else: 
        return None



order_name: str = "columnIndex"

columnd_index_property: str = "https://w3id.org/ro/terms/arc#columnIndex"

def try_get_index(node: LDNode) -> int | None:
    match_value: Any | None = node.TryGetPropertyAsSingleton(columnd_index_property)
    (pattern_matching_result, ci) = (None, None)
    if match_value is not None:
        if str(type(value(match_value))) == "<class \'str\'>":
            pattern_matching_result = 0
            ci = value(match_value)

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return try_int(ci)

    elif pattern_matching_result == 1:
        match_value_1: Any | None = node.TryGetPropertyAsSingleton(order_name)
        (pattern_matching_result_1, ci_1) = (None, None)
        if match_value_1 is not None:
            if str(type(value(match_value_1))) == "<class \'str\'>":
                pattern_matching_result_1 = 0
                ci_1 = value(match_value_1)

            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1

        if pattern_matching_result_1 == 0:
            return try_int(ci_1)

        elif pattern_matching_result_1 == 1:
            return None




def set_index(node: LDNode, index: int) -> None:
    node.SetProperty(columnd_index_property, int32_to_string(index))


def ARCtrl_ROCrate_LDNode__LDNode_GetColumnIndex(this: LDNode) -> int:
    return value(try_get_index(this))


def ARCtrl_ROCrate_LDNode__LDNode_TryGetColumnIndex(this: LDNode) -> int | None:
    return try_get_index(this)


def ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4(this: LDNode, index: int) -> None:
    set_index(this, index)


__all__ = ["try_int", "order_name", "columnd_index_property", "try_get_index", "set_index", "ARCtrl_ROCrate_LDNode__LDNode_GetColumnIndex", "ARCtrl_ROCrate_LDNode__LDNode_TryGetColumnIndex", "ARCtrl_ROCrate_LDNode__LDNode_SetColumnIndex_Z524259A4"]


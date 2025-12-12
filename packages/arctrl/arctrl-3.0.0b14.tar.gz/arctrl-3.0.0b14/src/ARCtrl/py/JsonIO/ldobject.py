from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Json.encode import default_spaces
from ..Json.ROCrate.ldgraph import (decoder as decoder_2, encoder as encoder_1)
from ..Json.ROCrate.ldnode import (decoder as decoder_1, encoder)
from ..ROCrate.ldobject import (LDNode, LDGraph)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_ROCrate_LDNode__LDNode_fromROCrateJsonString_Static_Z721C83C5(s: str) -> LDNode:
    match_value: FSharpResult_2[LDNode, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ROCrate_LDNode__LDNode_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[LDNode], str]:
    def _arrow3868(obj: LDNode, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3868


def ARCtrl_ROCrate_LDNode__LDNode_ToROCrateJsonString_71136F3F(this: LDNode, spaces: int | None=None) -> str:
    return ARCtrl_ROCrate_LDNode__LDNode_toROCrateJsonString_Static_71136F3F(spaces)(this)


def _expr3869() -> TypeInfo:
    return class_type("ARCtrl.Json.LDNodeExtensions.PyJsInterop", None, LDNodeExtensions_PyJsInterop)


class LDNodeExtensions_PyJsInterop:
    @staticmethod
    def from_rocrate_json_string(s: str) -> LDNode:
        match_value: FSharpResult_2[LDNode, str] = Decode_fromString(decoder_1, s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    @staticmethod
    def to_rocrate_json_string(node: LDNode, spaces: int | None=None) -> str:
        value: IEncodable = encoder(node)
        return to_string(default_spaces(spaces), value)


LDNodeExtensions_PyJsInterop_reflection = _expr3869

def ARCtrl_ROCrate_LDGraph__LDGraph_fromROCrateJsonString_Static_Z721C83C5(s: str) -> LDGraph:
    match_value: FSharpResult_2[LDGraph, str] = Decode_fromString(decoder_2, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ROCrate_LDGraph__LDGraph_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[LDGraph], str]:
    def _arrow3870(obj: LDGraph, spaces: Any=spaces) -> str:
        value: IEncodable = encoder_1(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3870


def ARCtrl_ROCrate_LDGraph__LDGraph_ToROCrateJsonString_71136F3F(this: LDGraph, spaces: int | None=None) -> str:
    return ARCtrl_ROCrate_LDGraph__LDGraph_toROCrateJsonString_Static_71136F3F(spaces)(this)


def _expr3871() -> TypeInfo:
    return class_type("ARCtrl.Json.LDGraphExtensions.PyJsInterop", None, LDGraphExtensions_PyJsInterop)


class LDGraphExtensions_PyJsInterop:
    @staticmethod
    def from_rocrate_json_string(s: str) -> LDGraph:
        match_value: FSharpResult_2[LDGraph, str] = Decode_fromString(decoder_2, s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    @staticmethod
    def to_rocrate_json_string(graph: LDGraph, spaces: int | None=None) -> str:
        value: IEncodable = encoder_1(graph)
        return to_string(default_spaces(spaces), value)


LDGraphExtensions_PyJsInterop_reflection = _expr3871

__all__ = ["ARCtrl_ROCrate_LDNode__LDNode_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ROCrate_LDNode__LDNode_toROCrateJsonString_Static_71136F3F", "ARCtrl_ROCrate_LDNode__LDNode_ToROCrateJsonString_71136F3F", "LDNodeExtensions_PyJsInterop_reflection", "ARCtrl_ROCrate_LDGraph__LDGraph_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ROCrate_LDGraph__LDGraph_toROCrateJsonString_Static_71136F3F", "ARCtrl_ROCrate_LDGraph__LDGraph_ToROCrateJsonString_71136F3F", "LDGraphExtensions_PyJsInterop_reflection"]


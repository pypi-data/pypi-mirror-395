from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.component import Component
from ...Json.encode import default_spaces
from ...Json.Process.component import (ISAJson_decoder, ISAJson_encoder, ROCrate_decoder, ROCrate_encoder)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Process_Component__Component_fromISAJsonString_Static_Z721C83C5(s: str) -> Component:
    match_value: FSharpResult_2[Component, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Component__Component_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Component], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3810(f: Component, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(id_map, f)
        return to_string(default_spaces(spaces), value)

    return _arrow3810


def ARCtrl_Process_Component__Component_toISAJsonString_71136F3F(this: Component, spaces: int | None=None) -> str:
    return ARCtrl_Process_Component__Component_toISAJsonString_Static_Z3B036AA(spaces)(this)


def ARCtrl_Process_Component__Component_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Component:
    match_value: FSharpResult_2[Component, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Component__Component_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Component], str]:
    def _arrow3811(f: Component, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow3811


def ARCtrl_Process_Component__Component_toROCrateJsonString_71136F3F(this: Component, spaces: int | None=None) -> str:
    return ARCtrl_Process_Component__Component_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_Process_Component__Component_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_Component__Component_toISAJsonString_Static_Z3B036AA", "ARCtrl_Process_Component__Component_toISAJsonString_71136F3F", "ARCtrl_Process_Component__Component_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Process_Component__Component_toROCrateJsonString_Static_71136F3F", "ARCtrl_Process_Component__Component_toROCrateJsonString_71136F3F"]


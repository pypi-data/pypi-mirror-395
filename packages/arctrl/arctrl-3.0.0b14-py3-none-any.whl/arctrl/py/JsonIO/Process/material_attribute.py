from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.material_attribute import MaterialAttribute
from ...Json.encode import default_spaces
from ...Json.Process.material_attribute import (decoder as decoder_1, encoder)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Process_MaterialAttribute__MaterialAttribute_fromISAJsonString_Static_Z721C83C5(s: str) -> MaterialAttribute:
    match_value: FSharpResult_2[MaterialAttribute, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_MaterialAttribute__MaterialAttribute_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[MaterialAttribute], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3809(v: MaterialAttribute, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = encoder(id_map, v)
        return to_string(default_spaces(spaces), value)

    return _arrow3809


def ARCtrl_Process_MaterialAttribute__MaterialAttribute_ToJsonString_Z3B036AA(this: MaterialAttribute, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Process_MaterialAttribute__MaterialAttribute_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["ARCtrl_Process_MaterialAttribute__MaterialAttribute_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_toISAJsonString_Static_Z3B036AA", "ARCtrl_Process_MaterialAttribute__MaterialAttribute_ToJsonString_Z3B036AA"]


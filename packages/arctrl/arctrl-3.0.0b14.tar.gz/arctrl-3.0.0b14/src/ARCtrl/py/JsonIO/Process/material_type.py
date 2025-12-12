from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.material_type import MaterialType
from ...Json.encode import default_spaces
from ...Json.Process.material_type import (ISAJson_decoder, ISAJson_encoder)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Process_MaterialType__MaterialType_fromISAJsonString_Static_Z721C83C5(s: str) -> MaterialType:
    match_value: FSharpResult_2[MaterialType, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_MaterialType__MaterialType_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[MaterialType], str]:
    def _arrow3808(f: MaterialType, spaces: Any=spaces) -> str:
        value: IEncodable = ISAJson_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow3808


def ARCtrl_Process_MaterialType__MaterialType_ToISAJsonString_71136F3F(this: MaterialType, spaces: int | None=None) -> str:
    return ARCtrl_Process_MaterialType__MaterialType_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_Process_MaterialType__MaterialType_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_MaterialType__MaterialType_toISAJsonString_Static_71136F3F", "ARCtrl_Process_MaterialType__MaterialType_ToISAJsonString_71136F3F"]


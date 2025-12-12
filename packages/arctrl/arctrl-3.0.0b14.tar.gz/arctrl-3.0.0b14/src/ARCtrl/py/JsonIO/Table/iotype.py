from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Table.composite_header import IOType
from ...Json.encode import default_spaces
from ...Json.Table.iotype import (decoder as decoder_1, encoder)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_IOType__IOType_fromJsonString_Static_Z721C83C5(s: str) -> IOType:
    match_value: FSharpResult_2[IOType, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_IOType__IOType_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[IOType], str]:
    def _arrow3841(obj: IOType, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3841


def ARCtrl_IOType__IOType_ToJsonString_71136F3F(this: IOType, spaces: int | None=None) -> str:
    return ARCtrl_IOType__IOType_toJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_IOType__IOType_fromJsonString_Static_Z721C83C5", "ARCtrl_IOType__IOType_toJsonString_Static_71136F3F", "ARCtrl_IOType__IOType_ToJsonString_71136F3F"]


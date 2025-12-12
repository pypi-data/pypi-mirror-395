from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.datamap import Datamap
from ..Json.Datamap.datamap import (decoder as decoder_1, encoder)
from ..Json.encode import default_spaces
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Datamap__Datamap_fromJsonString_Static_Z721C83C5(s: str) -> Datamap:
    match_value: FSharpResult_2[Datamap, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Datamap__Datamap_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Datamap], str]:
    def _arrow3797(obj: Datamap, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3797


def ARCtrl_Datamap__Datamap_ToJsonString_71136F3F(this: Datamap, spaces: int | None=None) -> str:
    return ARCtrl_Datamap__Datamap_toJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_Datamap__Datamap_fromJsonString_Static_Z721C83C5", "ARCtrl_Datamap__Datamap_toJsonString_Static_71136F3F", "ARCtrl_Datamap__Datamap_ToJsonString_71136F3F"]


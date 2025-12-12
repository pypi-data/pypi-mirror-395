from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.arc_types import ArcRun
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.composite_cell import CompositeCell
from ..Json.encode import default_spaces
from ..Json.run import (decoder as decoder_1, encoder, decoder_compressed, encoder_compressed)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from .Table.compression import (decode, encode)

def ARCtrl_ArcRun__ArcRun_fromJsonString_Static_Z721C83C5(s: str) -> ArcRun:
    match_value: FSharpResult_2[ArcRun, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcRun__ArcRun_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcRun], str]:
    def _arrow3862(obj: ArcRun, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3862


def ARCtrl_ArcRun__ArcRun_ToJsonString_71136F3F(this: ArcRun, spaces: int | None=None) -> str:
    return ARCtrl_ArcRun__ArcRun_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcRun__ArcRun_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcRun:
    try: 
        match_value: FSharpResult_2[ArcRun, str] = Decode_fromString(decode(decoder_compressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcRun: %s"))(arg_1)



def ARCtrl_ArcRun__ArcRun_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcRun], str]:
    def _arrow3863(obj: ArcRun, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(encoder_compressed, obj))

    return _arrow3863


def ARCtrl_ArcRun__ArcRun_ToCompressedJsonString_71136F3F(this: ArcRun, spaces: int | None=None) -> str:
    return ARCtrl_ArcRun__ArcRun_toCompressedJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_ArcRun__ArcRun_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcRun__ArcRun_toJsonString_Static_71136F3F", "ARCtrl_ArcRun__ArcRun_ToJsonString_71136F3F", "ARCtrl_ArcRun__ArcRun_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcRun__ArcRun_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcRun__ArcRun_ToCompressedJsonString_71136F3F"]


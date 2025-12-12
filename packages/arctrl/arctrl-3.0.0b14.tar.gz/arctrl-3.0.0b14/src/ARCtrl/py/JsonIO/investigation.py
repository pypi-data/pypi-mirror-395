from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.arc_types import ArcInvestigation
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.composite_cell import CompositeCell
from ..Json.encode import default_spaces
from ..Json.investigation import (decoder as decoder_1, encoder, decoder_compressed, encoder_compressed, ROCrate_decoder, ROCrate_encoder, ISAJson_encoder, ISAJson_decoder)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from .Table.compression import (decode, encode)

def ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow3864(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3864


def ARCtrl_ArcInvestigation__ArcInvestigation_ToJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    try: 
        match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(decode(decoder_compressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow3865(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(encoder_compressed, obj))

    return _arrow3865


def ARCtrl_ArcInvestigation__ArcInvestigation_ToCompressedJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcInvestigation], str]:
    def _arrow3866(obj: ArcInvestigation, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3866


def ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateJsonString_71136F3F(this: ArcInvestigation, spaces: int | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcInvestigation], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3867(obj: ArcInvestigation, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3867


def ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5(s: str) -> ArcInvestigation:
    match_value: FSharpResult_2[ArcInvestigation, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcInvestigation__ArcInvestigation_ToISAJsonString_Z3B036AA(this: ArcInvestigation, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["ARCtrl_ArcInvestigation__ArcInvestigation_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToCompressedJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_toROCrateJsonString_Static_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_ToROCrateJsonString_71136F3F", "ARCtrl_ArcInvestigation__ArcInvestigation_toISAJsonString_Static_Z3B036AA", "ARCtrl_ArcInvestigation__ArcInvestigation_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcInvestigation__ArcInvestigation_ToISAJsonString_Z3B036AA"]


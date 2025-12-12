from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.arc_types import (ArcStudy, ArcAssay)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.composite_cell import CompositeCell
from ..Json.encode import default_spaces
from ..Json.study import (decoder as decoder_1, encoder, decoder_compressed, encoder_compressed, ROCrate_decoder, ROCrate_encoder, ISAJson_decoder, ISAJson_encoder)
from ..fable_modules.fable_library.list import FSharpList
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from .Table.compression import (decode, encode)

def ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5(s: str) -> ArcStudy:
    match_value: FSharpResult_2[ArcStudy, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow3856(obj: ArcStudy, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3856


def ARCtrl_ArcStudy__ArcStudy_ToJsonString_71136F3F(this: ArcStudy, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcStudy:
    try: 
        match_value: FSharpResult_2[ArcStudy, str] = Decode_fromString(decode(decoder_compressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcStudy: %s"))(arg_1)



def ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow3857(obj: ArcStudy, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(encoder_compressed, obj))

    return _arrow3857


def ARCtrl_ArcStudy__ArcStudy_ToCompressedJsonString_71136F3F(this: ArcStudy, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5(s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    match_value: FSharpResult_2[tuple[ArcStudy, FSharpList[ArcAssay]], str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086(assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None) -> Callable[[ArcStudy], str]:
    def _arrow3858(obj: ArcStudy, assays: Any=assays, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(assays, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3858


def ARCtrl_ArcStudy__ArcStudy_ToROCrateJsonString_3BA23086(this: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086(assays, spaces)(this)


def ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5(s: str) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    match_value: FSharpResult_2[tuple[ArcStudy, FSharpList[ArcAssay]], str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1(assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcStudy], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3859(obj: ArcStudy, assays: Any=assays, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(id_map, assays, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3859


def ARCtrl_ArcStudy__ArcStudy_ToISAJsonString_Z3FD920F1(this: ArcStudy, assays: FSharpList[ArcAssay] | None=None, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1(assays, spaces, use_idreferencing)(this)


__all__ = ["ARCtrl_ArcStudy__ArcStudy_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toJsonString_Static_71136F3F", "ARCtrl_ArcStudy__ArcStudy_ToJsonString_71136F3F", "ARCtrl_ArcStudy__ArcStudy_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcStudy__ArcStudy_ToCompressedJsonString_71136F3F", "ARCtrl_ArcStudy__ArcStudy_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toROCrateJsonString_Static_3BA23086", "ARCtrl_ArcStudy__ArcStudy_ToROCrateJsonString_3BA23086", "ARCtrl_ArcStudy__ArcStudy_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcStudy__ArcStudy_toISAJsonString_Static_Z3FD920F1", "ARCtrl_ArcStudy__ArcStudy_ToISAJsonString_Z3FD920F1"]


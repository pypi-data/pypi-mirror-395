from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.arc_types import ArcAssay
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.Table.composite_cell import CompositeCell
from ..Json.assay import (decoder as decoder_1, encoder, decoder_compressed, encoder_compressed, ROCrate_decoder, ROCrate_encoder, ISAJson_encoder, ISAJson_decoder)
from ..Json.encode import default_spaces
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf, to_fail)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.thoth_json_core.types import (IEncodable, Decoder_1)
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from .Table.compression import (decode, encode)

def ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow3852(obj: ArcAssay, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3852


def ARCtrl_ArcAssay__ArcAssay_ToJsonString_71136F3F(this: ArcAssay, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    try: 
        match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(decode(decoder_compressed), s)
        if match_value.tag == 1:
            raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

        else: 
            return match_value.fields[0]


    except Exception as e_1:
        arg_1: str = str(e_1)
        return to_fail(printf("Error. Unable to parse json string to ArcAssay: %s"))(arg_1)



def ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow3853(obj: ArcAssay, spaces: Any=spaces) -> str:
        return to_string(default_arg(spaces, 0), encode(encoder_compressed, obj))

    return _arrow3853


def ARCtrl_ArcAssay__ArcAssay_ToCompressedJsonString_71136F3F(this: ArcAssay, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47(study_name: str | None=None, spaces: int | None=None) -> Callable[[ArcAssay], str]:
    def _arrow3854(obj: ArcAssay, study_name: Any=study_name, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(study_name, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3854


def ARCtrl_ArcAssay__ArcAssay_ToROCrateJsonString_5CABCA47(this: ArcAssay, study_name: str | None=None, spaces: int | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47(study_name, spaces)(this)


def ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[ArcAssay], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3855(obj: ArcAssay, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(None, id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3855


def ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5(s: str) -> ArcAssay:
    match_value: FSharpResult_2[ArcAssay, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ArcAssay__ArcAssay_ToISAJsonString_Z3B036AA(this: ArcAssay, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["ARCtrl_ArcAssay__ArcAssay_fromJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toJsonString_Static_71136F3F", "ARCtrl_ArcAssay__ArcAssay_ToJsonString_71136F3F", "ARCtrl_ArcAssay__ArcAssay_fromCompressedJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toCompressedJsonString_Static_71136F3F", "ARCtrl_ArcAssay__ArcAssay_ToCompressedJsonString_71136F3F", "ARCtrl_ArcAssay__ArcAssay_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_toROCrateJsonString_Static_5CABCA47", "ARCtrl_ArcAssay__ArcAssay_ToROCrateJsonString_5CABCA47", "ARCtrl_ArcAssay__ArcAssay_toISAJsonString_Static_Z3B036AA", "ARCtrl_ArcAssay__ArcAssay_fromISAJsonString_Static_Z721C83C5", "ARCtrl_ArcAssay__ArcAssay_ToISAJsonString_Z3B036AA"]


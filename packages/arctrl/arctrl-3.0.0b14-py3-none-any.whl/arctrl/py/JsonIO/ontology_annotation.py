from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.ontology_annotation import OntologyAnnotation
from ..Json.encode import default_spaces
from ..Json.ontology_annotation import (OntologyAnnotation_decoder, OntologyAnnotation_encoder, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ISAJson_decoder, OntologyAnnotation_ISAJson_encoder)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow3787(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: IEncodable = OntologyAnnotation_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3787


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ROCrate_decoderDefinedTerm, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow3788(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: IEncodable = OntologyAnnotation_ROCrate_encoderDefinedTerm(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3788


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToROCrateJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5(s: str) -> OntologyAnnotation:
    match_value: FSharpResult_2[OntologyAnnotation, str] = Decode_fromString(OntologyAnnotation_ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologyAnnotation], str]:
    def _arrow3789(obj: OntologyAnnotation, spaces: Any=spaces) -> str:
        value: IEncodable = OntologyAnnotation_ISAJson_encoder(None, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3789


def ARCtrl_OntologyAnnotation__OntologyAnnotation_ToISAJsonString_71136F3F(this: OntologyAnnotation, spaces: int | None=None) -> str:
    return ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_OntologyAnnotation__OntologyAnnotation_fromJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToJsonString_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toROCrateJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToROCrateJsonString_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_fromISAJsonString_Static_Z721C83C5", "ARCtrl_OntologyAnnotation__OntologyAnnotation_toISAJsonString_Static_71136F3F", "ARCtrl_OntologyAnnotation__OntologyAnnotation_ToISAJsonString_71136F3F"]


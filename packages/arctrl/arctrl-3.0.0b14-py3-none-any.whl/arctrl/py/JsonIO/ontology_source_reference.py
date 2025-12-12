from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.ontology_source_reference import OntologySourceReference
from ..Json.encode import default_spaces
from ..Json.ontology_source_reference import (decoder as decoder_1, encoder, ROCrate_decoder, ROCrate_encoder, ISAJson_decoder, ISAJson_encoder)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_OntologySourceReference__OntologySourceReference_fromJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow3790(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3790


def ARCtrl_OntologySourceReference__OntologySourceReference_ToJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologySourceReference__OntologySourceReference_fromROCrateJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow3791(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3791


def ARCtrl_OntologySourceReference__OntologySourceReference_ToROCrateJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_OntologySourceReference__OntologySourceReference_fromISAJsonString_Static_Z721C83C5(s: str) -> OntologySourceReference:
    match_value: FSharpResult_2[OntologySourceReference, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[OntologySourceReference], str]:
    def _arrow3792(obj: OntologySourceReference, spaces: Any=spaces) -> str:
        value: IEncodable = ISAJson_encoder(None, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3792


def ARCtrl_OntologySourceReference__OntologySourceReference_ToISAJsonString_71136F3F(this: OntologySourceReference, spaces: int | None=None) -> str:
    return ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_OntologySourceReference__OntologySourceReference_fromJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToJsonString_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toROCrateJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToROCrateJsonString_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_fromISAJsonString_Static_Z721C83C5", "ARCtrl_OntologySourceReference__OntologySourceReference_toISAJsonString_Static_71136F3F", "ARCtrl_OntologySourceReference__OntologySourceReference_ToISAJsonString_71136F3F"]


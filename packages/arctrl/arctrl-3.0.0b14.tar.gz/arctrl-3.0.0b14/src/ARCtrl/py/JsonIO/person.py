from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.person import Person
from ..Json.encode import default_spaces
from ..Json.person import (decoder as decoder_1, encoder, ROCrate_decoder, ROCrate_encoder, ISAJson_decoder, ISAJson_encoder)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Person__Person_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Person], str]:
    def _arrow3798(obj: Person, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3798


def ARCtrl_Person__Person_toJsonString_71136F3F(this: Person, spaces: int | None=None) -> str:
    return ARCtrl_Person__Person_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Person__Person_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Person], str]:
    def _arrow3799(obj: Person, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3799


def ARCtrl_Person__Person_toROCrateJsonString_71136F3F(this: Person, spaces: int | None=None) -> str:
    return ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5(s: str) -> Person:
    match_value: FSharpResult_2[Person, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Person__Person_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Person], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3800(obj: Person, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(id_map, obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3800


def ARCtrl_Person__Person_toISAJsonString_Z3B036AA(this: Person, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Person__Person_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


__all__ = ["ARCtrl_Person__Person_fromJsonString_Static_Z721C83C5", "ARCtrl_Person__Person_toJsonString_Static_71136F3F", "ARCtrl_Person__Person_toJsonString_71136F3F", "ARCtrl_Person__Person_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Person__Person_toROCrateJsonString_Static_71136F3F", "ARCtrl_Person__Person_toROCrateJsonString_71136F3F", "ARCtrl_Person__Person_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Person__Person_toISAJsonString_Static_Z3B036AA", "ARCtrl_Person__Person_toISAJsonString_Z3B036AA"]


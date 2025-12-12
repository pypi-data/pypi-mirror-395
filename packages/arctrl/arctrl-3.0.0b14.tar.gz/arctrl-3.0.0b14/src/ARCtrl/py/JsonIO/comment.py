from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.comment import Comment
from ..Json.comment import (decoder as decoder_1, encoder, ROCrate_decoder, ROCrate_encoder, ISAJson_decoder, ISAJson_encoder)
from ..Json.encode import default_spaces
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Comment__Comment_fromJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow3784(c: Comment, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(c)
        return to_string(default_spaces(spaces), value)

    return _arrow3784


def ARCtrl_Comment__Comment_toJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Comment__Comment_fromROCrateJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow3785(c: Comment, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(c)
        return to_string(default_spaces(spaces), value)

    return _arrow3785


def ARCtrl_Comment__Comment_toROCrateJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_Comment__Comment_fromISAJsonString_Static_Z721C83C5(s: str) -> Comment:
    match_value: FSharpResult_2[Comment, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[Comment], str]:
    def _arrow3786(c: Comment, spaces: Any=spaces) -> str:
        value: IEncodable = ISAJson_encoder(None, c)
        return to_string(default_spaces(spaces), value)

    return _arrow3786


def ARCtrl_Comment__Comment_toISAJsonString_71136F3F(this: Comment, spaces: int | None=None) -> str:
    return ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_Comment__Comment_fromJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toJsonString_71136F3F", "ARCtrl_Comment__Comment_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toROCrateJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toROCrateJsonString_71136F3F", "ARCtrl_Comment__Comment_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Comment__Comment_toISAJsonString_Static_71136F3F", "ARCtrl_Comment__Comment_toISAJsonString_71136F3F"]


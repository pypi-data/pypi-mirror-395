from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..Core.data_file import DataFile
from ..Json.data_file import (ISAJson_decoder, ISAJson_encoder, ROCrate_decoder, ROCrate_encoder)
from ..Json.encode import default_spaces
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string

def ARCtrl_DataFile__DataFile_fromISAJsonString_Static_Z721C83C5(s: str) -> DataFile:
    match_value: FSharpResult_2[DataFile, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_DataFile__DataFile_toISAJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[DataFile], str]:
    def _arrow3793(f: DataFile, spaces: Any=spaces) -> str:
        value: IEncodable = ISAJson_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow3793


def ARCtrl_DataFile__DataFile_ToISAJsonString_71136F3F(this: DataFile, spaces: int | None=None) -> str:
    return ARCtrl_DataFile__DataFile_toISAJsonString_Static_71136F3F(spaces)(this)


def ARCtrl_DataFile__DataFile_fromROCrateJsonString_Static_Z721C83C5(s: str) -> DataFile:
    match_value: FSharpResult_2[DataFile, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_DataFile__DataFile_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[DataFile], str]:
    def _arrow3794(f: DataFile, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(f)
        return to_string(default_spaces(spaces), value)

    return _arrow3794


def ARCtrl_DataFile__DataFile_ToROCrateJsonString_71136F3F(this: DataFile, spaces: int | None=None) -> str:
    return ARCtrl_DataFile__DataFile_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_DataFile__DataFile_fromISAJsonString_Static_Z721C83C5", "ARCtrl_DataFile__DataFile_toISAJsonString_Static_71136F3F", "ARCtrl_DataFile__DataFile_ToISAJsonString_71136F3F", "ARCtrl_DataFile__DataFile_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_DataFile__DataFile_toROCrateJsonString_Static_71136F3F", "ARCtrl_DataFile__DataFile_ToROCrateJsonString_71136F3F"]


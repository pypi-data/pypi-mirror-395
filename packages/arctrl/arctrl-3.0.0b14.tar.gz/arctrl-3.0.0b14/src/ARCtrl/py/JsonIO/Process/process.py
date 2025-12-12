from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.process import Process
from ...Json.encode import default_spaces
from ...Json.Process.process import (ISAJson_decoder, ISAJson_encoder, ROCrate_decoder, ROCrate_encoder)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Process_Process__Process_fromISAJsonString_Static_Z721C83C5(s: str) -> Process:
    match_value: FSharpResult_2[Process, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Process__Process_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Process], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3827(f: Process, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(None, None, id_map, f)
        return to_string(default_spaces(spaces), value)

    return _arrow3827


def ARCtrl_Process_Process__Process_ToISAJsonString_Z3B036AA(this: Process, spaces: int | None=None, use_idreferencing: bool | None=None) -> str:
    return ARCtrl_Process_Process__Process_toISAJsonString_Static_Z3B036AA(spaces, use_idreferencing)(this)


def ARCtrl_Process_Process__Process_fromROCrateString_Static_Z721C83C5(s: str) -> Process:
    match_value: FSharpResult_2[Process, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F(study_name: str | None=None, assay_name: str | None=None, spaces: int | None=None) -> Callable[[Process], str]:
    def _arrow3828(f: Process, study_name: Any=study_name, assay_name: Any=assay_name, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(study_name, assay_name, f)
        return to_string(default_spaces(spaces), value)

    return _arrow3828


def ARCtrl_Process_Process__Process_ToROCrateString_39E0BC3F(this: Process, study_name: str | None=None, assay_name: str | None=None, spaces: int | None=None) -> str:
    return ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F(study_name, assay_name, spaces)(this)


__all__ = ["ARCtrl_Process_Process__Process_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_Process__Process_toISAJsonString_Static_Z3B036AA", "ARCtrl_Process_Process__Process_ToISAJsonString_Z3B036AA", "ARCtrl_Process_Process__Process_fromROCrateString_Static_Z721C83C5", "ARCtrl_Process_Process__Process_toROCrateString_Static_39E0BC3F", "ARCtrl_Process_Process__Process_ToROCrateString_39E0BC3F"]


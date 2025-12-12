from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.protocol import Protocol
from ...Json.encode import default_spaces
from ...Json.Process.protocol import (ISAJson_decoder, ISAJson_encoder, ROCrate_decoder, ROCrate_encoder)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def ARCtrl_Process_Protocol__Protocol_fromISAJsonString_Static_Z721C83C5(s: str) -> Protocol:
    match_value: FSharpResult_2[Protocol, str] = Decode_fromString(ISAJson_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Protocol__Protocol_toISAJsonString_Static_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[Protocol], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3812(f: Protocol, spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        value: IEncodable = ISAJson_encoder(None, None, None, id_map, f)
        return to_string(default_spaces(spaces), value)

    return _arrow3812


def ARCtrl_Process_Protocol__Protocol_ToISAJsonString_71136F3F(this: Protocol, spaces: int | None=None) -> str:
    return ARCtrl_Process_Protocol__Protocol_toISAJsonString_Static_Z3B036AA(spaces)(this)


def ARCtrl_Process_Protocol__Protocol_fromROCrateString_Static_Z721C83C5(s: str) -> Protocol:
    match_value: FSharpResult_2[Protocol, str] = Decode_fromString(ROCrate_decoder, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_Process_Protocol__Protocol_toROCrateString_Static_Z482224B9(study_name: str | None=None, assay_name: str | None=None, process_name: str | None=None, spaces: int | None=None) -> Callable[[Protocol], str]:
    def _arrow3813(f: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, spaces: Any=spaces) -> str:
        value: IEncodable = ROCrate_encoder(study_name, assay_name, process_name, f)
        return to_string(default_spaces(spaces), value)

    return _arrow3813


def ARCtrl_Process_Protocol__Protocol_ToROCrateString_Z482224B9(this: Protocol, study_name: str | None=None, assay_name: str | None=None, process_name: str | None=None, spaces: int | None=None) -> str:
    return ARCtrl_Process_Protocol__Protocol_toROCrateString_Static_Z482224B9(study_name, assay_name, process_name, spaces)(this)


__all__ = ["ARCtrl_Process_Protocol__Protocol_fromISAJsonString_Static_Z721C83C5", "ARCtrl_Process_Protocol__Protocol_toISAJsonString_Static_Z3B036AA", "ARCtrl_Process_Protocol__Protocol_ToISAJsonString_71136F3F", "ARCtrl_Process_Protocol__Protocol_fromROCrateString_Static_Z721C83C5", "ARCtrl_Process_Protocol__Protocol_toROCrateString_Static_Z482224B9", "ARCtrl_Process_Protocol__Protocol_ToROCrateString_Z482224B9"]


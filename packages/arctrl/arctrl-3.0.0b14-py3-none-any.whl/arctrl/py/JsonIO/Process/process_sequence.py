from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...Core.Process.process import Process
from ...Json.encode import default_spaces
from ...Json.Process.process import (ISAJson_decoder, ISAJson_encoder, ROCrate_decoder, ROCrate_encoder)
from ...fable_modules.fable_library.list import (FSharpList, map)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.string_ import (to_text, printf)
from ...fable_modules.thoth_json_core.decode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_2
from ...fable_modules.thoth_json_core.types import IEncodable
from ...fable_modules.thoth_json_python.decode import Decode_fromString
from ...fable_modules.thoth_json_python.encode import to_string

def _expr3829() -> TypeInfo:
    return class_type("ARCtrl.Json.ProcessSequence", None, ProcessSequence)


class ProcessSequence:
    ...

ProcessSequence_reflection = _expr3829

def ProcessSequence_fromISAJsonString_Z721C83C5(s: str) -> FSharpList[Process]:
    match_value: FSharpResult_2[FSharpList[Process], str] = Decode_fromString(list_1_1(ISAJson_decoder), s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ProcessSequence_toISAJsonString_Z3B036AA(spaces: int | None=None, use_idreferencing: bool | None=None) -> Callable[[FSharpList[Process]], str]:
    id_map: Any | None = dict([]) if default_arg(use_idreferencing, False) else None
    def _arrow3830(f: FSharpList[Process], spaces: Any=spaces, use_idreferencing: Any=use_idreferencing) -> str:
        def mapping(oa: Process) -> IEncodable:
            return ISAJson_encoder(None, None, id_map, oa)

        value: IEncodable = list_1_2(map(mapping, f))
        return to_string(default_spaces(spaces), value)

    return _arrow3830


def ProcessSequence_fromROCrateJsonString_Z721C83C5(s: str) -> FSharpList[Process]:
    match_value: FSharpResult_2[FSharpList[Process], str] = Decode_fromString(list_1_1(ROCrate_decoder), s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ProcessSequence_toROCrateJsonString_39E0BC3F(study_name: str | None=None, assay_name: str | None=None, spaces: int | None=None) -> Callable[[FSharpList[Process]], str]:
    def _arrow3831(f: FSharpList[Process], study_name: Any=study_name, assay_name: Any=assay_name, spaces: Any=spaces) -> str:
        def mapping(oa: Process) -> IEncodable:
            return ROCrate_encoder(study_name, assay_name, oa)

        value: IEncodable = list_1_2(map(mapping, f))
        return to_string(default_spaces(spaces), value)

    return _arrow3831


__all__ = ["ProcessSequence_reflection", "ProcessSequence_fromISAJsonString_Z721C83C5", "ProcessSequence_toISAJsonString_Z3B036AA", "ProcessSequence_fromROCrateJsonString_Z721C83C5", "ProcessSequence_toROCrateJsonString_39E0BC3F"]


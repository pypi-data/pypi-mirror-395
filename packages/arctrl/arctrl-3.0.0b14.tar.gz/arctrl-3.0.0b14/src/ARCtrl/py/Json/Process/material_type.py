from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.thoth_json_core.decode import string
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ...Core.Process.material_type import MaterialType

__A_ = TypeVar("__A_")

def ROCrate_encoder(value: MaterialType) -> IEncodable:
    if value.tag == 1:
        class ObjectExpr2708(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_1.encode_string("Labeled Extract Name")

        return ObjectExpr2708()

    else: 
        class ObjectExpr2709(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers.encode_string("Extract Name")

        return ObjectExpr2709()



class ObjectExpr2710(Decoder_1[MaterialType]):
    def Decode(self, s: IDecoderHelpers_1[Any], json: Any) -> FSharpResult_2[MaterialType, tuple[str, ErrorReason_1[__A_]]]:
        match_value: FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]] = string.Decode(s, json)
        if match_value.tag == 1:
            return FSharpResult_2(1, match_value.fields[0])

        elif match_value.fields[0] == "Extract Name":
            return FSharpResult_2(0, MaterialType(0))

        elif match_value.fields[0] == "Labeled Extract Name":
            return FSharpResult_2(0, MaterialType(1))

        else: 
            s_1: str = match_value.fields[0]
            return FSharpResult_2(1, (("Could not parse " + s_1) + "No other value than \"Extract Name\" or \"Labeled Extract Name\" allowed for materialtype", ErrorReason_1(0, s_1, json)))



ROCrate_decoder: Decoder_1[MaterialType] = ObjectExpr2710()

ISAJson_encoder: Callable[[MaterialType], IEncodable] = ROCrate_encoder

ISAJson_decoder: Decoder_1[MaterialType] = ROCrate_decoder

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]


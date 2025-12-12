from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.thoth_json_core.decode import string
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ..Core.data_file import DataFile

__A_ = TypeVar("__A_")

def ROCrate_encoder(value: DataFile) -> IEncodable:
    if value.tag == 1:
        class ObjectExpr2363(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_1.encode_string("Derived Data File")

        return ObjectExpr2363()

    elif value.tag == 2:
        class ObjectExpr2364(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers_2.encode_string("Image File")

        return ObjectExpr2364()

    else: 
        class ObjectExpr2365(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
                return helpers.encode_string("Raw Data File")

        return ObjectExpr2365()



class ObjectExpr2366(Decoder_1[DataFile]):
    def Decode(self, s: IDecoderHelpers_1[Any], json: Any) -> FSharpResult_2[DataFile, tuple[str, ErrorReason_1[__A_]]]:
        match_value: FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]] = string.Decode(s, json)
        if match_value.tag == 1:
            return FSharpResult_2(1, match_value.fields[0])

        elif match_value.fields[0] == "Raw Data File":
            return FSharpResult_2(0, DataFile(0))

        elif match_value.fields[0] == "Derived Data File":
            return FSharpResult_2(0, DataFile(1))

        elif match_value.fields[0] == "Image File":
            return FSharpResult_2(0, DataFile(2))

        else: 
            s_1: str = match_value.fields[0]
            return FSharpResult_2(1, (("Could not parse " + s_1) + ".", ErrorReason_1(0, s_1, json)))



ROCrate_decoder: Decoder_1[DataFile] = ObjectExpr2366()

ISAJson_encoder: Callable[[DataFile], IEncodable] = ROCrate_encoder

ISAJson_decoder: Decoder_1[DataFile] = ROCrate_decoder

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]


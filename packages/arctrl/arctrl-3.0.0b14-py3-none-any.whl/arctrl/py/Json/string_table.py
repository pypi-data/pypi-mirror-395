from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import (fill, map)
from ..fable_modules.fable_library.map_util import (try_get_value, add_to_dict)
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.seq import iterate
from ..fable_modules.fable_library.types import Array
from ..fable_modules.thoth_json_core.decode import (array as array_2, string, int_1)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ..fable_modules.fable_library.types import FSharpRef

__A_ = TypeVar("__A_")

def array_from_map(otm: Any) -> Array[str]:
    a: Array[str] = fill([0] * len(otm), 0, len(otm), "")
    def action(kv: Any, otm: Any=otm) -> None:
        a[kv[1]] = kv[0]

    iterate(action, otm)
    return a


def encoder(ot: Array[str]) -> IEncodable:
    def _arrow2217(value: str, ot: Any=ot) -> IEncodable:
        class ObjectExpr2216(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2216()

    values: Array[IEncodable] = map(_arrow2217, ot, None)
    class ObjectExpr2218(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], ot: Any=ot) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers_1)

            arg: Array[__A_] = map(mapping, values, None)
            return helpers_1.encode_array(arg)

    return ObjectExpr2218()


decoder: Decoder_1[Array[str]] = array_2(string)

def encode_string(otm: Any, s: str) -> IEncodable:
    match_value: int | None
    pattern_input: tuple[bool, int]
    out_arg: int = None or 0
    def _arrow2219(__unit: None=None, otm: Any=otm, s: Any=s) -> int:
        return out_arg

    def _arrow2220(v: int, otm: Any=otm, s: Any=s) -> None:
        nonlocal out_arg
        out_arg = v or 0

    pattern_input = (try_get_value(otm, s, FSharpRef(_arrow2219, _arrow2220)), out_arg)
    match_value = pattern_input[1] if pattern_input[0] else None
    if match_value is None:
        i_1: int = len(otm) or 0
        add_to_dict(otm, s, i_1)
        class ObjectExpr2221(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], otm: Any=otm, s: Any=s) -> Any:
                return helpers_1.encode_signed_integral_number(i_1)

        return ObjectExpr2221()

    else: 
        i: int = match_value or 0
        class ObjectExpr2222(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], otm: Any=otm, s: Any=s) -> Any:
                return helpers.encode_signed_integral_number(i)

        return ObjectExpr2222()



def decode_string(ot: Array[str]) -> Decoder_1[str]:
    class ObjectExpr2223(Decoder_1[str]):
        def Decode(self, s: IDecoderHelpers_1[Any], json: Any, ot: Any=ot) -> FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]]:
            match_value: FSharpResult_2[int, tuple[str, ErrorReason_1[__A_]]] = int_1.Decode(s, json)
            return FSharpResult_2(1, match_value.fields[0]) if (match_value.tag == 1) else FSharpResult_2(0, ot[match_value.fields[0]])

    return ObjectExpr2223()


__all__ = ["array_from_map", "encoder", "decoder", "encode_string", "decode_string"]


from __future__ import annotations
from collections.abc import Callable
from json import JSONDecodeError
import numbers
import json as json_1
from typing import (Any, TypeVar)
from ..fable_library.result import FSharpResult_2
from ..fable_library.types import (Array, float32)
from ..fable_library.util import IEnumerable_1
from ..thoth_json_core.decode import (Advanced_fromValue, Helpers_prependPath, error_to_string)
from ..thoth_json_core.types import (IDecoderHelpers_1, Decoder_1, ErrorReason_1)

_T = TypeVar("_T")

class ObjectExpr354(IDecoderHelpers_1[Any]):
    def is_string(self, json_value: Any=None) -> bool:
        return str(type(json_value)) == "<class \'str\'>"

    def is_number(self, json_value_1: Any=None) -> bool:
        return (not (isinstance(json_value_1, (bool)))) if (isinstance(json_value_1, numbers.Number)) else False

    def is_boolean(self, json_value_2: Any=None) -> bool:
        return str(type(json_value_2)) == "<class \'bool\'>"

    def is_null_value(self, json_value_3: Any=None) -> bool:
        return json_value_3 is None

    def is_array(self, json_value_4: Any=None) -> bool:
        return isinstance(json_value_4, (list))

    def is_object(self, json_value_5: Any=None) -> bool:
        return isinstance(json_value_5, (dict))

    def has_property(self, field_name: str, json_value_6: Any=None) -> bool:
        return field_name in json_value_6

    def is_integral_value(self, json_value_7: Any=None) -> bool:
        return isinstance(json_value_7, (int))

    def as_string(self, json_value_8: Any=None) -> str:
        return json_value_8

    def as_boolean(self, json_value_9: Any=None) -> bool:
        return json_value_9

    def as_array(self, json_value_10: Any=None) -> Array[Any]:
        return json_value_10

    def as_float(self, json_value_11: Any=None) -> float:
        return json_value_11

    def as_float32(self, json_value_12: Any=None) -> float32:
        return json_value_12

    def as_int(self, json_value_13: Any=None) -> int:
        return json_value_13

    def get_properties(self, json_value_14: Any=None) -> IEnumerable_1[str]:
        return json_value_14.keys()

    def get_property(self, field_name_1: str, json_value_15: Any=None) -> Any:
        return json_value_15[field_name_1]

    def any_to_string(self, json_value_16: Any=None) -> str:
        return json_1.dumps(json_value_16, indent = 4)


Decode_helpers: IDecoderHelpers_1[Any] = ObjectExpr354()

def Decode_fromValue(decoder: Decoder_1[Any]) -> Callable[[Any], FSharpResult_2[_T, str]]:
    def _arrow355(value: Any=None, decoder: Any=decoder) -> FSharpResult_2[_T, str]:
        return Advanced_fromValue(Decode_helpers, decoder, value)

    return _arrow355


def Decode_fromString(decoder: Decoder_1[Any], value: str) -> FSharpResult_2[Any, str]:
    try: 
        json: Any = json_1.loads(value)
        match_value: FSharpResult_2[_T, tuple[str, ErrorReason_1[Any]]] = decoder.Decode(Decode_helpers, json)
        if match_value.tag == 1:
            final_error: tuple[str, ErrorReason_1[Any]]
            tupled_arg: tuple[str, ErrorReason_1[Any]] = match_value.fields[0]
            final_error = Helpers_prependPath("$", tupled_arg[0], tupled_arg[1])
            return FSharpResult_2(1, error_to_string(Decode_helpers, final_error[0], final_error[1]))

        else: 
            return FSharpResult_2(0, match_value.fields[0])


    except Exception as match_value_1:
        if isinstance(match_value_1, JSONDecodeError):
            return FSharpResult_2(1, "Given an invalid JSON: " + str(match_value_1))

        else: 
            raise match_value_1




def Decode_unsafeFromString(decoder: Decoder_1[Any], value: str) -> Any:
    match_value: FSharpResult_2[_T, str] = Decode_fromString(decoder, value)
    if match_value.tag == 1:
        raise Exception(match_value.fields[0])

    else: 
        return match_value.fields[0]



__all__ = ["Decode_helpers", "Decode_fromValue", "Decode_fromString", "Decode_unsafeFromString"]


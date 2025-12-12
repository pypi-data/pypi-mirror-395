from __future__ import annotations
import json as json_2
from typing import Any
from ..fable_library.list import (to_array, FSharpList)
from ..fable_library.seq import to_array as to_array_1
from ..fable_library.types import (Array, uint32)
from ..fable_library.util import (get_enumerator, IEnumerable_1)
from ..thoth_json_core.types import (IEncoderHelpers_1, IEncodable)

class ObjectExpr357(IEncoderHelpers_1[Any]):
    def encode_string(self, value: str) -> Any:
        return value

    def encode_char(self, value_1: str) -> Any:
        return value_1

    def encode_decimal_number(self, value_2: float) -> Any:
        return value_2

    def encode_bool(self, value_3: bool) -> Any:
        return value_3

    def encode_null(self, __unit: None=None) -> Any:
        return None

    def encode_object(self, values: IEnumerable_1[tuple[str, Any]]) -> Any:
        o: Any = {}
        with get_enumerator(values) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                for_loop_var: tuple[str, Any] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                o[for_loop_var[0]] = for_loop_var[1]
        return o

    def encode_array(self, values_1: Array[Any]) -> Any:
        return values_1

    def encode_list(self, values_2: FSharpList[Any]) -> Any:
        this: IEncoderHelpers_1[Any] = self
        arg: Array[Any] = to_array(values_2)
        return this.encode_array(arg)

    def encode_seq(self, values_3: IEnumerable_1[Any]) -> Any:
        this_1: IEncoderHelpers_1[Any] = self
        arg_1: Array[Any] = to_array_1(values_3)
        return this_1.encode_array(arg_1)

    def encode_resize_array(self, values_4: Array[Any]) -> Any:
        this_2: IEncoderHelpers_1[Any] = self
        arg_2: Array[Any] = values_4[:]
        return this_2.encode_array(arg_2)

    def encode_signed_integral_number(self, value_5: int) -> Any:
        return value_5

    def encode_unsigned_integral_number(self, value_6: uint32) -> Any:
        return value_6


helpers: IEncoderHelpers_1[Any] = ObjectExpr357()

def to_string(space: int, value: IEncodable) -> str:
    json_1: Any = value.Encode(helpers)
    if space == 0:
        return json_2.dumps(json_1, separators = [",", ":"], ensure_ascii = False)

    else: 
        return json_2.dumps(json_1, indent = space, ensure_ascii = False)



__all__ = ["helpers", "to_string"]


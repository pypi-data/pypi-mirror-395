from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.date import to_string
from ..fable_modules.fable_library.list import (is_empty as is_empty_1, map as map_3, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (is_empty, map as map_1, append, to_array)
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (to_enumerable, count, IDictionary)
from ..fable_modules.thoth_json_core.encode import (seq, list_1 as list_1_1, tuple2)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Json)

_VALUE = TypeVar("_VALUE")

__A = TypeVar("__A")

__A_ = TypeVar("__A_")

_T = TypeVar("_T")

_KEY = TypeVar("_KEY")

def try_include(name: str, encoder: Callable[[_VALUE], IEncodable], value: Any | None=None) -> tuple[str, IEncodable | None]:
    return (name, map(encoder, value))


def try_include_seq(name: Any, encoder: Callable[[_VALUE], IEncodable], value: Any) -> tuple[__A, IEncodable | None]:
    return (name, None if is_empty(value) else seq(map_1(encoder, value)))


def try_include_array(name: Any, encoder: Callable[[_VALUE], IEncodable], value: Array[Any]) -> tuple[__A, IEncodable | None]:
    def _arrow2128(__unit: None=None, name: Any=name, encoder: Any=encoder, value: Any=value) -> IEncodable:
        values: Array[IEncodable] = map_2(encoder, value, None)
        class ObjectExpr2127(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[__A_]) -> __A_:
                def mapping(v: IEncodable) -> __A_:
                    return v.Encode(helpers)

                arg: Array[__A_] = map_2(mapping, values, None)
                return helpers.encode_array(arg)

        return ObjectExpr2127()

    return (name, None if (len(value) == 0) else _arrow2128())


def try_include_list(name: Any, encoder: Callable[[_VALUE], IEncodable], value: FSharpList[Any]) -> tuple[__A, IEncodable | None]:
    return (name, None if is_empty_1(value) else list_1_1(map_3(encoder, value)))


def try_include_list_opt(name: Any, encoder: Callable[[_VALUE], IEncodable], value: FSharpList[Any] | None=None) -> tuple[__A, IEncodable | None]:
    def _arrow2131(__unit: None=None, name: Any=name, encoder: Any=encoder, value: Any=value) -> IEncodable | None:
        o: FSharpList[_VALUE] = value
        return None if is_empty_1(o) else list_1_1(map_3(encoder, o))

    return (name, _arrow2131() if (value is not None) else None)


DefaultSpaces: int = 0

def default_spaces(spaces: int | None=None) -> int:
    return default_arg(spaces, DefaultSpaces)


def date_time(d: Any) -> IEncodable:
    value: str = to_string(d, "O", {}).split("+")[0]
    class ObjectExpr2135(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], d: Any=d) -> Any:
            return helpers.encode_string(value)

    return ObjectExpr2135()


def add_property_to_object(name: str, value: Json, obj: Json) -> Json:
    if obj.tag == 5:
        return Json(5, append(obj.fields[0], to_enumerable([(name, value)])))

    else: 
        raise Exception("Expected object")



def resize_array_or_singleton(encoder: Callable[[_T], IEncodable], values: Array[Any]) -> IEncodable:
    if len(values) == 1:
        return encoder(values[0])

    else: 
        return seq(map_1(encoder, values))



def dictionary(key_encoder: Callable[[_KEY], IEncodable], value_encoder: Callable[[_VALUE], IEncodable], values: IDictionary[Any, Any]) -> IEncodable:
    if count(values) == 0:
        class ObjectExpr2137(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], key_encoder: Any=key_encoder, value_encoder: Any=value_encoder, values: Any=values) -> Any:
                return helpers.encode_null()

        return ObjectExpr2137()

    else: 
        def mapping(_arg: Any, key_encoder: Any=key_encoder, value_encoder: Any=value_encoder, values: Any=values) -> IEncodable:
            active_pattern_result: tuple[_KEY, _VALUE] = _arg
            return tuple2(key_encoder, value_encoder, active_pattern_result[0], active_pattern_result[1])

        return seq(to_array(map_1(mapping, values)))



def int_dictionary(value_encoder: Callable[[_VALUE], IEncodable], values: IDictionary[int, Any]) -> IEncodable:
    if count(values) == 0:
        class ObjectExpr2139(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], value_encoder: Any=value_encoder, values: Any=values) -> Any:
                return helpers.encode_null()

        return ObjectExpr2139()

    else: 
        def mapping(_arg: Any, value_encoder: Any=value_encoder, values: Any=values) -> IEncodable:
            active_pattern_result: tuple[int, _VALUE] = _arg
            k: int = active_pattern_result[0] or 0
            if True if (k > 2147483647) else (k < -2147483648):
                to_fail(printf("Key %d is out of bounds for Int32"))(k)

            def _arrow2141(value: int, _arg: Any=_arg) -> IEncodable:
                class ObjectExpr2140(IEncodable):
                    def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                        return helpers_1.encode_signed_integral_number(value)

                return ObjectExpr2140()

            return tuple2(_arrow2141, value_encoder, k, active_pattern_result[1])

        return seq(to_array(map_1(mapping, values)))



__all__ = ["try_include", "try_include_seq", "try_include_array", "try_include_list", "try_include_list_opt", "DefaultSpaces", "default_spaces", "date_time", "add_property_to_object", "resize_array_or_singleton", "dictionary", "int_dictionary"]


from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.array_ import map as map_3
from ..fable_library.list import (map as map_1, FSharpList)
from ..fable_library.map import (to_seq, to_list)
from ..fable_library.option import (default_arg_with, map as map_4, value as value_5)
from ..fable_library.seq import map as map_2
from ..fable_library.types import (float32 as float32_1, Array)
from ..fable_library.util import (IEnumerable_1, get_enumerator, dispose, to_enumerable)
from .types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

_T1 = TypeVar("_T1")

_T2 = TypeVar("_T2")

_T3 = TypeVar("_T3")

_T4 = TypeVar("_T4")

_T5 = TypeVar("_T5")

_T6 = TypeVar("_T6")

_T7 = TypeVar("_T7")

_T8 = TypeVar("_T8")

_KEY = TypeVar("_KEY")

_VALUE = TypeVar("_VALUE")

_A = TypeVar("_A")

def float32(value: float32_1) -> IEncodable:
    class ObjectExpr44(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_decimal_number(value)

    return ObjectExpr44()


def list_1(values: FSharpList[IEncodable]) -> IEncodable:
    class ObjectExpr45(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: FSharpList[__A_] = map_1(mapping, values)
            return helpers.encode_list(arg)

    return ObjectExpr45()


def seq(values: IEnumerable_1[IEncodable]) -> IEncodable:
    class ObjectExpr46(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: IEnumerable_1[__A_] = map_2(mapping, values)
            return helpers.encode_seq(arg)

    return ObjectExpr46()


def resize_array(values: Array[IEncodable]) -> IEncodable:
    class ObjectExpr47(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            result: Array[__A_] = []
            enumerator: Any = get_enumerator(values)
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    v: IEncodable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    (result.append(v.Encode(helpers)))

            finally: 
                dispose(enumerator)

            return helpers.encode_resize_array(result)

    return ObjectExpr47()


def dict_1(values: Any) -> IEncodable:
    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_seq(values)
    class ObjectExpr48(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping, values_1)
            return helpers.encode_object(arg)

    return ObjectExpr48()


def tuple2(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], v1: Any, v2: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2)]
    class ObjectExpr49(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, v1: Any=v1, v2: Any=v2) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr49()


def tuple3(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], v1: Any, v2: Any, v3: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3)]
    class ObjectExpr50(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, v1: Any=v1, v2: Any=v2, v3: Any=v3) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr50()


def tuple4(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4)]
    class ObjectExpr51(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr51()


def tuple5(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5)]
    class ObjectExpr52(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr52()


def tuple6(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6)]
    class ObjectExpr53(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr53()


def tuple7(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], enc7: Callable[[_T7], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any, v7: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6), enc7(v7)]
    class ObjectExpr54(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, enc7: Any=enc7, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6, v7: Any=v7) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr54()


def tuple8(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], enc7: Callable[[_T7], IEncodable], enc8: Callable[[_T8], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any, v7: Any, v8: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6), enc7(v7), enc8(v8)]
    class ObjectExpr55(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, enc7: Any=enc7, enc8: Any=enc8, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6, v7: Any=v7, v8: Any=v8) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr55()


def map(key_encoder: Callable[[_KEY], IEncodable], value_encoder: Callable[[_VALUE], IEncodable], values: Any) -> IEncodable:
    def mapping(tupled_arg: tuple[_KEY, _VALUE], key_encoder: Any=key_encoder, value_encoder: Any=value_encoder, values: Any=values) -> IEncodable:
        return tuple2(key_encoder, value_encoder, tupled_arg[0], tupled_arg[1])

    return list_1(map_1(mapping, to_list(values)))


def Enum_byte(value: Any | None=None) -> IEncodable:
    class ObjectExpr56(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr56()


def Enum_sbyte(value: Any | None=None) -> IEncodable:
    class ObjectExpr57(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr57()


def Enum_int16(value: Any | None=None) -> IEncodable:
    class ObjectExpr58(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr58()


def Enum_uint16(value: Any | None=None) -> IEncodable:
    class ObjectExpr59(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr59()


def Enum_int(value: Any | None=None) -> IEncodable:
    class ObjectExpr60(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr60()


def Enum_uint32(value: Any | None=None) -> IEncodable:
    class ObjectExpr61(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr61()


def lossy_option(encoder: Callable[[_A], IEncodable]) -> Callable[[_A | None], IEncodable]:
    def _arrow63(arg: _A | None=None, encoder: Any=encoder) -> IEncodable:
        def def_thunk(__unit: None=None) -> IEncodable:
            class ObjectExpr62(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_null()

            return ObjectExpr62()

        return default_arg_with(map_4(encoder, arg), def_thunk)

    return _arrow63


def lossless_option(encoder: Callable[[_A], IEncodable], value: Any | None=None) -> IEncodable:
    if value is None:
        class ObjectExpr64(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                return helpers_3.encode_string("option")

        class ObjectExpr65(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                return helpers_4.encode_string("none")

        values_1: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("$type", ObjectExpr64()), ("$case", ObjectExpr65())])
        class ObjectExpr66(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

                arg_1: IEnumerable_1[tuple[str, __A_]] = map_2(mapping_1, values_1)
                return helpers_5.encode_object(arg_1)

        return ObjectExpr66()

    else: 
        v: _A = value_5(value)
        class ObjectExpr67(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                return helpers.encode_string("option")

        class ObjectExpr68(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                return helpers_1.encode_string("some")

        values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("$type", ObjectExpr67()), ("$case", ObjectExpr68()), ("$value", encoder(v))])
        class ObjectExpr69(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], encoder: Any=encoder, value: Any=value) -> Any:
                def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg[0], tupled_arg[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr69()



__all__ = ["float32", "list_1", "seq", "resize_array", "dict_1", "tuple2", "tuple3", "tuple4", "tuple5", "tuple6", "tuple7", "tuple8", "map", "Enum_byte", "Enum_sbyte", "Enum_int16", "Enum_uint16", "Enum_int", "Enum_uint32", "lossy_option", "lossless_option"]


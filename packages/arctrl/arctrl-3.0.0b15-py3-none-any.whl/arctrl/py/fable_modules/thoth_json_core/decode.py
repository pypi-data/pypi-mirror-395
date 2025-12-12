from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from decimal import Decimal
from typing import (Any, Protocol, Generic, TypeVar)
from ..fable_library.array_ import (fold as fold_1, fill)
from ..fable_library.big_int import (from_int32, try_parse as try_parse_4)
from ..fable_library.date import (min_value, try_parse as try_parse_6)
from ..fable_library.decimal_ import (Decimal as Decimal_1, try_parse as try_parse_5)
from ..fable_library.guid import try_parse as try_parse_1
from ..fable_library.int32 import try_parse as try_parse_2
from ..fable_library.list import (map as map_1, try_last, FSharpList, fold, empty, append, singleton, of_seq, reverse as reverse_1, cons, is_empty, head as head_1, tail as tail_1, length)
from ..fable_library.long import (to_number, from_number, try_parse as try_parse_3)
from ..fable_library.map import (of_list, of_seq as of_seq_1)
from ..fable_library.option import (some, default_arg, value as value_7)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.result import (FSharpResult_2, Result_MapError, Result_Map)
from ..fable_library.seq import (reverse, append as append_1, to_list)
from ..fable_library.string_ import join
from ..fable_library.time_span import (create, try_parse as try_parse_7)
from ..fable_library.types import (FSharpRef, int8, uint8, int16 as int16_1, uint16 as uint16_1, uint32 as uint32_1, int64 as int64_1, uint64 as uint64_1, float32 as float32_1, Array)
from ..fable_library.util import (int32_to_string, IEnumerable_1, to_enumerable, compare_primitives, compare)
from .types import (ErrorReason_1, IDecoderHelpers_1, Decoder_1)

_JSONVALUE = TypeVar("_JSONVALUE")

_T = TypeVar("_T")

__A_ = TypeVar("__A_")

_VALUE = TypeVar("_VALUE")

_VALUE_ = TypeVar("_VALUE_")

__A = TypeVar("__A")

_OUTPUT_ = TypeVar("_OUTPUT_")

_A_ = TypeVar("_A_")

__C_ = TypeVar("__C_")

_B_ = TypeVar("_B_")

_A = TypeVar("_A")

_B = TypeVar("_B")

_OUTPUT = TypeVar("_OUTPUT")

__B_ = TypeVar("__B_")

__D_ = TypeVar("__D_")

_C_ = TypeVar("_C_")

_C = TypeVar("_C")

__E_ = TypeVar("__E_")

_D_ = TypeVar("_D_")

_D = TypeVar("_D")

__F_ = TypeVar("__F_")

_E_ = TypeVar("_E_")

_E = TypeVar("_E")

__G_ = TypeVar("__G_")

_F_ = TypeVar("_F_")

_F = TypeVar("_F")

__H_ = TypeVar("__H_")

_G_ = TypeVar("_G_")

_G = TypeVar("_G")

__I_ = TypeVar("__I_")

_H_ = TypeVar("_H_")

_H = TypeVar("_H")

_JSONVALUE_ = TypeVar("_JSONVALUE_")

_T2 = TypeVar("_T2")

_T1 = TypeVar("_T1")

_T3 = TypeVar("_T3")

_T4 = TypeVar("_T4")

_T5 = TypeVar("_T5")

_T6 = TypeVar("_T6")

_T7 = TypeVar("_T7")

_T8 = TypeVar("_T8")

_KEY_ = TypeVar("_KEY_")

_KEY = TypeVar("_KEY")

def Helpers_prependPath(path: str, err_: str, err__1: ErrorReason_1[Any]) -> tuple[str, ErrorReason_1[_JSONVALUE]]:
    err: tuple[str, ErrorReason_1[_JSONVALUE]] = (err_, err__1)
    return (path + err[0], err[1])


def generic_msg(helpers: IDecoderHelpers_1[Any], msg: str, value_1: Any, new_line: bool) -> str:
    try: 
        return ((("Expecting " + msg) + " but instead got:") + ("\n" if new_line else " ")) + helpers.any_to_string(value_1)

    except Exception as match_value:
        return (("Expecting " + msg) + " but decoder failed. Couldn\'t report given value due to circular structure.") + ("\n" if new_line else " ")



def error_to_string(helpers: IDecoderHelpers_1[Any], path: str, error: ErrorReason_1[Any]) -> str:
    def mapping(error_1: tuple[str, ErrorReason_1[_JSONVALUE]], helpers: Any=helpers, path: Any=path, error: Any=error) -> str:
        tupled_arg: tuple[str, ErrorReason_1[_JSONVALUE]] = Helpers_prependPath(path, error_1[0], error_1[1])
        return error_to_string(helpers, tupled_arg[0], tupled_arg[1])

    reason_1: str = generic_msg(helpers, error.fields[0], error.fields[1], True) if (error.tag == 2) else (((generic_msg(helpers, error.fields[0], error.fields[1], False) + "\nReason: ") + error.fields[2]) if (error.tag == 1) else (generic_msg(helpers, error.fields[0], error.fields[1], True) if (error.tag == 3) else ((generic_msg(helpers, error.fields[0], error.fields[1], True) + (("\nNode `" + error.fields[2]) + "` is unkown.")) if (error.tag == 4) else (((("Expecting " + error.fields[0]) + ".\n") + helpers.any_to_string(error.fields[1])) if (error.tag == 5) else (("The following errors were found:\n\n" + join("\n\n", map_1(mapping, error.fields[0]))) if (error.tag == 7) else (("The following `failure` occurred with the decoder: " + error.fields[0]) if (error.tag == 6) else generic_msg(helpers, error.fields[0], error.fields[1], False)))))))
    if error.tag == 7:
        return reason_1

    else: 
        return (("Error at: `" + path) + "`\n") + reason_1



def Advanced_fromValue(helpers: IDecoderHelpers_1[Any], decoder: Decoder_1[Any], value_1: Any) -> FSharpResult_2[Any, str]:
    match_value: FSharpResult_2[_T, tuple[str, ErrorReason_1[_JSONVALUE]]] = decoder.Decode(helpers, value_1)
    if match_value.tag == 1:
        error: tuple[str, ErrorReason_1[_JSONVALUE]] = match_value.fields[0]
        return FSharpResult_2(1, error_to_string(helpers, error[0], error[1]))

    else: 
        return FSharpResult_2(0, match_value.fields[0])



class ObjectExpr77(Decoder_1[str]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, helpers.as_string(value_1)) if helpers.is_string(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "a string", value_1)))


string: Decoder_1[str] = ObjectExpr77()

class ObjectExpr78(Decoder_1[str]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_string(value_1):
            str_1: str = helpers.as_string(value_1)
            return FSharpResult_2(0, str_1[0]) if (len(str_1) == 1) else FSharpResult_2(1, ("", ErrorReason_1(0, "a single character string", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a char", value_1)))



char: Decoder_1[str] = ObjectExpr78()

class ObjectExpr81(Decoder_1[str]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_string(value_1):
            match_value: tuple[bool, str]
            out_arg: str = "00000000-0000-0000-0000-000000000000"
            def _arrow79(__unit: None=None) -> str:
                return out_arg

            def _arrow80(v: str) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_1(helpers.as_string(value_1), FSharpRef(_arrow79, _arrow80)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a guid", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a guid", value_1)))



guid: Decoder_1[str] = ObjectExpr81()

class ObjectExpr82(Decoder_1[None]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[None, tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, None) if helpers.is_null_value(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "null", value_1)))


unit: Decoder_1[None] = ObjectExpr82()

class ObjectExpr85(Decoder_1[int8]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[int8, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, (int(float_value) + 0x80 & 0xFF) - 0x80) if ((float_value <= int8(127)) if (int8(-128) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "a sbyte", value_2, "Value was either too large or too small for a sbyte")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "a sbyte", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, int8]
            out_arg: int8 = int8(0) or 0
            def _arrow83(__unit: None=None) -> int8:
                return out_arg

            def _arrow84(v: int8) -> None:
                nonlocal out_arg
                out_arg = v or 0

            match_value = (try_parse_2(helpers.as_string(value_2), 511, False, 8, FSharpRef(_arrow83, _arrow84)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a sbyte", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a sbyte", value_2)))



sbyte: Decoder_1[int8] = ObjectExpr85()

class ObjectExpr88(Decoder_1[uint8]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[uint8, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, int(float_value+0x100 if float_value < 0 else float_value) & 0xFF) if ((float_value <= uint8(255)) if (uint8(0) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "a byte", value_2, "Value was either too large or too small for a byte")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "a byte", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, uint8]
            out_arg: uint8 = uint8(0)
            def _arrow86(__unit: None=None) -> uint8:
                return out_arg

            def _arrow87(v: uint8) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_2(helpers.as_string(value_2), 511, True, 8, FSharpRef(_arrow86, _arrow87)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a byte", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a byte", value_2)))



byte: Decoder_1[uint8] = ObjectExpr88()

class ObjectExpr91(Decoder_1[int16_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[int16_1, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, (int(float_value) + 0x8000 & 0xFFFF) - 0x8000) if ((float_value <= int16_1(32767)) if (int16_1(-32768) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an int16", value_2, "Value was either too large or too small for an int16")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an int16", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, int16_1]
            out_arg: int16_1 = int16_1(0) or 0
            def _arrow89(__unit: None=None) -> int16_1:
                return out_arg

            def _arrow90(v: int16_1) -> None:
                nonlocal out_arg
                out_arg = v or 0

            match_value = (try_parse_2(helpers.as_string(value_2), 511, False, 16, FSharpRef(_arrow89, _arrow90)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an int16", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an int16", value_2)))



int16: Decoder_1[int16_1] = ObjectExpr91()

class ObjectExpr94(Decoder_1[uint16_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[uint16_1, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, int(float_value+0x10000 if float_value < 0 else float_value) & 0xFFFF) if ((float_value <= uint16_1(65535)) if (uint16_1(0) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an uint16", value_2, "Value was either too large or too small for an uint16")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an uint16", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, uint16_1]
            out_arg: uint16_1 = uint16_1(0)
            def _arrow92(__unit: None=None) -> uint16_1:
                return out_arg

            def _arrow93(v: uint16_1) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_2(helpers.as_string(value_2), 511, True, 16, FSharpRef(_arrow92, _arrow93)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an uint16", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an uint16", value_2)))



uint16: Decoder_1[uint16_1] = ObjectExpr94()

class ObjectExpr97(Decoder_1[int]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[int, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, int(float_value)) if ((float_value <= 2147483647) if (-2147483648 <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an int", value_2, "Value was either too large or too small for an int")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an int", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, int]
            out_arg: int = 0
            def _arrow95(__unit: None=None) -> int:
                return out_arg

            def _arrow96(v: int) -> None:
                nonlocal out_arg
                out_arg = v or 0

            match_value = (try_parse_2(helpers.as_string(value_2), 511, False, 32, FSharpRef(_arrow95, _arrow96)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an int", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an int", value_2)))



int_1: Decoder_1[int] = ObjectExpr97()

class ObjectExpr100(Decoder_1[uint32_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[uint32_1, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, int(float_value+0x100000000 if float_value < 0 else float_value)) if ((float_value <= uint32_1(4294967295)) if (uint32_1(0) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an uint32", value_2, "Value was either too large or too small for an uint32")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an uint32", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, uint32_1]
            out_arg: uint32_1 = uint32_1(0)
            def _arrow98(__unit: None=None) -> uint32_1:
                return out_arg

            def _arrow99(v: uint32_1) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_2(helpers.as_string(value_2), 511, True, 32, FSharpRef(_arrow98, _arrow99)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an uint32", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an uint32", value_2)))



uint32: Decoder_1[uint32_1] = ObjectExpr100()

class ObjectExpr103(Decoder_1[int64_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[int64_1, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, from_number(float_value, False)) if ((float_value <= to_number(int64_1(9223372036854775807))) if (to_number(int64_1(-9223372036854775808)) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an int64", value_2, "Value was either too large or too small for an int64")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an int64", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, int64_1]
            out_arg: int64_1 = int64_1(0)
            def _arrow101(__unit: None=None) -> int64_1:
                return out_arg

            def _arrow102(v: int64_1) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_3(helpers.as_string(value_2), 511, False, 64, FSharpRef(_arrow101, _arrow102)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an int64", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an int64", value_2)))



int64: Decoder_1[int64_1] = ObjectExpr103()

class ObjectExpr106(Decoder_1[uint64_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_2: Any) -> FSharpResult_2[uint64_1, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_2):
            if helpers.is_integral_value(value_2):
                float_value: float = helpers.as_float(value_2)
                return FSharpResult_2(0, from_number(float_value, True)) if ((float_value <= to_number(uint64_1(18446744073709551615))) if (to_number(uint64_1(0)) <= float_value) else False) else FSharpResult_2(1, ("", ErrorReason_1(1, "an uint64", value_2, "Value was either too large or too small for an uint64")))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(1, "an uint64", value_2, "Value is not an integral value")))


        elif helpers.is_string(value_2):
            match_value: tuple[bool, uint64_1]
            out_arg: uint64_1 = uint64_1(0)
            def _arrow104(__unit: None=None) -> uint64_1:
                return out_arg

            def _arrow105(v: uint64_1) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_3(helpers.as_string(value_2), 511, True, 64, FSharpRef(_arrow104, _arrow105)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "an uint64", value_2)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "an uint64", value_2)))



uint64: Decoder_1[uint64_1] = ObjectExpr106()

class ObjectExpr109(Decoder_1[int]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[int, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_1):
            return FSharpResult_2(0, from_int32(helpers.as_int(value_1)))

        elif helpers.is_string(value_1):
            parse_result: tuple[bool, int]
            out_arg: int = from_int32(0)
            def _arrow107(__unit: None=None) -> int:
                return out_arg

            def _arrow108(v: int) -> None:
                nonlocal out_arg
                out_arg = v

            parse_result = (try_parse_4(helpers.as_string(value_1), FSharpRef(_arrow107, _arrow108)), out_arg)
            return FSharpResult_2(0, parse_result[1]) if parse_result[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a bigint", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a bigint", value_1)))



bigint: Decoder_1[int] = ObjectExpr109()

class ObjectExpr110(Decoder_1[bool]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[bool, tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, helpers.as_boolean(value_1)) if helpers.is_boolean(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "a boolean", value_1)))


bool_1: Decoder_1[bool] = ObjectExpr110()

class ObjectExpr111(Decoder_1[float]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[float, tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, helpers.as_float(value_1)) if helpers.is_number(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "a float", value_1)))


float_1: Decoder_1[float] = ObjectExpr111()

class ObjectExpr112(Decoder_1[float32_1]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[float32_1, tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, helpers.as_float32(value_1)) if helpers.is_number(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "a float32", value_1)))


float32: Decoder_1[float32_1] = ObjectExpr112()

class ObjectExpr115(Decoder_1[Decimal]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[Decimal, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_number(value_1):
            return FSharpResult_2(0, Decimal_1(helpers.as_float(value_1)))

        elif helpers.is_string(value_1):
            match_value: tuple[bool, Decimal]
            out_arg: Decimal = Decimal_1(0)
            def _arrow113(__unit: None=None) -> Decimal:
                return out_arg

            def _arrow114(v: Decimal) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_5(helpers.as_string(value_1), FSharpRef(_arrow113, _arrow114)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a decimal", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a decimal", value_1)))



decimal: Decoder_1[Decimal] = ObjectExpr115()

class ObjectExpr118(Decoder_1[Any]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_string(value_1):
            match_value: tuple[bool, Any]
            out_arg: Any = min_value()
            def _arrow116(__unit: None=None) -> Any:
                return out_arg

            def _arrow117(v: Any) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_6(helpers.as_string(value_1), FSharpRef(_arrow116, _arrow117)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a datetime", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a datetime", value_1)))



datetime_local: Decoder_1[Any] = ObjectExpr118()

class ObjectExpr121(Decoder_1[Any]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
        if helpers.is_string(value_1):
            match_value: tuple[bool, Any]
            out_arg: Any = create(0)
            def _arrow119(__unit: None=None) -> Any:
                return out_arg

            def _arrow120(v: Any) -> None:
                nonlocal out_arg
                out_arg = v

            match_value = (try_parse_7(helpers.as_string(value_1), FSharpRef(_arrow119, _arrow120)), out_arg)
            return FSharpResult_2(0, match_value[1]) if match_value[0] else FSharpResult_2(1, ("", ErrorReason_1(0, "a timespan", value_1)))

        else: 
            return FSharpResult_2(1, ("", ErrorReason_1(0, "a timespan", value_1)))



timespan: Decoder_1[Any] = ObjectExpr121()

def decode_maybe_null(helpers: IDecoderHelpers_1[Any], path: str, decoder: Decoder_1[Any], value_1: Any) -> FSharpResult_2[Any | None, tuple[str, ErrorReason_1[_JSONVALUE]]]:
    if helpers.is_null_value(value_1):
        return FSharpResult_2(0, None)

    else: 
        match_value: FSharpResult_2[_VALUE, tuple[str, ErrorReason_1[_JSONVALUE]]] = decoder.Decode(helpers, value_1)
        if match_value.tag == 1:
            def _arrow122(__unit: None=None, helpers: Any=helpers, path: Any=path, decoder: Any=decoder, value_1: Any=value_1) -> tuple[str, ErrorReason_1[_JSONVALUE]]:
                tupled_arg: tuple[str, ErrorReason_1[_JSONVALUE]] = match_value.fields[0]
                return Helpers_prependPath(path, tupled_arg[0], tupled_arg[1])

            return FSharpResult_2(1, _arrow122())

        else: 
            return FSharpResult_2(0, some(match_value.fields[0]))




def optional(field_name: str, decoder: Decoder_1[Any]) -> Decoder_1[Any | None]:
    class ObjectExpr123(Decoder_1[_VALUE_ | None]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, field_name: Any=field_name, decoder: Any=decoder) -> FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]]:
            return (decode_maybe_null(helpers, "." + field_name, decoder, helpers.get_property(field_name, value_1)) if helpers.has_property(field_name, value_1) else FSharpResult_2(0, None)) if helpers.is_object(value_1) else FSharpResult_2(1, ("", ErrorReason_1(2, "an object", value_1)))

    return ObjectExpr123()


def bad_path_error(field_names: FSharpList[str], current_path: str | None, value_1: Any) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A]]]:
    return FSharpResult_2(1, ("." + default_arg(current_path, join(".", field_names)), ErrorReason_1(4, ("an object with path `" + join(".", field_names)) + "`", value_1, default_arg(try_last(field_names), ""))))


def map2(ctor: Callable[[_A, _B], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr124(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__C_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__C_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__C_]]] = d2.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__C_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__C_]]] = match_value_1
                return FSharpResult_2(1, copy_of_struct_1.fields[0]) if (copy_of_struct_1.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0]))


    return ObjectExpr124()


def optional_at(field_names: FSharpList[str], decoder: Decoder_1[Any]) -> Decoder_1[Any | None]:
    class ObjectExpr125(Decoder_1[_VALUE_ | None]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], first_value: Any, field_names: Any=field_names, decoder: Any=decoder) -> FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]]:
            def folder(tupled_arg: tuple[str, __A_, FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]] | None], field_1: str) -> tuple[str, __A_, FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]] | None]:
                cur_path: str = tupled_arg[0]
                cur_value: __A_ = tupled_arg[1]
                res: FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]] | None = tupled_arg[2]
                if res is None:
                    if helpers.is_null_value(cur_value):
                        return (cur_path, cur_value, FSharpResult_2(0, None))

                    elif helpers.is_object(cur_value):
                        if helpers.has_property(field_1, cur_value):
                            return ((cur_path + ".") + field_1, helpers.get_property(field_1, cur_value), None)

                        else: 
                            return (cur_path, cur_value, FSharpResult_2(0, None))


                    else: 
                        return (cur_path, cur_value, FSharpResult_2(1, (cur_path, ErrorReason_1(2, "an object", cur_value))))


                else: 
                    return (cur_path, cur_value, res)


            _arg: tuple[str, __A_, FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]] | None] = fold(folder, ("", first_value, None), field_names)
            if _arg[2] is None:
                last_value: __A_ = _arg[1]
                return FSharpResult_2(0, None) if helpers.is_null_value(last_value) else decode_maybe_null(helpers, _arg[0], decoder, last_value)

            else: 
                return _arg[2]


    return ObjectExpr125()


def field(field_name: str, decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr126(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, field_name: Any=field_name, decoder: Any=decoder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_object(value_1):
                if helpers.has_property(field_name, value_1):
                    field_value: __A_ = helpers.get_property(field_name, value_1)
                    path: str = "." + field_name
                    def mapping(tupled_arg: tuple[str, ErrorReason_1[__A_]]) -> tuple[str, ErrorReason_1[__A_]]:
                        return Helpers_prependPath(path, tupled_arg[0], tupled_arg[1])

                    return Result_MapError(mapping, decoder.Decode(helpers, field_value))

                else: 
                    return FSharpResult_2(1, ("", ErrorReason_1(3, ("an object with a field named `" + field_name) + "`", value_1)))


            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(2, "an object", value_1)))


    return ObjectExpr126()


def at(field_names: FSharpList[str], decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr127(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], first_value: Any, field_names: Any=field_names, decoder: Any=decoder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            def folder(tupled_arg: tuple[str, __A_, FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] | None], field_1: str) -> tuple[str, __A_, FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] | None]:
                cur_path: str = tupled_arg[0]
                cur_value: __A_ = tupled_arg[1]
                res: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] | None = tupled_arg[2]
                if res is None:
                    if helpers.is_null_value(cur_value):
                        return (cur_path, cur_value, bad_path_error(field_names, cur_path, first_value))

                    elif helpers.is_object(cur_value):
                        if helpers.has_property(field_1, cur_value):
                            return ((cur_path + ".") + field_1, helpers.get_property(field_1, cur_value), None)

                        else: 
                            return (cur_path, cur_value, bad_path_error(field_names, None, first_value))


                    else: 
                        return (cur_path, cur_value, FSharpResult_2(1, (cur_path, ErrorReason_1(2, "an object", cur_value))))


                else: 
                    return (cur_path, cur_value, res)


            _arg: tuple[str, __A_, FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] | None] = fold(folder, ("", first_value, None), field_names)
            def mapping(tupled_arg_1: tuple[str, ErrorReason_1[__A_]]) -> tuple[str, ErrorReason_1[__A_]]:
                return Helpers_prependPath(_arg[0], tupled_arg_1[0], tupled_arg_1[1])

            return Result_MapError(mapping, decoder.Decode(helpers, _arg[1])) if (_arg[2] is None) else _arg[2]

    return ObjectExpr127()


def index(requested_index: int, decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr128(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, requested_index: Any=requested_index, decoder: Any=decoder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value_1):
                v_array: Array[__A_] = helpers.as_array(value_1)
                path: str = (".[" + int32_to_string(requested_index)) + "]"
                def mapping(tupled_arg: tuple[str, ErrorReason_1[__A_]]) -> tuple[str, ErrorReason_1[__A_]]:
                    return Helpers_prependPath(path, tupled_arg[0], tupled_arg[1])

                return Result_MapError(mapping, decoder.Decode(helpers, v_array[requested_index])) if (requested_index < len(v_array)) else FSharpResult_2(1, (path, ErrorReason_1(5, ((("a longer array. Need index `" + int32_to_string(requested_index)) + "` but there are only `") + int32_to_string(len(v_array))) + "` entries", value_1)))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value_1)))


    return ObjectExpr128()


def list_1(decoder: Decoder_1[Any]) -> Decoder_1[FSharpList[Any]]:
    class ObjectExpr130(Decoder_1[FSharpList[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[FSharpList[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value_1):
                tokens: Array[__A_] = helpers.as_array(value_1)
                i: int = 0
                result: FSharpList[_VALUE_] = empty()
                error: tuple[str, ErrorReason_1[__A_]] | None = None
                while (error is None) if (i < len(tokens)) else False:
                    value_2: __A_ = tokens[i]
                    match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_2)
                    if match_value.tag == 1:
                        def _arrow129(__unit: None=None) -> tuple[str, ErrorReason_1[__A_]]:
                            tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                            return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                        x: tuple[str, ErrorReason_1[__A_]] | None = _arrow129()
                        error = x

                    else: 
                        result = append(result, singleton(match_value.fields[0]))

                    i = (i + 1) or 0
                return FSharpResult_2(0, result) if (error is None) else FSharpResult_2(1, value_7(error))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "a list", value_1)))


    return ObjectExpr130()


def resize_array(decoder: Decoder_1[Any]) -> Decoder_1[Array[Any]]:
    class ObjectExpr132(Decoder_1[Array[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value_1):
                tokens: Array[__A_] = helpers.as_array(value_1)
                i: int = 0
                result: Array[_VALUE_] = []
                error: tuple[str, ErrorReason_1[__A_]] | None = None
                while (error is None) if (i < len(tokens)) else False:
                    value_2: __A_ = tokens[i]
                    match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_2)
                    if match_value.tag == 1:
                        def _arrow131(__unit: None=None) -> tuple[str, ErrorReason_1[__A_]]:
                            tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                            return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                        error = _arrow131()

                    else: 
                        (result.append(match_value.fields[0]))

                    i = (i + 1) or 0
                return FSharpResult_2(0, list(result)) if (error is None) else FSharpResult_2(1, value_7(error))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "a ResizeArray", value_1)))


    return ObjectExpr132()


def seq(decoder: Decoder_1[Any]) -> Decoder_1[IEnumerable_1[Any]]:
    class ObjectExpr134(Decoder_1[IEnumerable_1[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[IEnumerable_1[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value_1):
                i: int = -1
                def folder(acc: FSharpResult_2[IEnumerable_1[_VALUE_], tuple[str, ErrorReason_1[__A_]]], value_2: __A_) -> FSharpResult_2[IEnumerable_1[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
                    nonlocal i
                    i = (i + 1) or 0
                    if acc.tag == 0:
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_2)
                        if match_value.tag == 0:
                            return FSharpResult_2(0, append_1(to_enumerable([match_value.fields[0]]), acc.fields[0]))

                        else: 
                            def _arrow133(__unit: None=None, acc: Any=acc, value_2: Any=value_2) -> tuple[str, ErrorReason_1[__A_]]:
                                tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                                return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                            return FSharpResult_2(1, _arrow133())


                    else: 
                        return acc


                return Result_Map(reverse, fold_1(folder, FSharpResult_2(0, to_enumerable([])), helpers.as_array(value_1)))

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "a seq", value_1)))


    return ObjectExpr134()


def array(decoder: Decoder_1[Any]) -> Decoder_1[Array[Any]]:
    class ObjectExpr136(Decoder_1[Array[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value_1):
                i: int = -1
                tokens: Array[__A_] = helpers.as_array(value_1)
                def folder(acc: FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]], value_2: __A_) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
                    nonlocal i
                    i = (i + 1) or 0
                    if acc.tag == 0:
                        acc_1: Array[_VALUE_] = acc.fields[0]
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_2)
                        if match_value.tag == 0:
                            acc_1[i] = match_value.fields[0]
                            return FSharpResult_2(0, acc_1)

                        else: 
                            def _arrow135(__unit: None=None, acc: Any=acc, value_2: Any=value_2) -> tuple[str, ErrorReason_1[__A_]]:
                                tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                                return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                            return FSharpResult_2(1, _arrow135())


                    else: 
                        return acc


                return fold_1(folder, FSharpResult_2(0, fill([0] * len(tokens), 0, len(tokens), None)), tokens)

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value_1)))


    return ObjectExpr136()


class ObjectExpr137(Decoder_1[FSharpList[str]]):
    def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> FSharpResult_2[FSharpList[str], tuple[str, ErrorReason_1[__A_]]]:
        return FSharpResult_2(0, of_seq(helpers.get_properties(value_1))) if helpers.is_object(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value_1)))


keys: Decoder_1[FSharpList[str]] = ObjectExpr137()

def key_value_pairs(decoder: Decoder_1[Any]) -> Decoder_1[FSharpList[tuple[str, _VALUE]]]:
    class ObjectExpr138(Decoder_1[FSharpList[tuple[str, _VALUE_]]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[FSharpList[tuple[str, _VALUE_]], tuple[str, ErrorReason_1[__A_]]]:
            match_value: FSharpResult_2[FSharpList[str], tuple[str, ErrorReason_1[__A_]]] = keys.Decode(helpers, value_1)
            def folder(acc: FSharpResult_2[FSharpList[tuple[str, _VALUE_]], tuple[str, ErrorReason_1[__A_]]], prop: str) -> FSharpResult_2[FSharpList[tuple[str, _VALUE_]], tuple[str, ErrorReason_1[__A_]]]:
                if acc.tag == 0:
                    field_value: __A_ = helpers.get_property(prop, value_1)
                    match_value_1: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, field_value)
                    if match_value_1.tag == 0:
                        return FSharpResult_2(0, cons((prop, match_value_1.fields[0]), acc.fields[0]))

                    else: 
                        return FSharpResult_2(1, match_value_1.fields[0])


                else: 
                    return acc


            return FSharpResult_2(1, match_value.fields[0]) if (match_value.tag == 1) else Result_Map(reverse_1, fold(folder, FSharpResult_2(0, empty()), match_value.fields[0]))

    return ObjectExpr138()


def one_of(decoders: FSharpList[Decoder_1[Any]]) -> Decoder_1[Any]:
    class ObjectExpr139(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoders: Any=decoders) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            def runner(decoders_1_mut: FSharpList[Decoder_1[_VALUE_]], errors_mut: FSharpList[tuple[str, ErrorReason_1[__A_]]]) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
                while True:
                    (decoders_1, errors) = (decoders_1_mut, errors_mut)
                    if is_empty(decoders_1):
                        return FSharpResult_2(1, ("", ErrorReason_1(7, errors)))

                    else: 
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = head_1(decoders_1).Decode(helpers, value_1)
                        if match_value.tag == 1:
                            decoders_1_mut = tail_1(decoders_1)
                            errors_mut = append(errors, singleton(match_value.fields[0]))
                            continue

                        else: 
                            return FSharpResult_2(0, match_value.fields[0])


                    break

            return runner(decoders, empty())

    return ObjectExpr139()


def nil(output: Any | None=None) -> Decoder_1[Any]:
    class ObjectExpr140(Decoder_1[_A_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, output: Any=output) -> FSharpResult_2[_A_, tuple[str, ErrorReason_1[__B_]]]:
            return FSharpResult_2(0, output) if helpers.is_null_value(value_1) else FSharpResult_2(1, ("", ErrorReason_1(0, "null", value_1)))

    return ObjectExpr140()


def value(_arg: Any, v: Any) -> FSharpResult_2[Any, Any]:
    return FSharpResult_2(0, v)


def succeed(output: Any | None=None) -> Decoder_1[Any]:
    class ObjectExpr141(Decoder_1[_A_]):
        def Decode(self, _arg: IDecoderHelpers_1[Any], _arg_1: Any, output: Any=output) -> FSharpResult_2[_A_, tuple[str, ErrorReason_1[__B_]]]:
            return FSharpResult_2(0, output)

    return ObjectExpr141()


def fail(msg: str) -> Decoder_1[Any]:
    class ObjectExpr142(Decoder_1[_A_]):
        def Decode(self, _arg: IDecoderHelpers_1[Any], _arg_1: Any, msg: Any=msg) -> FSharpResult_2[_A_, tuple[str, ErrorReason_1[__B_]]]:
            return FSharpResult_2(1, ("", ErrorReason_1(6, msg)))

    return ObjectExpr142()


def and_then(cb: Callable[[_A], Decoder_1[_B]], decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr143(Decoder_1[_B_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, cb: Any=cb, decoder: Any=decoder) -> FSharpResult_2[_B_, tuple[str, ErrorReason_1[__C_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__C_]]] = decoder.Decode(helpers, value_1)
            return cb(match_value.fields[0]).Decode(helpers, value_1) if (match_value.tag == 0) else FSharpResult_2(1, match_value.fields[0])

    return ObjectExpr143()


def all(decoders: FSharpList[Decoder_1[Any]]) -> Decoder_1[FSharpList[Any]]:
    class ObjectExpr144(Decoder_1[FSharpList[_A_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoders: Any=decoders) -> FSharpResult_2[FSharpList[_A_], tuple[str, ErrorReason_1[__B_]]]:
            def runner(decoders_1_mut: FSharpList[Decoder_1[_A_]], values_mut: FSharpList[_A_]) -> FSharpResult_2[FSharpList[_A_], tuple[str, ErrorReason_1[__B_]]]:
                while True:
                    (decoders_1, values) = (decoders_1_mut, values_mut)
                    if is_empty(decoders_1):
                        return FSharpResult_2(0, values)

                    else: 
                        match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__B_]]] = head_1(decoders_1).Decode(helpers, value_1)
                        if match_value.tag == 1:
                            return FSharpResult_2(1, match_value.fields[0])

                        else: 
                            decoders_1_mut = tail_1(decoders_1)
                            values_mut = append(values, singleton(match_value.fields[0]))
                            continue


                    break

            return runner(decoders, empty())

    return ObjectExpr144()


def map(ctor: Callable[[_A], _OUTPUT], d1: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr145(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__B_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__B_]]] = d1.Decode(helpers, value_1)
            return FSharpResult_2(1, match_value.fields[0]) if (match_value.tag == 1) else FSharpResult_2(0, ctor(match_value.fields[0]))

    return ObjectExpr145()


def map3(ctor: Callable[[_A, _B, _C], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr146(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__D_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__D_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__D_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__D_]]] = d3.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__D_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__D_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__D_]]] = match_value_2
                    return FSharpResult_2(1, copy_of_struct_2.fields[0]) if (copy_of_struct_2.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0]))



    return ObjectExpr146()


def map4(ctor: Callable[[_A, _B, _C, _D], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any], d4: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr147(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3, d4: Any=d4) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__E_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__E_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__E_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__E_]]] = d3.Decode(helpers, value_1)
            match_value_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__E_]]] = d4.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__E_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__E_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__E_]]] = match_value_2
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, copy_of_struct_2.fields[0])

                    else: 
                        copy_of_struct_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__E_]]] = match_value_3
                        return FSharpResult_2(1, copy_of_struct_3.fields[0]) if (copy_of_struct_3.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0], copy_of_struct_3.fields[0]))




    return ObjectExpr147()


def map5(ctor: Callable[[_A, _B, _C, _D, _E], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any], d4: Decoder_1[Any], d5: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr148(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3, d4: Any=d4, d5: Any=d5) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__F_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__F_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__F_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__F_]]] = d3.Decode(helpers, value_1)
            match_value_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__F_]]] = d4.Decode(helpers, value_1)
            match_value_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__F_]]] = d5.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__F_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__F_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__F_]]] = match_value_2
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, copy_of_struct_2.fields[0])

                    else: 
                        copy_of_struct_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__F_]]] = match_value_3
                        if copy_of_struct_3.tag == 1:
                            return FSharpResult_2(1, copy_of_struct_3.fields[0])

                        else: 
                            copy_of_struct_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__F_]]] = match_value_4
                            return FSharpResult_2(1, copy_of_struct_4.fields[0]) if (copy_of_struct_4.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0], copy_of_struct_3.fields[0], copy_of_struct_4.fields[0]))





    return ObjectExpr148()


def map6(ctor: Callable[[_A, _B, _C, _D, _E, _F], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any], d4: Decoder_1[Any], d5: Decoder_1[Any], d6: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr149(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3, d4: Any=d4, d5: Any=d5, d6: Any=d6) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__G_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__G_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__G_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__G_]]] = d3.Decode(helpers, value_1)
            match_value_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__G_]]] = d4.Decode(helpers, value_1)
            match_value_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__G_]]] = d5.Decode(helpers, value_1)
            match_value_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__G_]]] = d6.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__G_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__G_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__G_]]] = match_value_2
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, copy_of_struct_2.fields[0])

                    else: 
                        copy_of_struct_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__G_]]] = match_value_3
                        if copy_of_struct_3.tag == 1:
                            return FSharpResult_2(1, copy_of_struct_3.fields[0])

                        else: 
                            copy_of_struct_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__G_]]] = match_value_4
                            if copy_of_struct_4.tag == 1:
                                return FSharpResult_2(1, copy_of_struct_4.fields[0])

                            else: 
                                copy_of_struct_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__G_]]] = match_value_5
                                return FSharpResult_2(1, copy_of_struct_5.fields[0]) if (copy_of_struct_5.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0], copy_of_struct_3.fields[0], copy_of_struct_4.fields[0], copy_of_struct_5.fields[0]))






    return ObjectExpr149()


def map7(ctor: Callable[[_A, _B, _C, _D, _E, _F, _G], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any], d4: Decoder_1[Any], d5: Decoder_1[Any], d6: Decoder_1[Any], d7: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr150(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3, d4: Any=d4, d5: Any=d5, d6: Any=d6, d7: Any=d7) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__H_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__H_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__H_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__H_]]] = d3.Decode(helpers, value_1)
            match_value_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__H_]]] = d4.Decode(helpers, value_1)
            match_value_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__H_]]] = d5.Decode(helpers, value_1)
            match_value_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__H_]]] = d6.Decode(helpers, value_1)
            match_value_6: FSharpResult_2[_G_, tuple[str, ErrorReason_1[__H_]]] = d7.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__H_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__H_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__H_]]] = match_value_2
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, copy_of_struct_2.fields[0])

                    else: 
                        copy_of_struct_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__H_]]] = match_value_3
                        if copy_of_struct_3.tag == 1:
                            return FSharpResult_2(1, copy_of_struct_3.fields[0])

                        else: 
                            copy_of_struct_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__H_]]] = match_value_4
                            if copy_of_struct_4.tag == 1:
                                return FSharpResult_2(1, copy_of_struct_4.fields[0])

                            else: 
                                copy_of_struct_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__H_]]] = match_value_5
                                if copy_of_struct_5.tag == 1:
                                    return FSharpResult_2(1, copy_of_struct_5.fields[0])

                                else: 
                                    copy_of_struct_6: FSharpResult_2[_G_, tuple[str, ErrorReason_1[__H_]]] = match_value_6
                                    return FSharpResult_2(1, copy_of_struct_6.fields[0]) if (copy_of_struct_6.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0], copy_of_struct_3.fields[0], copy_of_struct_4.fields[0], copy_of_struct_5.fields[0], copy_of_struct_6.fields[0]))







    return ObjectExpr150()


def map8(ctor: Callable[[_A, _B, _C, _D, _E, _F, _G, _H], _OUTPUT], d1: Decoder_1[Any], d2: Decoder_1[Any], d3: Decoder_1[Any], d4: Decoder_1[Any], d5: Decoder_1[Any], d6: Decoder_1[Any], d7: Decoder_1[Any], d8: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr151(Decoder_1[_OUTPUT_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, ctor: Any=ctor, d1: Any=d1, d2: Any=d2, d3: Any=d3, d4: Any=d4, d5: Any=d5, d6: Any=d6, d7: Any=d7, d8: Any=d8) -> FSharpResult_2[_OUTPUT_, tuple[str, ErrorReason_1[__I_]]]:
            match_value: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__I_]]] = d1.Decode(helpers, value_1)
            match_value_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__I_]]] = d2.Decode(helpers, value_1)
            match_value_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__I_]]] = d3.Decode(helpers, value_1)
            match_value_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__I_]]] = d4.Decode(helpers, value_1)
            match_value_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__I_]]] = d5.Decode(helpers, value_1)
            match_value_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__I_]]] = d6.Decode(helpers, value_1)
            match_value_6: FSharpResult_2[_G_, tuple[str, ErrorReason_1[__I_]]] = d7.Decode(helpers, value_1)
            match_value_7: FSharpResult_2[_H_, tuple[str, ErrorReason_1[__I_]]] = d8.Decode(helpers, value_1)
            copy_of_struct: FSharpResult_2[_A_, tuple[str, ErrorReason_1[__I_]]] = match_value
            if copy_of_struct.tag == 1:
                return FSharpResult_2(1, copy_of_struct.fields[0])

            else: 
                copy_of_struct_1: FSharpResult_2[_B_, tuple[str, ErrorReason_1[__I_]]] = match_value_1
                if copy_of_struct_1.tag == 1:
                    return FSharpResult_2(1, copy_of_struct_1.fields[0])

                else: 
                    copy_of_struct_2: FSharpResult_2[_C_, tuple[str, ErrorReason_1[__I_]]] = match_value_2
                    if copy_of_struct_2.tag == 1:
                        return FSharpResult_2(1, copy_of_struct_2.fields[0])

                    else: 
                        copy_of_struct_3: FSharpResult_2[_D_, tuple[str, ErrorReason_1[__I_]]] = match_value_3
                        if copy_of_struct_3.tag == 1:
                            return FSharpResult_2(1, copy_of_struct_3.fields[0])

                        else: 
                            copy_of_struct_4: FSharpResult_2[_E_, tuple[str, ErrorReason_1[__I_]]] = match_value_4
                            if copy_of_struct_4.tag == 1:
                                return FSharpResult_2(1, copy_of_struct_4.fields[0])

                            else: 
                                copy_of_struct_5: FSharpResult_2[_F_, tuple[str, ErrorReason_1[__I_]]] = match_value_5
                                if copy_of_struct_5.tag == 1:
                                    return FSharpResult_2(1, copy_of_struct_5.fields[0])

                                else: 
                                    copy_of_struct_6: FSharpResult_2[_G_, tuple[str, ErrorReason_1[__I_]]] = match_value_6
                                    if copy_of_struct_6.tag == 1:
                                        return FSharpResult_2(1, copy_of_struct_6.fields[0])

                                    else: 
                                        copy_of_struct_7: FSharpResult_2[_H_, tuple[str, ErrorReason_1[__I_]]] = match_value_7
                                        return FSharpResult_2(1, copy_of_struct_7.fields[0]) if (copy_of_struct_7.tag == 1) else FSharpResult_2(0, ctor(copy_of_struct.fields[0], copy_of_struct_1.fields[0], copy_of_struct_2.fields[0], copy_of_struct_3.fields[0], copy_of_struct_4.fields[0], copy_of_struct_5.fields[0], copy_of_struct_6.fields[0], copy_of_struct_7.fields[0]))








    return ObjectExpr151()


def lossy_option(decoder: Decoder_1[Any]) -> Decoder_1[Any | None]:
    class ObjectExpr152(Decoder_1[_VALUE_ | None]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, decoder: Any=decoder) -> FSharpResult_2[_VALUE_ | None, tuple[str, ErrorReason_1[__A_]]]:
            return FSharpResult_2(0, None) if helpers.is_null_value(value_1) else Result_Map(some, decoder.Decode(helpers, value_1))

    return ObjectExpr152()


def lossless_option(decoder: Decoder_1[Any]) -> Decoder_1[Any | None]:
    def cb_1(type_name: str, decoder: Any=decoder) -> Decoder_1[_VALUE | None]:
        if type_name == "option":
            def cb(state: str, type_name: Any=type_name) -> Decoder_1[_VALUE | None]:
                if state == "none":
                    return succeed(None)

                elif state == "some":
                    def ctor(Value: _VALUE | None=None, state: Any=state) -> _VALUE | None:
                        return some(Value)

                    return map(ctor, field("$value", decoder))

                else: 
                    return fail("Expecting a state field with value \'none\' or \'some\' but got " + state)


            return and_then(cb, field("$case", string))

        else: 
            return fail("Expecting an Option type but got " + type_name)


    return and_then(cb_1, field("$type", string))


def and_map(__unit: None=None) -> Callable[[Decoder_1[_A], Decoder_1[Callable[[_A], _B]]], Decoder_1[_B]]:
    def _arrow154(d: Decoder_1[_A]) -> Callable[[Decoder_1[Callable[[_A], _B]]], Decoder_1[_B]]:
        def _arrow153(d_1: Decoder_1[Callable[[_A], _B]]) -> Decoder_1[_B]:
            def ctor(arg: _A, func: Callable[[_A], _B]) -> _B:
                return func(arg)

            return map2(ctor, d, d_1)

        return _arrow153

    return _arrow154


class IRequiredGetter(Protocol):
    @abstractmethod
    def At(self, __arg0: FSharpList[str], __arg1: Decoder_1[_A]) -> _A:
        ...

    @abstractmethod
    def Field(self, __arg0: str, __arg1: Decoder_1[_A]) -> _A:
        ...

    @abstractmethod
    def Raw(self, __arg0: Decoder_1[_A]) -> _A:
        ...


class IOptionalGetter(Protocol):
    @abstractmethod
    def At(self, __arg0: FSharpList[str], __arg1: Decoder_1[_A]) -> _A | None:
        ...

    @abstractmethod
    def Field(self, __arg0: str, __arg1: Decoder_1[_A]) -> _A | None:
        ...

    @abstractmethod
    def Raw(self, __arg0: Decoder_1[_A]) -> _A | None:
        ...


class IGetters(Protocol):
    @property
    @abstractmethod
    def Optional(self) -> IOptionalGetter:
        ...

    @property
    @abstractmethod
    def Required(self) -> IRequiredGetter:
        ...


def unwrap_with(errors: Array[tuple[str, ErrorReason_1[_JSONVALUE]]], helpers: IDecoderHelpers_1[Any], decoder: Decoder_1[Any], value_1: Any) -> Any:
    match_value: FSharpResult_2[_T, tuple[str, ErrorReason_1[_JSONVALUE]]] = decoder.Decode(helpers, value_1)
    if match_value.tag == 1:
        (errors.append(match_value.fields[0]))
        return None

    else: 
        return match_value.fields[0]



def _expr159(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("Thoth.Json.Core.Decode.Getters`2", [gen0, gen1], Getters_2)


class Getters_2(Generic[_JSONVALUE, _T]):
    def __init__(self, helpers: IDecoderHelpers_1[Any], value_1: Any) -> None:
        self.errors: Array[tuple[str, ErrorReason_1[_JSONVALUE]]] = []
        def _arrow156(__unit: None=None) -> IRequiredGetter:
            _this: Any = self
            class ObjectExpr155(IRequiredGetter):
                def Field(self, field_name: str, decoder: Decoder_1[Any]) -> Any:
                    return unwrap_with(_this.errors, helpers, field(field_name, decoder), value_1)

                def At(self, field_names: FSharpList[str], decoder_1: Decoder_1[Any]) -> Any:
                    return unwrap_with(_this.errors, helpers, at(field_names, decoder_1), value_1)

                def Raw(self, decoder_2: Decoder_1[Any]) -> Any:
                    return unwrap_with(_this.errors, helpers, decoder_2, value_1)

            return ObjectExpr155()

        self.required: IRequiredGetter = _arrow156()
        def _arrow158(__unit: None=None) -> IOptionalGetter:
            _this_1: Any = self
            class ObjectExpr157(IOptionalGetter):
                def Field(self, field_name_1: str, decoder_3: Decoder_1[Any]) -> Any | None:
                    return unwrap_with(_this_1.errors, helpers, optional(field_name_1, decoder_3), value_1)

                def At(self, field_names_1: FSharpList[str], decoder_4: Decoder_1[Any]) -> Any | None:
                    return unwrap_with(_this_1.errors, helpers, optional_at(field_names_1, decoder_4), value_1)

                def Raw(self, decoder_5: Decoder_1[Any]) -> Any | None:
                    match_value: FSharpResult_2[__A_, tuple[str, ErrorReason_1[_JSONVALUE_]]] = decoder_5.Decode(helpers, value_1)
                    if match_value.tag == 1:
                        reason: ErrorReason_1[_JSONVALUE_] = match_value.fields[0][1]
                        error: tuple[str, ErrorReason_1[_JSONVALUE_]] = match_value.fields[0]
                        (pattern_matching_result, v_1) = (None, None)
                        if reason.tag == 1:
                            pattern_matching_result = 0
                            v_1 = reason.fields[1]

                        elif reason.tag == 2:
                            pattern_matching_result = 0
                            v_1 = reason.fields[1]

                        elif (reason.tag == 3) or (reason.tag == 4):
                            pattern_matching_result = 1

                        elif ((reason.tag == 5) or (reason.tag == 6)) or (reason.tag == 7):
                            pattern_matching_result = 2

                        else: 
                            pattern_matching_result = 0
                            v_1 = reason.fields[1]

                        if pattern_matching_result == 0:
                            if helpers.is_null_value(v_1):
                                return None

                            else: 
                                (_this_1.errors.append(error))
                                return None


                        elif pattern_matching_result == 1:
                            return None

                        elif pattern_matching_result == 2:
                            (_this_1.errors.append(error))
                            return None


                    else: 
                        return some(match_value.fields[0])


            return ObjectExpr157()

        self.optional: IOptionalGetter = _arrow158()

    @property
    def Required(self, __unit: None=None) -> IRequiredGetter:
        __: Getters_2[_JSONVALUE, _T] = self
        return __.required

    @property
    def Optional(self, __unit: None=None) -> IOptionalGetter:
        __: Getters_2[_JSONVALUE, _T] = self
        return __.optional


Getters_2_reflection = _expr159

def Getters_2__ctor_Z4BE6C149(helpers: IDecoderHelpers_1[Any], value_1: Any) -> Getters_2[_JSONVALUE]:
    return Getters_2(helpers, value_1)


def Getters_2__get_Errors(__: Getters_2[Any, Any]) -> FSharpList[tuple[str, ErrorReason_1[_JSONVALUE]]]:
    return to_list(__.errors)


def object(builder: Callable[[IGetters], _VALUE]) -> Decoder_1[Any]:
    class ObjectExpr160(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value_1: Any, builder: Any=builder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value_1)
            result: _VALUE_ = builder(getters)
            match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
            if not is_empty(match_value):
                errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head_1(match_value))

            else: 
                return FSharpResult_2(0, result)


    return ObjectExpr160()


def tuple2(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2]]:
    def cb_1(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2) -> Decoder_1[tuple[_T1, _T2]]:
        def cb(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2]]:
            return succeed((v1, v2))

        return and_then(cb, index(1, decoder2))

    return and_then(cb_1, index(0, decoder1))


def tuple3(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3]]:
    def cb_2(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3) -> Decoder_1[tuple[_T1, _T2, _T3]]:
        def cb_1(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3]]:
            def cb(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3]]:
                return succeed((v1, v2, v3))

            return and_then(cb, index(2, decoder3))

        return and_then(cb_1, index(1, decoder2))

    return and_then(cb_2, index(0, decoder1))


def tuple4(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any], decoder4: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3, _T4]]:
    def cb_3(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3, decoder4: Any=decoder4) -> Decoder_1[tuple[_T1, _T2, _T3, _T4]]:
        def cb_2(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3, _T4]]:
            def cb_1(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3, _T4]]:
                def cb(v4: _T4 | None=None, v3: Any=v3) -> Decoder_1[tuple[_T1, _T2, _T3, _T4]]:
                    return succeed((v1, v2, v3, v4))

                return and_then(cb, index(3, decoder4))

            return and_then(cb_1, index(2, decoder3))

        return and_then(cb_2, index(1, decoder2))

    return and_then(cb_3, index(0, decoder1))


def tuple5(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any], decoder4: Decoder_1[Any], decoder5: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
    def cb_4(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3, decoder4: Any=decoder4, decoder5: Any=decoder5) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
        def cb_3(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
            def cb_2(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
                def cb_1(v4: _T4 | None=None, v3: Any=v3) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
                    def cb(v5: _T5 | None=None, v4: Any=v4) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5]]:
                        return succeed((v1, v2, v3, v4, v5))

                    return and_then(cb, index(4, decoder5))

                return and_then(cb_1, index(3, decoder4))

            return and_then(cb_2, index(2, decoder3))

        return and_then(cb_3, index(1, decoder2))

    return and_then(cb_4, index(0, decoder1))


def tuple6(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any], decoder4: Decoder_1[Any], decoder5: Decoder_1[Any], decoder6: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
    def cb_5(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3, decoder4: Any=decoder4, decoder5: Any=decoder5, decoder6: Any=decoder6) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
        def cb_4(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
            def cb_3(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
                def cb_2(v4: _T4 | None=None, v3: Any=v3) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
                    def cb_1(v5: _T5 | None=None, v4: Any=v4) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
                        def cb(v6: _T6 | None=None, v5: Any=v5) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6]]:
                            return succeed((v1, v2, v3, v4, v5, v6))

                        return and_then(cb, index(5, decoder6))

                    return and_then(cb_1, index(4, decoder5))

                return and_then(cb_2, index(3, decoder4))

            return and_then(cb_3, index(2, decoder3))

        return and_then(cb_4, index(1, decoder2))

    return and_then(cb_5, index(0, decoder1))


def tuple7(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any], decoder4: Decoder_1[Any], decoder5: Decoder_1[Any], decoder6: Decoder_1[Any], decoder7: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
    def cb_6(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3, decoder4: Any=decoder4, decoder5: Any=decoder5, decoder6: Any=decoder6, decoder7: Any=decoder7) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
        def cb_5(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
            def cb_4(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
                def cb_3(v4: _T4 | None=None, v3: Any=v3) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
                    def cb_2(v5: _T5 | None=None, v4: Any=v4) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
                        def cb_1(v6: _T6 | None=None, v5: Any=v5) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
                            def cb(v7: _T7 | None=None, v6: Any=v6) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7]]:
                                return succeed((v1, v2, v3, v4, v5, v6, v7))

                            return and_then(cb, index(6, decoder7))

                        return and_then(cb_1, index(5, decoder6))

                    return and_then(cb_2, index(4, decoder5))

                return and_then(cb_3, index(3, decoder4))

            return and_then(cb_4, index(2, decoder3))

        return and_then(cb_5, index(1, decoder2))

    return and_then(cb_6, index(0, decoder1))


def tuple8(decoder1: Decoder_1[Any], decoder2: Decoder_1[Any], decoder3: Decoder_1[Any], decoder4: Decoder_1[Any], decoder5: Decoder_1[Any], decoder6: Decoder_1[Any], decoder7: Decoder_1[Any], decoder8: Decoder_1[Any]) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
    def cb_7(v1: _T1 | None=None, decoder1: Any=decoder1, decoder2: Any=decoder2, decoder3: Any=decoder3, decoder4: Any=decoder4, decoder5: Any=decoder5, decoder6: Any=decoder6, decoder7: Any=decoder7, decoder8: Any=decoder8) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
        def cb_6(v2: _T2 | None=None, v1: Any=v1) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
            def cb_5(v3: _T3 | None=None, v2: Any=v2) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                def cb_4(v4: _T4 | None=None, v3: Any=v3) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                    def cb_3(v5: _T5 | None=None, v4: Any=v4) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                        def cb_2(v6: _T6 | None=None, v5: Any=v5) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                            def cb_1(v7: _T7 | None=None, v6: Any=v6) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                                def cb(v8: _T8 | None=None, v7: Any=v7) -> Decoder_1[tuple[_T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]:
                                    return succeed((v1, v2, v3, v4, v5, v6, v7, v8))

                                return and_then(cb, index(7, decoder8))

                            return and_then(cb_1, index(6, decoder7))

                        return and_then(cb_2, index(5, decoder6))

                    return and_then(cb_3, index(4, decoder5))

                return and_then(cb_4, index(3, decoder4))

            return and_then(cb_5, index(2, decoder3))

        return and_then(cb_6, index(1, decoder2))

    return and_then(cb_7, index(0, decoder1))


def dict_1(decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    def _arrow162(elements: FSharpList[tuple[str, _VALUE]], decoder: Any=decoder) -> Any:
        class ObjectExpr161:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return of_list(elements, ObjectExpr161())

    return map(_arrow162, key_value_pairs(decoder))


def map_0027(key_decoder: Decoder_1[Any], value_decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    def _arrow164(elements: Array[tuple[_KEY, _VALUE]], key_decoder: Any=key_decoder, value_decoder: Any=value_decoder) -> Any:
        class ObjectExpr163:
            @property
            def Compare(self) -> Callable[[_KEY_, _KEY_], int]:
                return compare

        return of_seq_1(elements, ObjectExpr163())

    return map(_arrow164, array(tuple2(key_decoder, value_decoder)))


__all__ = ["Helpers_prependPath", "generic_msg", "error_to_string", "Advanced_fromValue", "string", "char", "guid", "unit", "sbyte", "byte", "int16", "uint16", "int_1", "uint32", "int64", "uint64", "bigint", "bool_1", "float_1", "float32", "decimal", "datetime_local", "timespan", "decode_maybe_null", "optional", "bad_path_error", "map2", "optional_at", "field", "at", "index", "list_1", "resize_array", "seq", "array", "keys", "key_value_pairs", "one_of", "nil", "value", "succeed", "fail", "and_then", "all", "map", "map3", "map4", "map5", "map6", "map7", "map8", "lossy_option", "lossless_option", "and_map", "unwrap_with", "Getters_2_reflection", "Getters_2__get_Errors", "object", "tuple2", "tuple3", "tuple4", "tuple5", "tuple6", "tuple7", "tuple8", "dict_1", "map_0027"]


from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from typing import (Any, Protocol, TypeVar)
from ..fable_library.boolean import try_parse as try_parse_2
from ..fable_library.date import (min_value, try_parse as try_parse_3)
from ..fable_library.date_offset import (min_value as min_value_1, try_parse as try_parse_4)
from ..fable_library.double import try_parse as try_parse_1
from ..fable_library.int32 import try_parse
from ..fable_library.list import (is_empty, head, tail, map as map_1, FSharpList, to_array, try_find, filter, exists, iterate)
from ..fable_library.map import (of_list, of_seq)
from ..fable_library.map_util import add_to_dict
from ..fable_library.mutable_map import Dictionary
from ..fable_library.option import (some, map as map_3, value as value_1)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import map as map_2
from ..fable_library.string_ import (to_text, printf)
from ..fable_library.types import (FSharpRef, Array)
from ..fable_library.util import (compare, equals as equals_1, structural_hash, IEnumerable_1)
from .Interop.py_interop import is_string
from .reader import read as read_1
from .yamlicious_types import YAMLElement

_A = TypeVar("_A")

_B = TypeVar("_B")

_A_ = TypeVar("_A_")

_C = TypeVar("_C")

_D = TypeVar("_D")

_E = TypeVar("_E")

_F = TypeVar("_F")

_G = TypeVar("_G")

_H = TypeVar("_H")

__A_ = TypeVar("__A_")

def Helper_isString(value: str) -> bool:
    return is_string(value)


def int_1(value: YAMLElement) -> int:
    (pattern_matching_result, v) = (None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        match_value: tuple[bool, int]
        out_arg: int = 0
        def _arrow442(__unit: None=None, value: Any=value) -> int:
            return out_arg

        def _arrow443(v_1: int, value: Any=value) -> None:
            nonlocal out_arg
            out_arg = v_1 or 0

        match_value = (try_parse(v.Value, 511, False, 32, FSharpRef(_arrow442, _arrow443)), out_arg)
        if match_value[0]:
            return match_value[1]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected an int")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected an YAMLElement.Value")(value) + "\\nParameter name: ") + "value")



def float_1(value: YAMLElement) -> float:
    Culture: Any = {}
    (pattern_matching_result, v) = (None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1


            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        match_value: tuple[bool, float]
        out_arg: float = 0.0
        def _arrow444(__unit: None=None, value: Any=value) -> float:
            return out_arg

        def _arrow445(v_1: float, value: Any=value) -> None:
            nonlocal out_arg
            out_arg = v_1

        match_value = (try_parse_1(v.Value, FSharpRef(_arrow444, _arrow445)), out_arg)
        if match_value[0]:
            return match_value[1]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected an int")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected an YAMLElement.Value")(value) + "\\nParameter name: ") + "value")



def char(value: YAMLElement) -> str:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        if Helper_isString(v.Value):
            return v.Value[0]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected a char")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a char")(any_else) + "\\nParameter name: ") + "value")



def bool_1(value: YAMLElement) -> bool:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        match_value: tuple[bool, bool]
        out_arg: bool = False
        def _arrow446(__unit: None=None, value: Any=value) -> bool:
            return out_arg

        def _arrow447(v_1: bool, value: Any=value) -> None:
            nonlocal out_arg
            out_arg = v_1

        match_value = (try_parse_2(v.Value, FSharpRef(_arrow446, _arrow447)), out_arg)
        if match_value[0]:
            return match_value[1]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected a bool")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a bool")(any_else) + "\\nParameter name: ") + "value")



def map(key_decoder: Callable[[str], _A], value_decoder: Callable[[YAMLElement], _B], value: YAMLElement) -> Any:
    if value.tag == 3:
        def mapping(x: YAMLElement, key_decoder: Any=key_decoder, value_decoder: Any=value_decoder, value: Any=value) -> tuple[_A, _B]:
            if x.tag == 0:
                return (key_decoder(x.fields[0].Value), value_decoder(x.fields[1]))

            else: 
                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(x) + "\\nParameter name: ") + "value")


        class ObjectExpr448:
            @property
            def Compare(self) -> Callable[[_A_, _A_], int]:
                return compare

        return of_list(map_1(mapping, value.fields[0]), ObjectExpr448())

    else: 
        raise Exception((to_text(printf("%s: %A"))("Expected a map")(value) + "\\nParameter name: ") + "value")



def dict_1(key_decoder: Callable[[str], _A], value_decoder: Callable[[YAMLElement], _B], value: YAMLElement) -> Any:
    if value.tag == 3:
        def mapping(x: YAMLElement, key_decoder: Any=key_decoder, value_decoder: Any=value_decoder, value: Any=value) -> tuple[_A, _B]:
            if x.tag == 0:
                return (key_decoder(x.fields[0].Value), value_decoder(x.fields[1]))

            else: 
                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(x) + "\\nParameter name: ") + "value")


        class ObjectExpr449:
            @property
            def Compare(self) -> Callable[[_A_, _A_], int]:
                return compare

        class ObjectExpr450:
            @property
            def Equals(self) -> Callable[[_A_, _A_], bool]:
                return equals_1

            @property
            def GetHashCode(self) -> Callable[[_A_], int]:
                return structural_hash

        return Dictionary(of_seq(map_1(mapping, value.fields[0]), ObjectExpr449()), ObjectExpr450())

    else: 
        raise Exception((to_text(printf("%s: %A"))("Expected a dictionary")(value) + "\\nParameter name: ") + "value")



def datetime(value: YAMLElement) -> Any:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        match_value: tuple[bool, Any]
        out_arg: Any = min_value()
        def _arrow451(__unit: None=None, value: Any=value) -> Any:
            return out_arg

        def _arrow452(v_1: Any, value: Any=value) -> None:
            nonlocal out_arg
            out_arg = v_1

        match_value = (try_parse_3(v.Value, FSharpRef(_arrow451, _arrow452)), out_arg)
        if match_value[0]:
            return match_value[1]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected a DateTime")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a DateTime")(any_else) + "\\nParameter name: ") + "value")



def datetime_offset(value: YAMLElement) -> Any:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        match_value: tuple[bool, Any]
        out_arg: Any = min_value_1()
        def _arrow453(__unit: None=None, value: Any=value) -> Any:
            return out_arg

        def _arrow454(v_1: Any, value: Any=value) -> None:
            nonlocal out_arg
            out_arg = v_1

        match_value = (try_parse_4(v.Value, FSharpRef(_arrow453, _arrow454)), out_arg)
        if match_value[0]:
            return match_value[1]

        else: 
            raise Exception((to_text(printf("%s: %A"))("Expected a DateTimeOffset")(v.Value) + "\\nParameter name: ") + "value")


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a DateTimeOffset")(any_else) + "\\nParameter name: ") + "value")



def option(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> Any | None:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        if v.Value == "null":
            return None

        else: 
            return some(decoder(value))


    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected an option")(any_else) + "\\nParameter name: ") + "value")



def string(value: YAMLElement) -> str:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 1:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 1:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return v.Value

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a string")(any_else) + "\\nParameter name: ") + "value")



def tuple2(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], value: YAMLElement) -> tuple[_A, _B]:
    (pattern_matching_result, a, b, any_else) = (None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if is_empty(tail(value.fields[0])):
                                pattern_matching_result = 0
                                a = head(head(value.fields[0]).fields[0])
                                b = head(tail(head(value.fields[0]).fields[0]))

                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if is_empty(tail(tail(value.fields[0]))):
                    pattern_matching_result = 0
                    a = head(value.fields[0])
                    b = head(tail(value.fields[0]))

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple2")(any_else) + "\\nParameter name: ") + "value")



def tuple3(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], value: YAMLElement) -> tuple[_A, _B, _C]:
    (pattern_matching_result, a, b, c, any_else) = (None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if is_empty(tail(value.fields[0])):
                                    pattern_matching_result = 0
                                    a = head(head(value.fields[0]).fields[0])
                                    b = head(tail(head(value.fields[0]).fields[0]))
                                    c = head(tail(tail(head(value.fields[0]).fields[0])))

                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if is_empty(tail(tail(tail(value.fields[0])))):
                        pattern_matching_result = 0
                        a = head(value.fields[0])
                        b = head(tail(value.fields[0]))
                        c = head(tail(tail(value.fields[0])))

                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple3")(any_else) + "\\nParameter name: ") + "value")



def tuple4(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], decoder_d: Callable[[YAMLElement], _D], value: YAMLElement) -> tuple[_A, _B, _C, _D]:
    (pattern_matching_result, a, b, c, d, any_else) = (None, None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if not is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if is_empty(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))):
                                    if is_empty(tail(value.fields[0])):
                                        pattern_matching_result = 0
                                        a = head(head(value.fields[0]).fields[0])
                                        b = head(tail(head(value.fields[0]).fields[0]))
                                        c = head(tail(tail(head(value.fields[0]).fields[0])))
                                        d = head(tail(tail(tail(head(value.fields[0]).fields[0]))))

                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if not is_empty(tail(tail(tail(value.fields[0])))):
                        if is_empty(tail(tail(tail(tail(value.fields[0]))))):
                            pattern_matching_result = 0
                            a = head(value.fields[0])
                            b = head(tail(value.fields[0]))
                            c = head(tail(tail(value.fields[0])))
                            d = head(tail(tail(tail(value.fields[0]))))

                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c), decoder_d(d))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple4")(any_else) + "\\nParameter name: ") + "value")



def tuple5(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], decoder_d: Callable[[YAMLElement], _D], decoder_e: Callable[[YAMLElement], _E], value: YAMLElement) -> tuple[_A, _B, _C, _D, _E]:
    (pattern_matching_result, a, b, c, d, e, any_else) = (None, None, None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if not is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if not is_empty(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))):
                                    if is_empty(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))):
                                        if is_empty(tail(value.fields[0])):
                                            pattern_matching_result = 0
                                            a = head(head(value.fields[0]).fields[0])
                                            b = head(tail(head(value.fields[0]).fields[0]))
                                            c = head(tail(tail(head(value.fields[0]).fields[0])))
                                            d = head(tail(tail(tail(head(value.fields[0]).fields[0]))))
                                            e = head(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))

                                        else: 
                                            pattern_matching_result = 1
                                            any_else = value


                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if not is_empty(tail(tail(tail(value.fields[0])))):
                        if not is_empty(tail(tail(tail(tail(value.fields[0]))))):
                            if is_empty(tail(tail(tail(tail(tail(value.fields[0])))))):
                                pattern_matching_result = 0
                                a = head(value.fields[0])
                                b = head(tail(value.fields[0]))
                                c = head(tail(tail(value.fields[0])))
                                d = head(tail(tail(tail(value.fields[0]))))
                                e = head(tail(tail(tail(tail(value.fields[0])))))

                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c), decoder_d(d), decoder_e(e))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple5")(any_else) + "\\nParameter name: ") + "value")



def tuple6(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], decoder_d: Callable[[YAMLElement], _D], decoder_e: Callable[[YAMLElement], _E], decoder_f: Callable[[YAMLElement], _F], value: YAMLElement) -> tuple[_A, _B, _C, _D, _E, _F]:
    (pattern_matching_result, a, b, c, d, e, f, any_else) = (None, None, None, None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if not is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if not is_empty(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))):
                                    if not is_empty(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))):
                                        if is_empty(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))):
                                            if is_empty(tail(value.fields[0])):
                                                pattern_matching_result = 0
                                                a = head(head(value.fields[0]).fields[0])
                                                b = head(tail(head(value.fields[0]).fields[0]))
                                                c = head(tail(tail(head(value.fields[0]).fields[0])))
                                                d = head(tail(tail(tail(head(value.fields[0]).fields[0]))))
                                                e = head(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))
                                                f = head(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))

                                            else: 
                                                pattern_matching_result = 1
                                                any_else = value


                                        else: 
                                            pattern_matching_result = 1
                                            any_else = value


                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if not is_empty(tail(tail(tail(value.fields[0])))):
                        if not is_empty(tail(tail(tail(tail(value.fields[0]))))):
                            if not is_empty(tail(tail(tail(tail(tail(value.fields[0])))))):
                                if is_empty(tail(tail(tail(tail(tail(tail(value.fields[0]))))))):
                                    pattern_matching_result = 0
                                    a = head(value.fields[0])
                                    b = head(tail(value.fields[0]))
                                    c = head(tail(tail(value.fields[0])))
                                    d = head(tail(tail(tail(value.fields[0]))))
                                    e = head(tail(tail(tail(tail(value.fields[0])))))
                                    f = head(tail(tail(tail(tail(tail(value.fields[0]))))))

                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c), decoder_d(d), decoder_e(e), decoder_f(f))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple6")(any_else) + "\\nParameter name: ") + "value")



def tuple7(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], decoder_d: Callable[[YAMLElement], _D], decoder_e: Callable[[YAMLElement], _E], decoder_f: Callable[[YAMLElement], _F], decoder_g: Callable[[YAMLElement], _G], value: YAMLElement) -> tuple[_A, _B, _C, _D, _E, _F, _G]:
    (pattern_matching_result, a, b, c, d, e, f, g, any_else) = (None, None, None, None, None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if not is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if not is_empty(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))):
                                    if not is_empty(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))):
                                        if not is_empty(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))):
                                            if is_empty(tail(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))))):
                                                if is_empty(tail(value.fields[0])):
                                                    pattern_matching_result = 0
                                                    a = head(head(value.fields[0]).fields[0])
                                                    b = head(tail(head(value.fields[0]).fields[0]))
                                                    c = head(tail(tail(head(value.fields[0]).fields[0])))
                                                    d = head(tail(tail(tail(head(value.fields[0]).fields[0]))))
                                                    e = head(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))
                                                    f = head(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))
                                                    g = head(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))))

                                                else: 
                                                    pattern_matching_result = 1
                                                    any_else = value


                                            else: 
                                                pattern_matching_result = 1
                                                any_else = value


                                        else: 
                                            pattern_matching_result = 1
                                            any_else = value


                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if not is_empty(tail(tail(tail(value.fields[0])))):
                        if not is_empty(tail(tail(tail(tail(value.fields[0]))))):
                            if not is_empty(tail(tail(tail(tail(tail(value.fields[0])))))):
                                if not is_empty(tail(tail(tail(tail(tail(tail(value.fields[0]))))))):
                                    if is_empty(tail(tail(tail(tail(tail(tail(tail(value.fields[0])))))))):
                                        pattern_matching_result = 0
                                        a = head(value.fields[0])
                                        b = head(tail(value.fields[0]))
                                        c = head(tail(tail(value.fields[0])))
                                        d = head(tail(tail(tail(value.fields[0]))))
                                        e = head(tail(tail(tail(tail(value.fields[0])))))
                                        f = head(tail(tail(tail(tail(tail(value.fields[0]))))))
                                        g = head(tail(tail(tail(tail(tail(tail(value.fields[0])))))))

                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c), decoder_d(d), decoder_e(e), decoder_f(f), decoder_g(g))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple7")(any_else) + "\\nParameter name: ") + "value")



def tuple8(decoder_a: Callable[[YAMLElement], _A], decoder_b: Callable[[YAMLElement], _B], decoder_c: Callable[[YAMLElement], _C], decoder_d: Callable[[YAMLElement], _D], decoder_e: Callable[[YAMLElement], _E], decoder_f: Callable[[YAMLElement], _F], decoder_g: Callable[[YAMLElement], _G], decoder_h: Callable[[YAMLElement], _H], value: YAMLElement) -> tuple[_A, _B, _C, _D, _E, _F, _G, _H]:
    (pattern_matching_result, a, b, c, d, e, f, g, h, any_else) = (None, None, None, None, None, None, None, None, None, None)
    if value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if not is_empty(head(value.fields[0]).fields[0]):
                    if not is_empty(tail(head(value.fields[0]).fields[0])):
                        if not is_empty(tail(tail(head(value.fields[0]).fields[0]))):
                            if not is_empty(tail(tail(tail(head(value.fields[0]).fields[0])))):
                                if not is_empty(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))):
                                    if not is_empty(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))):
                                        if not is_empty(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))):
                                            if not is_empty(tail(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))))):
                                                if is_empty(tail(tail(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))))):
                                                    if is_empty(tail(value.fields[0])):
                                                        pattern_matching_result = 0
                                                        a = head(head(value.fields[0]).fields[0])
                                                        b = head(tail(head(value.fields[0]).fields[0]))
                                                        c = head(tail(tail(head(value.fields[0]).fields[0])))
                                                        d = head(tail(tail(tail(head(value.fields[0]).fields[0]))))
                                                        e = head(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))
                                                        f = head(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))
                                                        g = head(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0])))))))
                                                        h = head(tail(tail(tail(tail(tail(tail(tail(head(value.fields[0]).fields[0]))))))))

                                                    else: 
                                                        pattern_matching_result = 1
                                                        any_else = value


                                                else: 
                                                    pattern_matching_result = 1
                                                    any_else = value


                                            else: 
                                                pattern_matching_result = 1
                                                any_else = value


                                        else: 
                                            pattern_matching_result = 1
                                            any_else = value


                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    elif value.tag == 2:
        if not is_empty(value.fields[0]):
            if not is_empty(tail(value.fields[0])):
                if not is_empty(tail(tail(value.fields[0]))):
                    if not is_empty(tail(tail(tail(value.fields[0])))):
                        if not is_empty(tail(tail(tail(tail(value.fields[0]))))):
                            if not is_empty(tail(tail(tail(tail(tail(value.fields[0])))))):
                                if not is_empty(tail(tail(tail(tail(tail(tail(value.fields[0]))))))):
                                    if not is_empty(tail(tail(tail(tail(tail(tail(tail(value.fields[0])))))))):
                                        if is_empty(tail(tail(tail(tail(tail(tail(tail(tail(value.fields[0]))))))))):
                                            pattern_matching_result = 0
                                            a = head(value.fields[0])
                                            b = head(tail(value.fields[0]))
                                            c = head(tail(tail(value.fields[0])))
                                            d = head(tail(tail(tail(value.fields[0]))))
                                            e = head(tail(tail(tail(tail(value.fields[0])))))
                                            f = head(tail(tail(tail(tail(tail(value.fields[0]))))))
                                            g = head(tail(tail(tail(tail(tail(tail(value.fields[0])))))))
                                            h = head(tail(tail(tail(tail(tail(tail(tail(value.fields[0]))))))))

                                        else: 
                                            pattern_matching_result = 1
                                            any_else = value


                                    else: 
                                        pattern_matching_result = 1
                                        any_else = value


                                else: 
                                    pattern_matching_result = 1
                                    any_else = value


                            else: 
                                pattern_matching_result = 1
                                any_else = value


                        else: 
                            pattern_matching_result = 1
                            any_else = value


                    else: 
                        pattern_matching_result = 1
                        any_else = value


                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return (decoder_a(a), decoder_b(b), decoder_c(c), decoder_d(d), decoder_e(e), decoder_f(f), decoder_g(g), decoder_h(h))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a tuple8")(any_else) + "\\nParameter name: ") + "value")



def list_1(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> FSharpList[Any]:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 2:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return map_1(decoder, v)

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a list")(any_else) + "\\nParameter name: ") + "value")



def array(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> Array[Any]:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 2:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return to_array(map_1(decoder, v))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected an array")(any_else) + "\\nParameter name: ") + "value")



def seq(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> IEnumerable_1[Any]:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 2:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return map_2(decoder, v)

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a seq")(any_else) + "\\nParameter name: ") + "value")



def resizearray(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> Array[Any]:
    (pattern_matching_result, v, any_else) = (None, None, None)
    if value.tag == 2:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 1
                    any_else = value


            else: 
                pattern_matching_result = 1
                any_else = value


        else: 
            pattern_matching_result = 1
            any_else = value


    else: 
        pattern_matching_result = 1
        any_else = value

    if pattern_matching_result == 0:
        return list(map_1(decoder, v))

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a resizearray")(any_else) + "\\nParameter name: ") + "value")



def values(decoder: Callable[[YAMLElement], _A], value: YAMLElement) -> FSharpList[Any]:
    (pattern_matching_result, v, any_else_1) = (None, None, None)
    if value.tag == 2:
        pattern_matching_result = 0
        v = value.fields[0]

    elif value.tag == 3:
        if not is_empty(value.fields[0]):
            if head(value.fields[0]).tag == 2:
                if is_empty(tail(value.fields[0])):
                    pattern_matching_result = 0
                    v = head(value.fields[0]).fields[0]

                else: 
                    pattern_matching_result = 0
                    v = value.fields[0]


            else: 
                pattern_matching_result = 0
                v = value.fields[0]


        else: 
            pattern_matching_result = 0
            v = value.fields[0]


    else: 
        pattern_matching_result = 1
        any_else_1 = value

    if pattern_matching_result == 0:
        def mapping(_arg: YAMLElement, decoder: Any=decoder, value: Any=value) -> _A:
            if _arg.tag == 1:
                return decoder(_arg)

            else: 
                raise Exception((to_text(printf("%s: %A"))("Expected a values")(_arg) + "\\nParameter name: ") + "value")


        return map_1(mapping, v)

    elif pattern_matching_result == 1:
        raise Exception((to_text(printf("%s: %A"))("Expected a values")(any_else_1) + "\\nParameter name: ") + "value")



class IRequiredGetter(Protocol):
    @abstractmethod
    def Field(self, __arg0: str, __arg1: Callable[[YAMLElement], _A]) -> _A:
        ...


class IOptionalGetter(Protocol):
    @abstractmethod
    def Field(self, __arg0: str, __arg1: Callable[[YAMLElement], _A]) -> _A | None:
        ...


class IMultipleOptionalGetter(Protocol):
    @abstractmethod
    def FieldList(self, __arg0: FSharpList[str]) -> Any:
        ...


class IOverflowGetter(Protocol):
    @abstractmethod
    def FieldList(self, __arg0: FSharpList[str]) -> Any:
        ...


class IGetters(Protocol):
    @property
    @abstractmethod
    def MultipleOptional(self) -> IMultipleOptionalGetter:
        ...

    @property
    @abstractmethod
    def Optional(self) -> IOptionalGetter:
        ...

    @property
    @abstractmethod
    def Overflow(self) -> IOverflowGetter:
        ...

    @property
    @abstractmethod
    def Required(self) -> IRequiredGetter:
        ...


def _expr466() -> TypeInfo:
    return class_type("YAMLicious.Decode.Getter", None, Getter)


class Getter:
    def __init__(self, ele: YAMLElement) -> None:
        def _arrow459(__unit: None=None) -> IRequiredGetter:
            _this: Any = self
            class ObjectExpr458(IRequiredGetter):
                def Field(self, field_name: str, dec: Callable[[YAMLElement], __A_]) -> Any:
                    if ele.tag == 3:
                        def mapping(_arg_1: YAMLElement) -> __A_:
                            if _arg_1.tag == 0:
                                return dec(_arg_1.fields[1])

                            else: 
                                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(ele) + "\\nParameter name: ") + "value")


                        def predicate(_arg: YAMLElement) -> bool:
                            if _arg.tag == 0:
                                return _arg.fields[0].Value == field_name

                            else: 
                                return False


                        x: __A_ | None = map_3(mapping, try_find(predicate, ele.fields[0]))
                        if x is None:
                            def _arrow457(__unit: None=None) -> str:
                                arg_3: str = to_text(printf("Field not found: %s"))(field_name)
                                return to_text(printf("%s: %A"))(arg_3)(ele)

                            raise Exception((_arrow457() + "\\nParameter name: ") + "value")

                        else: 
                            return value_1(x)


                    else: 
                        raise Exception((to_text(printf("%s: %A"))("Expected an object")(ele) + "\\nParameter name: ") + "value")


            return ObjectExpr458()

        self.required: IRequiredGetter = _arrow459()
        def _arrow461(__unit: None=None) -> IOptionalGetter:
            _this_1: Any = self
            class ObjectExpr460(IOptionalGetter):
                def Field(self, field_name_1: str, dec_1: Callable[[YAMLElement], __A_]) -> Any | None:
                    if ele.tag == 3:
                        def mapping_1(_arg_3: YAMLElement) -> __A_:
                            if _arg_3.tag == 0:
                                return dec_1(_arg_3.fields[1])

                            else: 
                                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(ele) + "\\nParameter name: ") + "value")


                        def predicate_1(_arg_2: YAMLElement) -> bool:
                            if _arg_2.tag == 0:
                                return _arg_2.fields[0].Value == field_name_1

                            else: 
                                return False


                        return map_3(mapping_1, try_find(predicate_1, ele.fields[0]))

                    else: 
                        raise Exception((to_text(printf("%s: %A"))("Expected an object")(ele) + "\\nParameter name: ") + "value")


            return ObjectExpr460()

        self.optional: IOptionalGetter = _arrow461()
        def _arrow463(__unit: None=None) -> IMultipleOptionalGetter:
            _this_2: Any = self
            class ObjectExpr462(IMultipleOptionalGetter):
                def FieldList(self, field_names: FSharpList[str]) -> Any:
                    if ele.tag == 3:
                        def mapping_2(_arg_5: YAMLElement) -> tuple[str, YAMLElement]:
                            if _arg_5.tag == 0:
                                return (_arg_5.fields[0].Value, _arg_5.fields[1])

                            else: 
                                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(ele) + "\\nParameter name: ") + "value")


                        def predicate_3(_arg_4: YAMLElement) -> bool:
                            if _arg_4.tag == 0:
                                def predicate_2(x_1: str, _arg_4: Any=_arg_4) -> bool:
                                    return x_1 == _arg_4.fields[0].Value

                                return exists(predicate_2, field_names)

                            else: 
                                return False


                        overflow: FSharpList[tuple[str, YAMLElement]] = map_1(mapping_2, filter(predicate_3, ele.fields[0]))
                        dict_2: Any = dict([])
                        def action(tupled_arg: tuple[str, YAMLElement]) -> None:
                            add_to_dict(dict_2, tupled_arg[0], tupled_arg[1])

                        iterate(action, overflow)
                        return dict_2

                    else: 
                        raise Exception((to_text(printf("%s: %A"))("Expected an object")(ele) + "\\nParameter name: ") + "value")


            return ObjectExpr462()

        self.multiple_optional: IMultipleOptionalGetter = _arrow463()
        def _arrow465(__unit: None=None) -> IOverflowGetter:
            _this_3: Any = self
            class ObjectExpr464(IOverflowGetter):
                def FieldList(self, field_names_1: FSharpList[str]) -> Any:
                    if ele.tag == 3:
                        def mapping_3(_arg_7: YAMLElement) -> tuple[str, YAMLElement]:
                            if _arg_7.tag == 0:
                                return (_arg_7.fields[0].Value, _arg_7.fields[1])

                            else: 
                                raise Exception((to_text(printf("%s: %A"))("Expected a mapping")(ele) + "\\nParameter name: ") + "value")


                        def predicate_5(_arg_6: YAMLElement) -> bool:
                            if _arg_6.tag == 0:
                                def predicate_4(x_2: str, _arg_6: Any=_arg_6) -> bool:
                                    return x_2 == _arg_6.fields[0].Value

                                return not exists(predicate_4, field_names_1)

                            else: 
                                return False


                        overflow_1: FSharpList[tuple[str, YAMLElement]] = map_1(mapping_3, filter(predicate_5, ele.fields[0]))
                        dict_3: Any = dict([])
                        def action_1(tupled_arg_1: tuple[str, YAMLElement]) -> None:
                            add_to_dict(dict_3, tupled_arg_1[0], tupled_arg_1[1])

                        iterate(action_1, overflow_1)
                        return dict_3

                    else: 
                        raise Exception((to_text(printf("%s: %A"))("Expected an object")(ele) + "\\nParameter name: ") + "value")


            return ObjectExpr464()

        self.overflow: IOverflowGetter = _arrow465()

    @property
    def Required(self, __unit: None=None) -> IRequiredGetter:
        __: Getter = self
        return __.required

    @property
    def Optional(self, __unit: None=None) -> IOptionalGetter:
        __: Getter = self
        return __.optional

    @property
    def MultipleOptional(self, __unit: None=None) -> IMultipleOptionalGetter:
        __: Getter = self
        return __.multiple_optional

    @property
    def Overflow(self, __unit: None=None) -> IOverflowGetter:
        __: Getter = self
        return __.overflow


Getter_reflection = _expr466

def Getter__ctor_D9C929(ele: YAMLElement) -> Getter:
    return Getter(ele)


def object(getter: Callable[[IGetters], _A], value: YAMLElement) -> Any:
    return getter(Getter__ctor_D9C929(value))


def read(yaml: str) -> YAMLElement:
    return read_1(yaml)


__all__ = ["Helper_isString", "int_1", "float_1", "char", "bool_1", "map", "dict_1", "datetime", "datetime_offset", "option", "string", "tuple2", "tuple3", "tuple4", "tuple5", "tuple6", "tuple7", "tuple8", "list_1", "array", "seq", "resizearray", "values", "Getter_reflection", "object", "read"]


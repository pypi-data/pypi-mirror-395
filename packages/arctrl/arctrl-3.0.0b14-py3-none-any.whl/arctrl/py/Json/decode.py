from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from datetime import datetime
from typing import (Any, Protocol, TypeVar)
from ..fable_modules.fable_library.array_ import fold
from ..fable_modules.fable_library.date import to_universal_time
from ..fable_modules.fable_library.list import (FSharpList, is_empty, length, head, empty, cons, tail)
from ..fable_modules.fable_library.map_util import add_to_dict
from ..fable_modules.fable_library.mutable_map import Dictionary
from ..fable_modules.fable_library.result import (FSharpResult_2, Result_Map)
from ..fable_modules.fable_library.seq import exists
from ..fable_modules.fable_library.set import (contains, of_seq)
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (compare_primitives, IEnumerable_1, int32_to_string, equals, structural_hash)
from ..fable_modules.thoth_json_core.decode import (string, Getters_2__ctor_Z4BE6C149, Getters_2, Getters_2__get_Errors, IGetters, map, datetime_local, tuple2, int_1)
from ..fable_modules.thoth_json_core.types import (ErrorReason_1, Decoder_1, IDecoderHelpers_1)

_JSONVALUE = TypeVar("_JSONVALUE")

__A_ = TypeVar("__A_")

_VALUE_ = TypeVar("_VALUE_")

_VALUE = TypeVar("_VALUE")

_KEY__ = TypeVar("_KEY__")

_KEY_ = TypeVar("_KEY_")

class DateTimeStatic(Protocol):
    @abstractmethod
    def from_time_stamp(self, timestamp: float) -> Any:
        ...


def PyTime_toUniversalTimePy(dt: Any) -> Any:
    timestamp: float = to_universal_time(dt).timestamp()
    return datetime.fromtimestamp(timestamp=timestamp)


def Helpers_prependPath(path: str, err_: str, err__1: ErrorReason_1[Any]) -> tuple[str, ErrorReason_1[_JSONVALUE]]:
    err: tuple[str, ErrorReason_1[_JSONVALUE]] = (err_, err__1)
    return (path + err[0], err[1])


def Decode_isURI(s: str) -> bool:
    return True


class ObjectExpr2118(Decoder_1[str]):
    def Decode(self, s: IDecoderHelpers_1[Any], json: Any) -> FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]]:
        match_value: FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]] = string.Decode(s, json)
        if match_value.tag == 1:
            return FSharpResult_2(1, match_value.fields[0])

        elif Decode_isURI(match_value.fields[0]):
            return FSharpResult_2(0, match_value.fields[0])

        else: 
            s_3: str = match_value.fields[0]
            return FSharpResult_2(1, (s_3, ErrorReason_1(6, to_text(printf("Expected URI, got %s"))(s_3))))



Decode_uri: Decoder_1[str] = ObjectExpr2118()

def Decode_hasUnknownFields(helpers: IDecoderHelpers_1[Any], known_fields: Any, json: Any) -> bool:
    def predicate(x: str, helpers: Any=helpers, known_fields: Any=known_fields, json: Any=json) -> bool:
        return not contains(x, known_fields)

    return exists(predicate, helpers.get_properties(json))


def Decode_objectNoAdditionalProperties(allowed_properties: IEnumerable_1[str], builder: Callable[[IGetters], _VALUE]) -> Decoder_1[Any]:
    class ObjectExpr2119:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    allowed_properties_1: Any = of_seq(allowed_properties, ObjectExpr2119())
    class ObjectExpr2120(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, allowed_properties: Any=allowed_properties, builder: Any=builder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
            if Decode_hasUnknownFields(helpers, allowed_properties_1, value):
                return FSharpResult_2(1, ("Unknown fields in object", ErrorReason_1(0, "", value)))

            else: 
                result: _VALUE_ = builder(getters)
                match_value: FSharpList[tuple[str, ErrorReason_1[__A_]]] = Getters_2__get_Errors(getters)
                if not is_empty(match_value):
                    errors: FSharpList[tuple[str, ErrorReason_1[__A_]]] = match_value
                    return FSharpResult_2(1, ("", ErrorReason_1(7, errors))) if (length(errors) > 1) else FSharpResult_2(1, head(match_value))

                else: 
                    return FSharpResult_2(0, result)



    return ObjectExpr2120()


def Decode_noAdditionalProperties(allowed_properties: IEnumerable_1[str], decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr2121:
        @property
        def Compare(self) -> Callable[[str, str], int]:
            return compare_primitives

    allowed_properties_1: Any = of_seq(allowed_properties, ObjectExpr2121())
    class ObjectExpr2122(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, allowed_properties: Any=allowed_properties, decoder: Any=decoder) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            getters: Getters_2[__A_, Any] = Getters_2__ctor_Z4BE6C149(helpers, value)
            return FSharpResult_2(1, ("Unknown fields in object", ErrorReason_1(0, "", value))) if Decode_hasUnknownFields(helpers, allowed_properties_1, value) else decoder.Decode(helpers, value)

    return ObjectExpr2122()


def Decode_resizeArrayOrSingleton(decoder: Decoder_1[Any]) -> Decoder_1[Array[Any]]:
    class ObjectExpr2124(Decoder_1[Array[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, decoder: Any=decoder) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value):
                i: int = -1
                def folder(acc: FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]], value_1: __A_) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
                    nonlocal i
                    i = (i + 1) or 0
                    if acc.tag == 0:
                        acc_1: Array[_VALUE_] = acc.fields[0]
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_1)
                        if match_value.tag == 0:
                            (acc_1.append(match_value.fields[0]))
                            return FSharpResult_2(0, acc_1)

                        else: 
                            def _arrow2123(__unit: None=None, acc: Any=acc, value_1: Any=value_1) -> tuple[str, ErrorReason_1[__A_]]:
                                tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                                return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                            return FSharpResult_2(1, _arrow2123())


                    else: 
                        return acc


                return fold(folder, FSharpResult_2(0, []), helpers.as_array(value))

            else: 
                def mapping(x: _VALUE_ | None=None) -> Array[_VALUE_]:
                    return [x]

                return Result_Map(mapping, decoder.Decode(helpers, value))


    return ObjectExpr2124()


Decode_datetime: Decoder_1[Any] = map(PyTime_toUniversalTimePy, datetime_local)

def Decode_dictionary(key_decoder: Decoder_1[Any], value_decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr2126(Decoder_1[Any]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, key_decoder: Any=key_decoder, value_decoder: Any=value_decoder) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value):
                errors: FSharpList[Any] = empty()
                tokens: Array[__A_] = helpers.as_array(value)
                class ObjectExpr2125:
                    @property
                    def Equals(self) -> Callable[[_KEY__, _KEY__], bool]:
                        return equals

                    @property
                    def GetHashCode(self) -> Callable[[_KEY__], int]:
                        return structural_hash

                dict_1: Any = Dictionary([], ObjectExpr2125())
                decoder: Decoder_1[tuple[_KEY_, _VALUE_]] = tuple2(key_decoder, value_decoder)
                def folder(acc: FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]], value_1: __A_) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
                    if acc.tag == 0:
                        acc_1: Any = acc.fields[0]
                        match_value: FSharpResult_2[tuple[_KEY_, _VALUE_], tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_1)
                        if match_value.tag == 0:
                            tupled_arg: tuple[_KEY_, _VALUE_] = match_value.fields[0]
                            add_to_dict(acc_1, tupled_arg[0], tupled_arg[1])
                            return FSharpResult_2(0, acc_1)

                        else: 
                            return FSharpResult_2(1, match_value.fields[0])


                    else: 
                        return acc


                return fold(folder, FSharpResult_2(0, dict_1), tokens)

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))


    return ObjectExpr2126()


def Decode_intDictionary(value_decoder: Decoder_1[Any]) -> Decoder_1[Any]:
    class ObjectExpr2133(Decoder_1[Any]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, value_decoder: Any=value_decoder) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value):
                errors: FSharpList[Any] = empty()
                tokens: Array[__A_] = helpers.as_array(value)
                dict_1: Any = dict([])
                decoder: Decoder_1[tuple[int, _VALUE_]] = tuple2(int_1, value_decoder)
                def folder(acc: FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]], value_1: __A_) -> FSharpResult_2[Any, tuple[str, ErrorReason_1[__A_]]]:
                    if acc.tag == 0:
                        acc_1: Any = acc.fields[0]
                        match_value: FSharpResult_2[tuple[int, _VALUE_], tuple[str, ErrorReason_1[__A_]]] = decoder.Decode(helpers, value_1)
                        if match_value.tag == 0:
                            tupled_arg: tuple[int, _VALUE_] = match_value.fields[0]
                            add_to_dict(acc_1, tupled_arg[0], tupled_arg[1])
                            return FSharpResult_2(0, acc_1)

                        else: 
                            return FSharpResult_2(1, match_value.fields[0])


                    else: 
                        return acc


                return fold(folder, FSharpResult_2(0, dict_1), tokens)

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an object", value)))


    return ObjectExpr2133()


def Decode_tryOneOf(decoders: FSharpList[Decoder_1[Any]]) -> Decoder_1[Any]:
    class ObjectExpr2138(Decoder_1[_VALUE_]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, decoders: Any=decoders) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
            def loop(errors_mut: FSharpList[tuple[str, ErrorReason_1[__A_]]], decoders_1_mut: FSharpList[Decoder_1[_VALUE_]]) -> FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]:
                while True:
                    (errors, decoders_1) = (errors_mut, decoders_1_mut)
                    if not is_empty(decoders_1):
                        decoding_result: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]]
                        try: 
                            decoding_result = head(decoders_1).Decode(helpers, value)

                        except Exception as e:
                            decoding_result = FSharpResult_2(1, ("", ErrorReason_1(6, str(e))))

                        if decoding_result.tag == 1:
                            errors_mut = cons(decoding_result.fields[0], errors)
                            decoders_1_mut = tail(decoders_1)
                            continue

                        else: 
                            return FSharpResult_2(0, decoding_result.fields[0])


                    else: 
                        return FSharpResult_2(1, ("", ErrorReason_1(7, errors)))

                    break

            return loop(empty(), decoders)

    return ObjectExpr2138()


__all__ = ["PyTime_toUniversalTimePy", "Helpers_prependPath", "Decode_isURI", "Decode_uri", "Decode_hasUnknownFields", "Decode_objectNoAdditionalProperties", "Decode_noAdditionalProperties", "Decode_resizeArrayOrSingleton", "Decode_datetime", "Decode_dictionary", "Decode_intDictionary", "Decode_tryOneOf"]


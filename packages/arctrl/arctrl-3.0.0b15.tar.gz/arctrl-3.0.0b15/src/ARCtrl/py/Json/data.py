from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, singleton)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters)
from ..fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.data import Data
from ..Core.data_file import DataFile
from ..Core.uri import URIModule_toString
from .comment import (encoder as encoder_1, decoder as decoder_1, ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from .context.rocrate.isa_data_context import context_jsonvalue
from .data_file import (ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1)
from .decode import (Decode_uri, Decode_objectNoAdditionalProperties)
from .encode import (try_include, try_include_seq)
from .idtable import encode
from .string_table import (encode_string, decode_string)

__A_ = TypeVar("__A_")

def encoder(d: Data) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], d: Any=d) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2422(value: str, d: Any=d) -> IEncodable:
        class ObjectExpr2421(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2421()

    def _arrow2424(value_2: str, d: Any=d) -> IEncodable:
        class ObjectExpr2423(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2423()

    def _arrow2426(value_4: str, d: Any=d) -> IEncodable:
        class ObjectExpr2425(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2425()

    def _arrow2428(value_6: str, d: Any=d) -> IEncodable:
        class ObjectExpr2427(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2427()

    def _arrow2429(comment: Comment, d: Any=d) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2422, d.ID), try_include("name", _arrow2424, d.Name), try_include("dataType", ISAJson_encoder_1, d.DataType), try_include("format", _arrow2426, d.Format), try_include("selectorFormat", _arrow2428, d.SelectorFormat), try_include_seq("comments", _arrow2429, d.Comments)]))
    class ObjectExpr2430(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], d: Any=d) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2430()


def _arrow2437(get: IGetters) -> Data:
    def _arrow2431(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2432(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2433(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("dataType", ISAJson_decoder_1)

    def _arrow2434(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("format", string)

    def _arrow2435(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("selectorFormat", Decode_uri)

    def _arrow2436(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow2431(), _arrow2432(), _arrow2433(), _arrow2434(), _arrow2435(), _arrow2436())


decoder: Decoder_1[Data] = object(_arrow2437)

def compressed_encoder(string_table: Any, d: Data) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, d: Any=d) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2439(s: str, string_table: Any=string_table, d: Any=d) -> IEncodable:
        return encode_string(string_table, s)

    def _arrow2440(s_1: str, string_table: Any=string_table, d: Any=d) -> IEncodable:
        return encode_string(string_table, s_1)

    def _arrow2441(s_2: str, string_table: Any=string_table, d: Any=d) -> IEncodable:
        return encode_string(string_table, s_2)

    def _arrow2442(s_3: str, string_table: Any=string_table, d: Any=d) -> IEncodable:
        return encode_string(string_table, s_3)

    def _arrow2443(comment: Comment, string_table: Any=string_table, d: Any=d) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("i", _arrow2439, d.ID), try_include("n", _arrow2440, d.Name), try_include("d", ISAJson_encoder_1, d.DataType), try_include("f", _arrow2441, d.Format), try_include("s", _arrow2442, d.SelectorFormat), try_include_seq("c", _arrow2443, d.Comments)]))
    class ObjectExpr2444(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], string_table: Any=string_table, d: Any=d) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr2444()


def compressed_decoder(string_table: Array[str]) -> Decoder_1[Data]:
    def _arrow2451(get: IGetters, string_table: Any=string_table) -> Data:
        def _arrow2445(__unit: None=None) -> str | None:
            arg_1: Decoder_1[str] = decode_string(string_table)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("i", arg_1)

        def _arrow2446(__unit: None=None) -> str | None:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("n", arg_3)

        def _arrow2447(__unit: None=None) -> DataFile | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("d", ISAJson_decoder_1)

        def _arrow2448(__unit: None=None) -> str | None:
            arg_7: Decoder_1[str] = decode_string(string_table)
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("f", arg_7)

        def _arrow2449(__unit: None=None) -> str | None:
            arg_9: Decoder_1[str] = decode_string(string_table)
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("s", arg_9)

        def _arrow2450(__unit: None=None) -> Array[Comment] | None:
            arg_11: Decoder_1[Array[Comment]] = resize_array(decoder_1)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("c", arg_11)

        return Data(_arrow2445(), _arrow2446(), _arrow2447(), _arrow2448(), _arrow2449(), _arrow2450())

    return object(_arrow2451)


def ROCrate_genID(d: Data) -> str:
    match_value: str | None = d.ID
    if match_value is None:
        match_value_1: str | None = d.Name
        if match_value_1 is None:
            return "#EmptyData"

        else: 
            return replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def ROCrate_encoder(oa: Data) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2455(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2454(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2454()

    class ObjectExpr2456(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Data")

    def _arrow2458(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2457(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2457()

    def _arrow2459(value_4: DataFile, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(value_4)

    def _arrow2461(value_5: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2460(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2460()

    def _arrow2463(value_7: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2462(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr2462()

    def _arrow2464(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_2(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2455()), ("@type", list_1_1(singleton(ObjectExpr2456()))), try_include("name", _arrow2458, oa.Name), try_include("type", _arrow2459, oa.DataType), try_include("encodingFormat", _arrow2461, oa.Format), try_include("usageInfo", _arrow2463, oa.SelectorFormat), try_include_seq("comments", _arrow2464, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2465(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2465()


def _arrow2472(get: IGetters) -> Data:
    def _arrow2466(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2467(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2468(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", ROCrate_decoder_1)

    def _arrow2469(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("encodingFormat", string)

    def _arrow2470(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("usageInfo", Decode_uri)

    def _arrow2471(__unit: None=None) -> Array[Comment] | None:
        arg_11: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_11)

    return Data(_arrow2466(), _arrow2467(), _arrow2468(), _arrow2469(), _arrow2470(), _arrow2471())


ROCrate_decoder: Decoder_1[Data] = object(_arrow2472)

def ISAJson_encoder(id_map: Any | None, oa: Data) -> IEncodable:
    def f(oa_1: Data, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2476(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2475(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2475()

        def _arrow2478(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2477(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2477()

        def _arrow2479(comment: Comment, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2476, ROCrate_genID(oa_1)), try_include("name", _arrow2478, oa_1.Name), try_include("type", ISAJson_encoder_1, oa_1.DataType), try_include_seq("comments", _arrow2479, oa_1.Comments)]))
        class ObjectExpr2480(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2480()

    if id_map is not None:
        def _arrow2481(d_1: Data, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(d_1)

        return encode(_arrow2481, f, oa, id_map)

    else: 
        return f(oa)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "type", "comments", "@type", "@context"])

def _arrow2486(get: IGetters) -> Data:
    def _arrow2482(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2483(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2484(__unit: None=None) -> DataFile | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("type", ISAJson_decoder_1)

    def _arrow2485(__unit: None=None) -> Array[Comment] | None:
        arg_7: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_2)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("comments", arg_7)

    return Data(_arrow2482(), _arrow2483(), _arrow2484(), None, None, _arrow2485())


ISAJson_decoder: Decoder_1[Data] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2486)

__all__ = ["encoder", "decoder", "compressed_encoder", "compressed_decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]


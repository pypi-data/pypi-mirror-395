from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList, is_empty, head, tail)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IRequiredGetter, unit, list_1 as list_1_2, string, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.Process.material_attribute_value import MaterialAttributeValue
from ...Core.Process.source import Source
from ...Core.uri import URIModule_toString
from ..context.rocrate.isa_source_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from .material_attribute_value import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def ROCrate_genID(s: Source) -> str:
    match_value: str | None = s.ID
    if match_value is None:
        match_value_1: str | None = s.Name
        if match_value_1 is None:
            return "#EmptySource"

        else: 
            return "#Source_" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def ROCrate_encoder(oa: Source) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2844(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2843(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2843()

    class ObjectExpr2845(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Source")

    class ObjectExpr2846(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Source")

    def _arrow2848(value_3: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2847(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr2847()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2844()), ("@type", list_1_1(singleton(ObjectExpr2845()))), ("additionalType", ObjectExpr2846()), try_include("name", _arrow2848, oa.Name), try_include_list_opt("characteristics", ROCrate_encoder_1, oa.Characteristics), ("@context", context_jsonvalue)]))
    class ObjectExpr2849(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2849()


def _arrow2853(get: IGetters) -> Source:
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("additionalType", Decode_uri)
    (pattern_matching_result,) = (None,)
    if match_value is None:
        pattern_matching_result = 0

    elif match_value == "Source":
        pattern_matching_result = 0

    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 1:
        object_arg_1: IRequiredGetter = get.Required
        object_arg_1.Field("FailBecauseNotSample", unit)

    match_value_1: FSharpList[str] | None
    arg_5: Decoder_1[FSharpList[str]] = list_1_2(string)
    object_arg_2: IOptionalGetter = get.Optional
    match_value_1 = object_arg_2.Field("@type", arg_5)
    (pattern_matching_result_1,) = (None,)
    if match_value_1 is None:
        pattern_matching_result_1 = 0

    elif not is_empty(match_value_1):
        if head(match_value_1) == "Source":
            if is_empty(tail(match_value_1)):
                pattern_matching_result_1 = 0

            else: 
                pattern_matching_result_1 = 1


        else: 
            pattern_matching_result_1 = 1


    else: 
        pattern_matching_result_1 = 1

    if pattern_matching_result_1 == 1:
        object_arg_3: IRequiredGetter = get.Required
        object_arg_3.Field("FailBecauseNotSample", unit)

    def _arrow2850(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("@id", Decode_uri)

    def _arrow2851(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("name", string)

    def _arrow2852(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
        arg_13: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ROCrate_decoder_1)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("characteristics", arg_13)

    return Source(_arrow2850(), _arrow2851(), _arrow2852())


ROCrate_decoder: Decoder_1[Source] = object(_arrow2853)

def ISAJson_encoder(id_map: Any | None, oa: Source) -> IEncodable:
    def f(oa_1: Source, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2857(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2856(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2856()

        def _arrow2859(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2858(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2858()

        def _arrow2860(oa_2: MaterialAttributeValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(id_map, oa_2)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2857, ROCrate_genID(oa_1)), try_include("name", _arrow2859, oa_1.Name), try_include_list_opt("characteristics", _arrow2860, oa_1.Characteristics)]))
        class ObjectExpr2861(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2861()

    if id_map is not None:
        def _arrow2862(s_1: Source, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(s_1)

        return encode(_arrow2862, f, oa, id_map)

    else: 
        return f(oa)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "characteristics", "@type", "@context"])

def _arrow2866(get: IGetters) -> Source:
    def _arrow2863(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2864(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2865(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
        arg_5: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ISAJson_decoder_1)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("characteristics", arg_5)

    return Source(_arrow2863(), _arrow2864(), _arrow2865())


ISAJson_decoder: Decoder_1[Source] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2866)

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]


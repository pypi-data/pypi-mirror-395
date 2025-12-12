from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (FSharpList, map, empty, append, choose, singleton, of_array, is_empty, head, tail)
from ...fable_modules.fable_library.option import (default_arg, map as map_1)
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import map as map_2
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (string, object, IOptionalGetter, IRequiredGetter, unit, list_1 as list_1_3, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_2
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ...Core.Helper.collections_ import Option_fromValueWithDefault
from ...Core.Process.factor_value import FactorValue
from ...Core.Process.material_attribute_value import MaterialAttributeValue
from ...Core.Process.sample import Sample
from ...Core.Process.source import Source
from ..context.rocrate.isa_sample_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_list, try_include_list_opt)
from ..idtable import encode
from .factor_value import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from .material_attribute_value import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)
from .source import (ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_3)

__A_ = TypeVar("__A_")

def ROCrate_genID(s: Sample) -> str:
    match_value: str | None = s.ID
    if match_value is None:
        match_value_1: str | None = s.Name
        if match_value_1 is None:
            return "#EmptySample"

        else: 
            return "#Sample_" + replace(match_value_1, " ", "_")


    else: 
        return match_value



def ROCrate_encoder(oa: Sample) -> IEncodable:
    additional_properties: FSharpList[IEncodable]
    list_4: FSharpList[IEncodable] = map(ROCrate_encoder_1, default_arg(oa.Characteristics, empty()))
    additional_properties = append(map(ROCrate_encoder_2, default_arg(oa.FactorValues, empty())), list_4)
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map_1(mapping, tupled_arg[1])

    def _arrow2890(__unit: None=None, oa: Any=oa) -> IEncodable:
        value_2: str = ROCrate_genID(oa)
        class ObjectExpr2889(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value_2)

        return ObjectExpr2889()

    class ObjectExpr2891(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Sample")

    class ObjectExpr2892(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Sample")

    def _arrow2894(value_5: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2893(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2893()

    def _arrow2895(x: IEncodable, oa: Any=oa) -> IEncodable:
        return x

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2890()), ("@type", list_1_2(singleton(ObjectExpr2891()))), ("additionalType", ObjectExpr2892()), try_include("name", _arrow2894, oa.Name), try_include_list("additionalProperties", _arrow2895, additional_properties), ("@context", context_jsonvalue)]))
    class ObjectExpr2896(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2896()


class ObjectExpr2898(Decoder_1[tuple[MaterialAttributeValue | None, FactorValue | None]]):
    def Decode(self, s: IDecoderHelpers_1[Any], json: Any) -> FSharpResult_2[tuple[MaterialAttributeValue | None, FactorValue | None], tuple[str, ErrorReason_1[__A_]]]:
        def _arrow2897(__unit: None=None) -> str:
            match_value: FSharpResult_2[str, tuple[str, ErrorReason_1[__A_]]] = string.Decode(s, s.get_property("additionalType", json))
            return match_value.fields[0] if (match_value.tag == 0) else ""

        if (_arrow2897() if s.has_property("additionalType", json) else "") == "FactorValue":
            match_value_1: FSharpResult_2[FactorValue, tuple[str, ErrorReason_1[__A_]]] = ROCrate_decoder_1.Decode(s, json)
            return FSharpResult_2(1, match_value_1.fields[0]) if (match_value_1.tag == 1) else FSharpResult_2(0, (None, match_value_1.fields[0]))

        else: 
            match_value_2: FSharpResult_2[MaterialAttributeValue, tuple[str, ErrorReason_1[__A_]]] = ROCrate_decoder_2.Decode(s, json)
            return FSharpResult_2(1, match_value_2.fields[0]) if (match_value_2.tag == 1) else FSharpResult_2(0, (match_value_2.fields[0], None))



ROCrate_additionalPropertyDecoder: Decoder_1[tuple[MaterialAttributeValue | None, FactorValue | None]] = ObjectExpr2898()

def _arrow2902(get: IGetters) -> Sample:
    match_value: str | None
    object_arg: IOptionalGetter = get.Optional
    match_value = object_arg.Field("additionalType", Decode_uri)
    (pattern_matching_result,) = (None,)
    if match_value is None:
        pattern_matching_result = 0

    elif match_value == "Sample":
        pattern_matching_result = 0

    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 1:
        object_arg_1: IRequiredGetter = get.Required
        object_arg_1.Field("FailBecauseNotSample", unit)

    match_value_1: FSharpList[str] | None
    arg_5: Decoder_1[FSharpList[str]] = list_1_3(string)
    object_arg_2: IOptionalGetter = get.Optional
    match_value_1 = object_arg_2.Field("@type", arg_5)
    (pattern_matching_result_1,) = (None,)
    if match_value_1 is None:
        pattern_matching_result_1 = 0

    elif not is_empty(match_value_1):
        if head(match_value_1) == "Sample":
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

    additional_properties: FSharpList[tuple[MaterialAttributeValue | None, FactorValue | None]] | None
    arg_9: Decoder_1[FSharpList[tuple[MaterialAttributeValue | None, FactorValue | None]]] = list_1_3(ROCrate_additionalPropertyDecoder)
    object_arg_4: IOptionalGetter = get.Optional
    additional_properties = object_arg_4.Field("additionalProperties", arg_9)
    pattern_input: tuple[FSharpList[MaterialAttributeValue] | None, FSharpList[FactorValue] | None]
    if additional_properties is not None:
        additional_properties_1: FSharpList[tuple[MaterialAttributeValue | None, FactorValue | None]] = additional_properties
        def chooser(tuple: tuple[MaterialAttributeValue | None, FactorValue | None]) -> MaterialAttributeValue | None:
            return tuple[0]

        def chooser_1(tuple_1: tuple[MaterialAttributeValue | None, FactorValue | None]) -> FactorValue | None:
            return tuple_1[1]

        pattern_input = (Option_fromValueWithDefault(empty(), choose(chooser, additional_properties_1)), Option_fromValueWithDefault(empty(), choose(chooser_1, additional_properties_1)))

    else: 
        pattern_input = (None, None)

    def _arrow2899(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("@id", Decode_uri)

    def _arrow2900(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("name", string)

    def _arrow2901(__unit: None=None) -> FSharpList[Source] | None:
        arg_15: Decoder_1[FSharpList[Source]] = list_1_3(ROCrate_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("derivesFrom", arg_15)

    return Sample(_arrow2899(), _arrow2900(), pattern_input[0], pattern_input[1], _arrow2901())


ROCrate_decoder: Decoder_1[Sample] = object(_arrow2902)

def ISAJson_encoder(id_map: Any | None, oa: Sample) -> IEncodable:
    def f(oa_1: Sample, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map_1(mapping, tupled_arg[1])

        def _arrow2906(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2905(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2905()

        def _arrow2908(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2907(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2907()

        def _arrow2909(oa_2: MaterialAttributeValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(id_map, oa_2)

        def _arrow2910(fv: FactorValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, fv)

        def _arrow2911(oa_3: Source, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_3(id_map, oa_3)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2906, ROCrate_genID(oa_1)), try_include("name", _arrow2908, oa_1.Name), try_include_list_opt("characteristics", _arrow2909, oa_1.Characteristics), try_include_list_opt("factorValues", _arrow2910, oa_1.FactorValues), try_include_list_opt("derivesFrom", _arrow2911, oa_1.DerivesFrom)]))
        class ObjectExpr2912(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2912()

    if id_map is not None:
        def _arrow2913(s_1: Sample, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(s_1)

        return encode(_arrow2913, f, oa, id_map)

    else: 
        return f(oa)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "name", "characteristics", "factorValues", "derivesFrom", "@type", "@context"])

def _arrow2919(get: IGetters) -> Sample:
    def _arrow2914(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2915(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2916(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
        arg_5: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_3(ISAJson_decoder_1)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("characteristics", arg_5)

    def _arrow2917(__unit: None=None) -> FSharpList[FactorValue] | None:
        arg_7: Decoder_1[FSharpList[FactorValue]] = list_1_3(ISAJson_decoder_2)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("factorValues", arg_7)

    def _arrow2918(__unit: None=None) -> FSharpList[Source] | None:
        arg_9: Decoder_1[FSharpList[Source]] = list_1_3(ISAJson_decoder_3)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("derivesFrom", arg_9)

    return Sample(_arrow2914(), _arrow2915(), _arrow2916(), _arrow2917(), _arrow2918())


ISAJson_decoder: Decoder_1[Sample] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2919)

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_additionalPropertyDecoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]


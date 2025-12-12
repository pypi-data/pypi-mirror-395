from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IRequiredGetter, unit, string, list_1 as list_1_2, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.Process.material import Material
from ...Core.Process.material_attribute_value import MaterialAttributeValue
from ...Core.Process.material_type import MaterialType
from ..context.rocrate.isa_material_context import context_jsonvalue
from ..decode import (Decode_uri, Decode_objectNoAdditionalProperties)
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from .material_attribute_value import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from .material_type import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def ROCrate_genID(m: Material) -> str:
    match_value: str | None = m.ID
    if match_value is None:
        match_value_1: str | None = m.Name
        if match_value_1 is None:
            return "#EmptyMaterial"

        else: 
            return "#Material_" + replace(match_value_1, " ", "_")


    else: 
        return match_value



def ROCrate_encoder(oa: Material) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2809(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2808(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2808()

    class ObjectExpr2810(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Material")

    class ObjectExpr2811(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_2.encode_string("Material")

    def _arrow2813(value_3: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2812(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr2812()

    def _arrow2814(value_5: MaterialType, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(value_5)

    def _arrow2815(oa_1: Material, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder(oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2809()), ("@type", list_1_1(singleton(ObjectExpr2810()))), ("additionalType", ObjectExpr2811()), try_include("name", _arrow2813, oa.Name), try_include("type", _arrow2814, oa.MaterialType), try_include_list_opt("characteristics", ROCrate_encoder_2, oa.Characteristics), try_include_list_opt("derivesFrom", _arrow2815, oa.DerivesFrom), ("@context", context_jsonvalue)]))
    class ObjectExpr2816(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2816()


def _arrow2823(__unit: None=None) -> Decoder_1[Material]:
    def decode(__unit: None=None) -> Decoder_1[Material]:
        def _arrow2822(get: IGetters) -> Material:
            match_value: str | None
            object_arg: IOptionalGetter = get.Optional
            match_value = object_arg.Field("additionalType", Decode_uri)
            (pattern_matching_result,) = (None,)
            if match_value is None:
                pattern_matching_result = 0

            elif match_value == "Material":
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1

            if pattern_matching_result == 1:
                object_arg_1: IRequiredGetter = get.Required
                object_arg_1.Field("FailBecauseNotSample", unit)

            def _arrow2817(__unit: None=None) -> str | None:
                object_arg_2: IOptionalGetter = get.Optional
                return object_arg_2.Field("@id", Decode_uri)

            def _arrow2818(__unit: None=None) -> str | None:
                object_arg_3: IOptionalGetter = get.Optional
                return object_arg_3.Field("name", string)

            def _arrow2819(__unit: None=None) -> MaterialType | None:
                object_arg_4: IOptionalGetter = get.Optional
                return object_arg_4.Field("type", ROCrate_decoder_1)

            def _arrow2820(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
                arg_11: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ROCrate_decoder_2)
                object_arg_5: IOptionalGetter = get.Optional
                return object_arg_5.Field("characteristics", arg_11)

            def _arrow2821(__unit: None=None) -> FSharpList[Material] | None:
                arg_13: Decoder_1[FSharpList[Material]] = list_1_2(decode(None))
                object_arg_6: IOptionalGetter = get.Optional
                return object_arg_6.Field("derivesFrom", arg_13)

            return Material(_arrow2817(), _arrow2818(), _arrow2819(), _arrow2820(), _arrow2821())

        return object(_arrow2822)

    return decode(None)


ROCrate_decoder: Decoder_1[Material] = _arrow2823()

def ISAJson_encoder(id_map: Any | None, c: Material) -> IEncodable:
    def f(oa: Material, id_map: Any=id_map, c: Any=c) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2827(value: str, oa: Any=oa) -> IEncodable:
            class ObjectExpr2826(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2826()

        def _arrow2829(value_2: str, oa: Any=oa) -> IEncodable:
            class ObjectExpr2828(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2828()

        def _arrow2830(oa_1: MaterialAttributeValue, oa: Any=oa) -> IEncodable:
            return ISAJson_encoder_2(id_map, oa_1)

        def _arrow2831(c_1: Material, oa: Any=oa) -> IEncodable:
            return ISAJson_encoder(id_map, c_1)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2827, ROCrate_genID(oa)), try_include("name", _arrow2829, oa.Name), try_include("type", ISAJson_encoder_1, oa.MaterialType), try_include_list_opt("characteristics", _arrow2830, oa.Characteristics), try_include_list_opt("derivesFrom", _arrow2831, oa.DerivesFrom)]))
        class ObjectExpr2832(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2832()

    if id_map is not None:
        def _arrow2833(m_1: Material, id_map: Any=id_map, c: Any=c) -> str:
            return ROCrate_genID(m_1)

        return encode(_arrow2833, f, c, id_map)

    else: 
        return f(c)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "@type", "name", "type", "characteristics", "derivesFrom", "@context"])

def _arrow2840(__unit: None=None) -> Decoder_1[Material]:
    def decode(__unit: None=None) -> Decoder_1[Material]:
        def _arrow2839(get: IGetters) -> Material:
            def _arrow2834(__unit: None=None) -> str | None:
                object_arg: IOptionalGetter = get.Optional
                return object_arg.Field("@id", Decode_uri)

            def _arrow2835(__unit: None=None) -> str | None:
                object_arg_1: IOptionalGetter = get.Optional
                return object_arg_1.Field("name", string)

            def _arrow2836(__unit: None=None) -> MaterialType | None:
                object_arg_2: IOptionalGetter = get.Optional
                return object_arg_2.Field("type", ISAJson_decoder_1)

            def _arrow2837(__unit: None=None) -> FSharpList[MaterialAttributeValue] | None:
                arg_7: Decoder_1[FSharpList[MaterialAttributeValue]] = list_1_2(ISAJson_decoder_2)
                object_arg_3: IOptionalGetter = get.Optional
                return object_arg_3.Field("characteristics", arg_7)

            def _arrow2838(__unit: None=None) -> FSharpList[Material] | None:
                arg_9: Decoder_1[FSharpList[Material]] = list_1_2(decode(None))
                object_arg_4: IOptionalGetter = get.Optional
                return object_arg_4.Field("derivesFrom", arg_9)

            return Material(_arrow2834(), _arrow2835(), _arrow2836(), _arrow2837(), _arrow2838())

        return Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2839)

    return decode(None)


ISAJson_decoder: Decoder_1[Material] = _arrow2840()

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]


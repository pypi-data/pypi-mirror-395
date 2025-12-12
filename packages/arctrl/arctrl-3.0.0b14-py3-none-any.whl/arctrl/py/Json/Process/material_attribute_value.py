from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, Decoder_1, IEncoderHelpers_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.material_attribute import MaterialAttribute
from ...Core.Process.material_attribute_value import (MaterialAttributeValue, MaterialAttributeValue_createAsPV)
from ...Core.value import Value as Value_1
from ..decode import Decode_uri
from ..encode import try_include
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from ..property_value import (encoder, decoder, gen_id)
from .material_attribute import (encoder as encoder_1, decoder as decoder_1)
from .value import (encoder as encoder_2, decoder as decoder_2)

__A_ = TypeVar("__A_")

ROCrate_encoder: Callable[[MaterialAttributeValue], IEncodable] = encoder

ROCrate_decoder: Decoder_1[MaterialAttributeValue] = decoder(MaterialAttributeValue_createAsPV)

def ISAJson_genID(oa: MaterialAttributeValue) -> str:
    return gen_id(oa)


def ISAJson_encoder(id_map: Any | None, oa: MaterialAttributeValue) -> IEncodable:
    def f(oa_1: MaterialAttributeValue, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2739(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2738(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2738()

        def _arrow2740(value_2: MaterialAttribute, oa_1: Any=oa_1) -> IEncodable:
            return encoder_1(id_map, value_2)

        def _arrow2741(value_3: Value_1, oa_1: Any=oa_1) -> IEncodable:
            return encoder_2(id_map, value_3)

        def _arrow2742(oa_3: OntologyAnnotation, oa_1: Any=oa_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2739, ISAJson_genID(oa_1)), try_include("category", _arrow2740, oa_1.Category), try_include("value", _arrow2741, oa_1.Value), try_include("unit", _arrow2742, oa_1.Unit)]))
        class ObjectExpr2743(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_1.encode_object(arg)

        return ObjectExpr2743()

    if id_map is not None:
        def _arrow2744(oa_4: MaterialAttributeValue, id_map: Any=id_map, oa: Any=oa) -> str:
            return ISAJson_genID(oa_4)

        return encode(_arrow2744, f, oa, id_map)

    else: 
        return f(oa)



def _arrow2749(get: IGetters) -> MaterialAttributeValue:
    def _arrow2745(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2746(__unit: None=None) -> MaterialAttribute | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("category", decoder_1)

    def _arrow2747(__unit: None=None) -> Value_1 | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("value", decoder_2)

    def _arrow2748(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("unit", OntologyAnnotation_ISAJson_decoder)

    return MaterialAttributeValue(_arrow2745(), _arrow2746(), _arrow2747(), _arrow2748())


ISAJson_decoder: Decoder_1[MaterialAttributeValue] = object(_arrow2749)

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_genID", "ISAJson_encoder", "ISAJson_decoder"]


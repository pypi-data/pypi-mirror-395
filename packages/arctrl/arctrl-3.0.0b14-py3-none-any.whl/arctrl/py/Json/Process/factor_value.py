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
from ...Core.Process.factor import Factor
from ...Core.Process.factor_value import (FactorValue, FactorValue_createAsPV)
from ...Core.value import Value as Value_1
from ..decode import Decode_uri
from ..encode import try_include
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from ..property_value import (encoder, decoder, gen_id)
from .factor import (encoder as encoder_1, decoder as decoder_1)
from .value import (encoder as encoder_2, decoder as decoder_2)

__A_ = TypeVar("__A_")

ROCrate_encoder: Callable[[FactorValue], IEncodable] = encoder

ROCrate_decoder: Decoder_1[FactorValue] = decoder(FactorValue_createAsPV)

def ISAJson_genID(fv: FactorValue) -> str:
    return gen_id(fv)


def ISAJson_encoder(id_map: Any | None, fv: FactorValue) -> IEncodable:
    def f(fv_1: FactorValue, id_map: Any=id_map, fv: Any=fv) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], fv_1: Any=fv_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2623(value: str, fv_1: Any=fv_1) -> IEncodable:
            class ObjectExpr2622(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2622()

        def _arrow2624(value_2: Factor, fv_1: Any=fv_1) -> IEncodable:
            return encoder_1(id_map, value_2)

        def _arrow2627(value_3: Value_1, fv_1: Any=fv_1) -> IEncodable:
            return encoder_2(id_map, value_3)

        def _arrow2628(oa: OntologyAnnotation, fv_1: Any=fv_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2623, ISAJson_genID(fv_1)), try_include("category", _arrow2624, fv_1.Category), try_include("value", _arrow2627, fv_1.Value), try_include("unit", _arrow2628, fv_1.Unit)]))
        class ObjectExpr2631(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], fv_1: Any=fv_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_1.encode_object(arg)

        return ObjectExpr2631()

    if id_map is not None:
        def _arrow2635(fv_3: FactorValue, id_map: Any=id_map, fv: Any=fv) -> str:
            return ISAJson_genID(fv_3)

        return encode(_arrow2635, f, fv, id_map)

    else: 
        return f(fv)



def _arrow2643(get: IGetters) -> FactorValue:
    def _arrow2638(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2639(__unit: None=None) -> Factor | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("category", decoder_1)

    def _arrow2640(__unit: None=None) -> Value_1 | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("value", decoder_2)

    def _arrow2641(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("unit", OntologyAnnotation_ISAJson_decoder)

    return FactorValue(_arrow2638(), _arrow2639(), _arrow2640(), _arrow2641())


ISAJson_decoder: Decoder_1[FactorValue] = object(_arrow2643)

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_genID", "ISAJson_encoder", "ISAJson_decoder"]


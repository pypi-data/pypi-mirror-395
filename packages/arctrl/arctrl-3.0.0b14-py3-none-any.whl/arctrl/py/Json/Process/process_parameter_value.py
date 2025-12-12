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
from ...Core.Process.process_parameter_value import ProcessParameterValue
from ...Core.Process.protocol_parameter import ProtocolParameter
from ...Core.value import Value
from ..encode import try_include
from ..ontology_annotation import (OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from ..property_value import (encoder, decoder)
from .protocol_parameter import (ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)
from .value import (encoder as encoder_1, decoder as decoder_1)

__A_ = TypeVar("__A_")

ROCrate_encoder: Callable[[ProcessParameterValue], IEncodable] = encoder

def _arrow2867(alternate_name: str | None=None, measurement_method: str | None=None, description: str | None=None, category: OntologyAnnotation | None=None, value: Value | None=None, unit: OntologyAnnotation | None=None) -> ProcessParameterValue:
    return ProcessParameterValue.create_as_pv(alternate_name, measurement_method, description, category, value, unit)


ROCrate_decoder: Decoder_1[ProcessParameterValue] = decoder(_arrow2867)

def ISAJson_genID(oa: ProcessParameterValue) -> Any:
    raise Exception("Not implemented")


def ISAJson_encoder(id_map: Any | None, oa: ProcessParameterValue) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2869(value: ProtocolParameter, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return ISAJson_encoder_1(id_map, value)

    def _arrow2870(value_1: Value, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return encoder_1(id_map, value_1)

    def _arrow2871(oa_1: OntologyAnnotation, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ISAJson_encoder(id_map, oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("category", _arrow2869, oa.Category), try_include("value", _arrow2870, oa.Value), try_include("unit", _arrow2871, oa.Unit)]))
    class ObjectExpr2872(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], id_map: Any=id_map, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr2872()


def _arrow2876(get: IGetters) -> ProcessParameterValue:
    def _arrow2873(__unit: None=None) -> ProtocolParameter | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("category", ISAJson_decoder_1)

    def _arrow2874(__unit: None=None) -> Value | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", decoder_1)

    def _arrow2875(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("unit", OntologyAnnotation_ISAJson_decoder)

    return ProcessParameterValue(_arrow2873(), _arrow2874(), _arrow2875())


ISAJson_decoder: Decoder_1[ProcessParameterValue] = object(_arrow2876)

__all__ = ["ROCrate_encoder", "ROCrate_decoder", "ISAJson_genID", "ISAJson_encoder", "ISAJson_decoder"]


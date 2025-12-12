from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import (default_arg, map as map_1)
from ...fable_modules.fable_library.seq import map as map_2
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (map, object, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, Decoder_1, IEncoderHelpers_1)
from ...Core.Helper.collections_ import Option_fromValueWithDefault
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.protocol_parameter import ProtocolParameter
from ..encode import try_include
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_genID, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)

__A_ = TypeVar("__A_")

def encoder(value: ProtocolParameter) -> IEncodable:
    return OntologyAnnotation_encoder(default_arg(value.ParameterName, OntologyAnnotation()))


def ctor(oa: OntologyAnnotation) -> ProtocolParameter:
    oa_1: OntologyAnnotation | None = Option_fromValueWithDefault(OntologyAnnotation(), oa)
    return ProtocolParameter.create(None, oa_1)


decoder: Decoder_1[ProtocolParameter] = map(ctor, OntologyAnnotation_decoder)

def ISAJson_genID(p: ProtocolParameter) -> str:
    match_value: OntologyAnnotation | None = p.ParameterName
    if match_value is None:
        return "#EmptyProtocolParameter"

    else: 
        return ("#ProtocolParameter/" + OntologyAnnotation_ROCrate_genID(match_value)) + ""



def ISAJson_encoder(id_map: Any | None, value: ProtocolParameter) -> IEncodable:
    def f(value_1: ProtocolParameter, id_map: Any=id_map, value: Any=value) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], value_1: Any=value_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map_1(mapping, tupled_arg[1])

        def _arrow2702(value_2: str, value_1: Any=value_1) -> IEncodable:
            class ObjectExpr2701(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value_2)

            return ObjectExpr2701()

        def _arrow2703(oa: OntologyAnnotation, value_1: Any=value_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2702, ISAJson_genID(value_1)), try_include("parameterName", _arrow2703, value_1.ParameterName)]))
        class ObjectExpr2704(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value_1: Any=value_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

                arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping_1, values)
                return helpers_1.encode_object(arg)

        return ObjectExpr2704()

    if id_map is not None:
        def _arrow2705(p_1: ProtocolParameter, id_map: Any=id_map, value: Any=value) -> str:
            return ISAJson_genID(p_1)

        return encode(_arrow2705, f, value, id_map)

    else: 
        return f(value)



def _arrow2707(get: IGetters) -> ProtocolParameter:
    def _arrow2706(__unit: None=None) -> OntologyAnnotation | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("parameterName", OntologyAnnotation_ISAJson_decoder)

    return ProtocolParameter(None, _arrow2706())


ISAJson_decoder: Decoder_1[ProtocolParameter] = object(_arrow2707)

__all__ = ["encoder", "decoder", "ISAJson_genID", "ISAJson_encoder", "ISAJson_decoder"]


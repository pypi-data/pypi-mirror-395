from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.component import (Component, Component_createAsPV, Component__get_ComponentName, Component_decomposeName_Z721C83C5)
from ...Core.value import Value
from ..decode import Decode_uri
from ..encode import try_include
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from ..property_value import (encoder as encoder_2, decoder as decoder_2, gen_id)
from .value import (encoder as encoder_1, decoder as decoder_1)

__A_ = TypeVar("__A_")

def encoder(value: Component) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], value: Any=value) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2721(oa: OntologyAnnotation, value: Any=value) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2722(value_1: Value, value: Any=value) -> IEncodable:
        return encoder_1(None, value_1)

    def _arrow2723(oa_1: OntologyAnnotation, value: Any=value) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("type", _arrow2721, value.ComponentType), try_include("value", _arrow2722, value.ComponentValue), try_include("unit", _arrow2723, value.ComponentUnit)]))
    class ObjectExpr2724(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers.encode_object(arg)

    return ObjectExpr2724()


def _arrow2727(get: IGetters) -> Component:
    ComponentType: OntologyAnnotation | None
    object_arg: IOptionalGetter = get.Optional
    ComponentType = object_arg.Field("type", OntologyAnnotation_decoder)
    def _arrow2725(__unit: None=None) -> Value | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", decoder_1)

    def _arrow2726(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("unit", OntologyAnnotation_decoder)

    return Component(_arrow2725(), _arrow2726(), ComponentType)


decoder: Decoder_1[Component] = object(_arrow2727)

ROCrate_encoder: Callable[[Component], IEncodable] = encoder_2

ROCrate_decoder: Decoder_1[Component] = decoder_2(Component_createAsPV)

def ISAJson_genID(c: Component) -> str:
    return gen_id(c)


def ISAJson_encoder(id_map: Any | None, c: Component) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, c: Any=c) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2731(value: str, id_map: Any=id_map, c: Any=c) -> IEncodable:
        class ObjectExpr2730(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2730()

    def _arrow2732(oa: OntologyAnnotation, id_map: Any=id_map, c: Any=c) -> IEncodable:
        return OntologyAnnotation_ISAJson_encoder(id_map, oa)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("componentName", _arrow2731, Component__get_ComponentName(c)), try_include("componentType", _arrow2732, c.ComponentType)]))
    class ObjectExpr2733(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], id_map: Any=id_map, c: Any=c) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr2733()


def _arrow2735(get: IGetters) -> Component:
    name: str | None
    object_arg: IOptionalGetter = get.Optional
    name = object_arg.Field("componentName", Decode_uri)
    pattern_input_1: tuple[Value | None, OntologyAnnotation | None]
    if name is None:
        pattern_input_1 = (None, None)

    else: 
        pattern_input: tuple[Value, OntologyAnnotation | None] = Component_decomposeName_Z721C83C5(name)
        pattern_input_1 = (pattern_input[0], pattern_input[1])

    def _arrow2734(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("componentType", OntologyAnnotation_ISAJson_decoder)

    return Component(pattern_input_1[0], pattern_input_1[1], _arrow2734())


ISAJson_decoder: Decoder_1[Component] = object(_arrow2735)

__all__ = ["encoder", "decoder", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_genID", "ISAJson_encoder", "ISAJson_decoder"]


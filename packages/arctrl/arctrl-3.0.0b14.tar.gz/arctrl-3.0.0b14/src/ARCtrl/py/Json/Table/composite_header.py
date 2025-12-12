from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (singleton, empty, FSharpList)
from ...fable_modules.fable_library.seq import map
from ...fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ...fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, index, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.composite_header import (CompositeHeader, IOType)
from ..ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder)
from .iotype import (encoder as encoder_1, decoder as decoder_1)

__A_ = TypeVar("__A_")

def encoder(ch: CompositeHeader) -> IEncodable:
    def oa_to_json_string(oa: OntologyAnnotation, ch: Any=ch) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    class ObjectExpr3023(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], ch: Any=ch) -> Any:
            return helpers.encode_string(ch.fields[0])

    pattern_input: tuple[str, FSharpList[IEncodable]] = (("Comment", singleton(ObjectExpr3023()))) if (ch.tag == 14) else ((("Parameter", singleton(oa_to_json_string(ch.fields[0])))) if (ch.tag == 3) else ((("Factor", singleton(oa_to_json_string(ch.fields[0])))) if (ch.tag == 2) else ((("Characteristic", singleton(oa_to_json_string(ch.fields[0])))) if (ch.tag == 1) else ((("Component", singleton(oa_to_json_string(ch.fields[0])))) if (ch.tag == 0) else ((("ProtocolType", empty())) if (ch.tag == 4) else ((("ProtocolREF", empty())) if (ch.tag == 8) else ((("ProtocolDescription", empty())) if (ch.tag == 5) else ((("ProtocolUri", empty())) if (ch.tag == 6) else ((("ProtocolVersion", empty())) if (ch.tag == 7) else ((("Performer", empty())) if (ch.tag == 9) else ((("Date", empty())) if (ch.tag == 10) else ((("Input", singleton(encoder_1(ch.fields[0])))) if (ch.tag == 11) else ((("Output", singleton(encoder_1(ch.fields[0])))) if (ch.tag == 12) else ((ch.fields[0], empty())))))))))))))))
    class ObjectExpr3024(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], ch: Any=ch) -> Any:
            return helpers_1.encode_string(pattern_input[0])

    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("headertype", ObjectExpr3024()), ("values", list_1(pattern_input[1]))])
    class ObjectExpr3025(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], ch: Any=ch) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values_1)
            return helpers_2.encode_object(arg)

    return ObjectExpr3025()


def _arrow3027(get: IGetters) -> CompositeHeader:
    header_type: str
    object_arg: IRequiredGetter = get.Required
    header_type = object_arg.Field("headertype", string)
    def oa(__unit: None=None) -> OntologyAnnotation:
        arg_3: Decoder_1[OntologyAnnotation] = index(0, OntologyAnnotation_decoder)
        object_arg_1: IRequiredGetter = get.Required
        return object_arg_1.Field("values", arg_3)

    def io(__unit: None=None) -> IOType:
        arg_5: Decoder_1[IOType] = index(0, decoder_1)
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("values", arg_5)

    def _arrow3026(__unit: None=None) -> str:
        arg_7: Decoder_1[str] = index(0, string)
        object_arg_3: IRequiredGetter = get.Required
        return object_arg_3.Field("values", arg_7)

    return CompositeHeader(1, oa(None)) if (header_type == "Characteristic") else (CompositeHeader(3, oa(None)) if (header_type == "Parameter") else (CompositeHeader(0, oa(None)) if (header_type == "Component") else (CompositeHeader(2, oa(None)) if (header_type == "Factor") else (CompositeHeader(11, io(None)) if (header_type == "Input") else (CompositeHeader(12, io(None)) if (header_type == "Output") else (CompositeHeader(4) if (header_type == "ProtocolType") else (CompositeHeader(8) if (header_type == "ProtocolREF") else (CompositeHeader(5) if (header_type == "ProtocolDescription") else (CompositeHeader(6) if (header_type == "ProtocolUri") else (CompositeHeader(7) if (header_type == "ProtocolVersion") else (CompositeHeader(9) if (header_type == "Performer") else (CompositeHeader(10) if (header_type == "Date") else (CompositeHeader(14, _arrow3026()) if (header_type == "Comment") else CompositeHeader(13, header_type))))))))))))))


decoder: Decoder_1[CompositeHeader] = object(_arrow3027)

__all__ = ["encoder", "decoder"]


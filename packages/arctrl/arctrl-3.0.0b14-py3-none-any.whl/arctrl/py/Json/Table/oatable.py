from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import map as map_1
from ...fable_modules.fable_library.map_util import add_to_dict
from ...fable_modules.fable_library.seq import (to_array, map, sort_by)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import compare_primitives
from ...fable_modules.thoth_json_core.decode import (array as array_2, object, int_1, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.Helper.collections_ import (Dictionary_items, Dictionary_tryFind)
from ...Core.ontology_annotation import OntologyAnnotation
from ..ontology_annotation import (OntologyAnnotation_compressedEncoder, OntologyAnnotation_compressedDecoder)

__A_ = TypeVar("__A_")

def array_from_map(otm: Any) -> Array[OntologyAnnotation]:
    def mapping(kv_1: Any, otm: Any=otm) -> OntologyAnnotation:
        return kv_1[0]

    def projection(kv: Any, otm: Any=otm) -> int:
        return kv[1]

    class ObjectExpr2994:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    return to_array(map(mapping, sort_by(projection, Dictionary_items(otm), ObjectExpr2994())))


def encoder(string_table: Any, ot: Array[OntologyAnnotation]) -> IEncodable:
    def mapping(oa: OntologyAnnotation, string_table: Any=string_table, ot: Any=ot) -> IEncodable:
        return OntologyAnnotation_compressedEncoder(string_table, oa)

    values: Array[IEncodable] = map_1(mapping, ot, None)
    class ObjectExpr2995(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], string_table: Any=string_table, ot: Any=ot) -> Any:
            def mapping_1(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_1(mapping_1, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr2995()


def decoder(string_table: Array[str]) -> Decoder_1[Array[OntologyAnnotation]]:
    return array_2(OntologyAnnotation_compressedDecoder(string_table))


def encode_oa(otm: Any, oa: OntologyAnnotation) -> IEncodable:
    match_value: int | None = Dictionary_tryFind(oa, otm)
    if match_value is None:
        i_1: int = len(otm) or 0
        add_to_dict(otm, oa, i_1)
        class ObjectExpr2996(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], otm: Any=otm, oa: Any=oa) -> Any:
                return helpers_1.encode_signed_integral_number(i_1)

        return ObjectExpr2996()

    else: 
        i: int = match_value or 0
        class ObjectExpr2997(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], otm: Any=otm, oa: Any=oa) -> Any:
                return helpers.encode_signed_integral_number(i)

        return ObjectExpr2997()



def decode_oa(ot: Array[OntologyAnnotation]) -> Decoder_1[OntologyAnnotation]:
    def _arrow2998(get: IGetters, ot: Any=ot) -> OntologyAnnotation:
        i: int = get.Required.Raw(int_1) or 0
        return ot[i]

    return object(_arrow2998)


__all__ = ["array_from_map", "encoder", "decoder", "encode_oa", "decode_oa"]

